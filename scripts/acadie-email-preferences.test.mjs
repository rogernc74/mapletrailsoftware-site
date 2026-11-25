import assert from 'node:assert/strict';
import test from 'node:test';
import {mountEmailPreferences} from '../acadie/email-preferences.mjs';

function element() {
  const selectors = new Map(), callbacks = new Map();
  return {
    hidden: false, disabled: false, checked: false, value: '', textContent: '', children: [],
    querySelector(query) {
      if (!selectors.has(query)) {
        const child = element();
        child.parentElement = this;
        selectors.set(query, child);
      }
      return selectors.get(query);
    },
    append(...children) { this.children.push(...children); },
    addEventListener(name, handler) { callbacks.set(name, handler); },
    emit(name) { callbacks.get(name)?.({preventDefault() {}}); },
  };
}

const sender = {name: 'Fixture sender', mailing: 'Fixture address', privacy: 'https://example.invalid/privacy', contact: 'abc@example.invalid'};
const config = {available: true, enabled: true, address: 'owner@example.invalid', copyVersion: '2026-11-email-v2', sender};
const settle = () => new Promise(resolve => setImmediate(resolve));
function setup(call, locale = 'en') {
  const root = element();
  const select = mountEmailPreferences(root, locale, call);
  const form = root.querySelector('form');
  const fieldset = form.querySelector('fieldset');
  const [selectAll, ...labels] = fieldset.children;
  const boxes = labels.map(label => label.children[0]);
  const save = form.querySelector('button[type="submit"]');
  return {root, form, boxes, save, selectAll, select};
}

test('signed-in enrollment starts with no topics and submits exactly what was selected', async () => {
  globalThis.document = {createElement: element};
  const writes = [];
  const {root, form, boxes, save, selectAll, select} = setup(async input => {
    if (input.action === 'config') return config;
    if (input.action === 'status') return {status: 'none'};
    writes.push(input);
    return {status: 'active', topics: input.topics, topicsRevision: 'current'};
  });
  select(true);
  root.open = true;
  root.emit('toggle');
  await settle();
  assert.deepEqual(boxes.map(box => box.checked), [false, false, false]);
  assert.equal(save.disabled, true);
  assert.equal(form.querySelector('[data-email-sender]').hidden, false);
  assert.equal(selectAll.hidden, false);
  selectAll.emit('click');
  assert.deepEqual(boxes.map(box => box.checked), [true, true, true]);
  assert.deepEqual(writes, []);
  assert.equal(selectAll.disabled, true);
  boxes[0].checked = false;
  boxes[0].emit('change');
  assert.equal(selectAll.disabled, false);
  boxes[2].checked = false;
  boxes[2].emit('change');
  assert.equal(save.disabled, false);
  form.emit('submit');
  await settle();
  assert.deepEqual(writes[0], {action: 'signup', address: config.address,
    locale: 'en', surface: 'web', topics: ['offers'], version: config.copyVersion});
});

test('saved topics load, unsubscribe all clears them, and switching accounts drops old responses', async () => {
  globalThis.document = {createElement: element};
  const writes = [];
  let delay = false, release;
  const {root, form, boxes, selectAll, select} = setup(async input => {
    if (input.action === 'config') return config;
    if (input.action === 'status') {
      if (delay) return new Promise(resolve => { release = resolve; });
      return {status: 'active', topics: ['news', 'community'], topicsRevision: 'old'};
    }
    writes.push(input);
    return {status: 'unsubscribed', topics: []};
  });
  select(true);
  root.open = true;
  root.emit('toggle');
  await settle();
  assert.deepEqual(boxes.map(box => box.checked), [true, false, true]);
  assert.equal(selectAll.hidden, true);
  form.querySelector('[data-email-unsubscribe]').emit('click');
  await settle();
  assert.deepEqual(writes, [{action: 'unsubscribe'}]);
  assert.deepEqual(boxes.map(box => box.checked), [false, false, false]);
  delay = true;
  root.emit('toggle');
  await settle();
  select(false);
  release({status: 'active', address: 'previous@example.invalid', topics: ['news']});
  await settle();
  assert.equal(root.hidden, true);
  assert.equal(root.querySelector('[data-email-address]').textContent, '');
  assert.equal(form.hidden, true);
});

test('explicit unsubscribe is confirmed even when delivery was suppressed', async () => {
  globalThis.document = {createElement: element};
  const labels = [
    ['en', 'Email delivery is paused.', 'You’re unsubscribed from all Acadie marketing.'],
    ['fr-CA', 'Les envois sont suspendus.', 'Vous êtes désabonné de tous les courriels promotionnels d’Acadie.'],
  ];
  for (const [locale, paused, unsubscribed] of labels) {
    let row = {status: 'active', suppressed: true, topics: ['news'], topicsRevision: 'before'};
    const {root, form, select} = setup(async input => {
      if (input.action === 'config') return config;
      if (input.action === 'status') return row;
      assert.equal(input.action, 'unsubscribe');
      row = {...row, status: 'unsubscribed', topics: [], topicsRevision: 'after'};
      return row;
    }, locale);
    select(true);
    root.open = true;
    root.emit('toggle');
    await settle();
    const status = root.querySelector('[role="status"]');
    const unsubscribe = form.querySelector('[data-email-unsubscribe]');
    assert.equal(status.textContent, paused);
    unsubscribe.emit('click');
    await settle();
    assert.equal(status.textContent, unsubscribed);
    assert.equal(unsubscribe.hidden, true);
    root.emit('toggle');
    await settle();
    assert.equal(status.textContent, unsubscribed);
  }
});

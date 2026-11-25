const topicLabels = {
  en: {news: 'Acadie news and stories', offers: 'Offers', community: 'Community events and fundraisers'},
  'fr-CA': {news: 'Nouvelles et histoires d’Acadie', offers: 'Offres', community: 'Événements communautaires et collectes de fonds'},
};
const words = {
  en: {
    topics: 'Email topics', selectAll: 'Select all three', loading: 'Loading email preferences…',
    unavailable: 'Email preferences are unavailable. Try again.',
    consent: 'By choosing topics, I agree to receive the selected marketing emails from MapleTrail Software Inc. about Acadie.',
    empty: 'Choose the Acadie emails you want to receive.',
    active: 'Manage the Acadie emails you receive.', pending: 'Check your inbox and confirm your email address.',
    unsubscribed: 'You’re unsubscribed from all Acadie marketing.',
    suppressed: 'Email delivery is paused.',
    noAddress: 'To sign up here, verify the email on your Acadie account. You can also use Email Preferences in the app.',
    save: 'Save topic choices', subscribe: 'Subscribe to selected topics', unsubscribe: 'Unsubscribe from all marketing',
    code: 'Confirmation code', claim: 'Connect my subscription',
    changed: 'Your choices changed elsewhere. Review them and try again.',
  },
  'fr-CA': {
    topics: 'Sujets des courriels', selectAll: 'Choisir les trois sujets', loading: 'Chargement des préférences de courriel…',
    unavailable: 'Les préférences de courriel sont indisponibles. Réessayez.',
    consent: 'En choisissant des sujets, j’accepte de recevoir les courriels promotionnels sélectionnés de MapleTrail Software Inc. au sujet d’Acadie.',
    empty: 'Choisissez les courriels d’Acadie que vous souhaitez recevoir.',
    active: 'Gérez les courriels d’Acadie que vous recevez.', pending: 'Vérifiez votre boîte de réception et confirmez votre adresse courriel.',
    unsubscribed: 'Vous êtes désabonné de tous les courriels promotionnels d’Acadie.',
    suppressed: 'Les envois sont suspendus.',
    noAddress: 'Pour vous inscrire ici, vérifiez l’adresse de votre compte Acadie. Vous pouvez aussi utiliser les préférences de courriel dans l’application.',
    save: 'Enregistrer mes choix', subscribe: 'S’abonner aux sujets sélectionnés',
    unsubscribe: 'Se désabonner de tous les courriels promotionnels',
    code: 'Code de confirmation', claim: 'Relier mon abonnement',
    changed: 'Vos choix ont changé ailleurs. Vérifiez-les et réessayez.',
  },
};

export function mountEmailPreferences(root, locale, call) {
  const copy = words[locale];
  const form = root.querySelector('form');
  const status = root.querySelector('[role="status"]');
  const address = root.querySelector('[data-email-address]');
  const fieldset = form.querySelector('fieldset');
  const save = form.querySelector('button[type="submit"]');
  const unsubscribe = form.querySelector('[data-email-unsubscribe]');
  const claim = form.querySelector('[data-email-claim]');
  const code = form.querySelector('input[type="text"]');
  const recovery = form.querySelector('[data-email-recovery]');
  const senderInfo = form.querySelector('[data-email-sender]');
  const senderName = senderInfo.querySelector('[data-email-sender-name]');
  const mailing = senderInfo.querySelector('[data-email-sender-address]');
  const privacy = senderInfo.querySelector('[data-email-privacy]');
  const contact = senderInfo.querySelector('[data-email-contact]');
  const selectAll = document.createElement('button');
  selectAll.type = 'button';
  selectAll.className = 'button secondary';
  selectAll.hidden = true;
  selectAll.textContent = copy.selectAll;
  fieldset.append(selectAll);
  const boxes = Object.entries(topicLabels[locale]).map(([id, title]) => {
    const label = document.createElement('label');
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.value = id;
    label.append(input, ' ' + title);
    fieldset.append(label);
    return input;
  });
  fieldset.querySelector('legend').textContent = copy.topics;
  form.querySelector('[data-email-consent]').textContent = copy.consent;
  unsubscribe.textContent = copy.unsubscribe;
  code.parentElement.append(' ' + copy.code);
  claim.textContent = copy.claim;

  let session = false, generation = 0, config, row, hasStatus = false, pending = false, busy = false;
  const topics = () => boxes.filter(input => input.checked).map(input => input.value);
  const sameTopics = () => topics().join() === (row?.topics ?? []).join();
  function controls() {
    const active = hasStatus && row?.status === 'active';
    const canEnroll = Boolean(config?.enabled && config.address && !senderInfo.hidden);
    const canEdit = hasStatus && (active || (canEnroll && !pending));
    fieldset.hidden = !canEdit;
    fieldset.disabled = busy;
    selectAll.hidden = active || !canEdit;
    selectAll.disabled = busy || boxes.every(input => input.checked);
    for (const input of boxes) {
      input.disabled = (!config?.enabled || senderInfo.hidden) && !(row?.topics ?? []).includes(input.value);
    }
    form.querySelector('[data-email-consent]').hidden = !canEdit;
    save.hidden = !canEdit;
    save.disabled = busy || (active ? sameTopics() : topics().length === 0);
    save.textContent = active ? copy.save : copy.subscribe;
    unsubscribe.hidden = !active;
    unsubscribe.disabled = busy;
    recovery.hidden = !hasStatus || active || !config?.address;
    claim.disabled = busy || code.value.trim().length !== 131;
  }
  function render() {
    root.hidden = !config?.available;
    form.hidden = !config?.available;
    const sender = config?.sender;
    senderName.textContent = sender?.name ?? '';
    mailing.textContent = sender?.mailing ?? '';
    senderInfo.hidden = !senderName.textContent || !mailing.textContent ||
      !/^https:\/\//.test(sender?.privacy ?? '') || !/^[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+$/.test(sender?.contact ?? '');
    if (!senderInfo.hidden) {
      privacy.href = sender.privacy;
      contact.href = 'mailto:' + sender.contact;
    }
    address.textContent = row?.address ?? config?.address ?? '';
    for (const input of boxes) input.checked = (row?.topics ?? []).includes(input.value);
    status.textContent = !config?.available ? copy.unavailable : pending ? copy.pending :
      row?.suppressed && row.status !== 'unsubscribed' ? copy.suppressed :
        copy[row?.status] ?? (config.address ? copy.empty : copy.noAddress);
    controls();
  }
  async function run(action) {
    if (busy || !session) return;
    const generationAtStart = generation;
    busy = true;
    controls();
    try {
      const result = await action();
      if (generationAtStart !== generation) return;
      if (result) {
        row = result;
        pending = result.status === 'pending';
        if (!pending) code.value = '';
      }
      render();
    } catch (error) {
      if (generationAtStart !== generation) return;
      if (error.message === 'aborted') {
        try {
          const latest = await call({action: 'status'});
          if (generationAtStart !== generation) return;
          row = latest;
          render();
        } catch { /* The next visit can retry. */ }
      }
      if (generationAtStart === generation) status.textContent = error.message === 'aborted' ? copy.changed : copy.unavailable;
    } finally {
      if (generationAtStart === generation) {
        busy = false;
        controls();
      }
    }
  }
  function load() {
    return run(async () => {
      const expected = generation;
      hasStatus = false;
      status.textContent = copy.loading;
      const settings = await call({action: 'config'});
      if (expected !== generation) return;
      config = settings;
      if (!settings.available || !root.open) return null;
      const subscription = await call({action: 'status'});
      if (expected !== generation) return;
      hasStatus = true;
      return subscription;
    });
  }
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (save.disabled || save.hidden) return;
    const active = row?.status === 'active';
    void run(() => call({action: active ? 'topics' : 'signup', surface: 'web', locale,
      topics: topics(), version: config.copyVersion, ...(active ? {revision: row.topicsRevision} : {address: config.address})}));
  });
  selectAll.addEventListener('click', () => {
    if (selectAll.hidden || selectAll.disabled) return;
    for (const input of boxes) input.checked = true;
    controls();
  });
  unsubscribe.addEventListener('click', () => {
    if (!unsubscribe.hidden) void run(() => call({action: 'unsubscribe'}));
  });
  claim.addEventListener('click', () => {
    if (!recovery.hidden && !claim.disabled) void run(() => call({action: 'claim', code: code.value.trim()}));
  });
  code.addEventListener('input', controls);
  for (const box of boxes) box.addEventListener('change', controls);
  root.addEventListener('toggle', () => { if (root.open && session) void load(); });
  return signedIn => {
    generation++;
    session = signedIn;
    busy = false;
    config = undefined;
    row = undefined;
    hasStatus = false;
    pending = false;
    code.value = '';
    root.open = false;
    root.hidden = true;
    form.hidden = true;
    address.textContent = '';
    status.textContent = '';
    for (const input of boxes) input.checked = false;
    controls();
    if (signedIn) void load();
  };
}

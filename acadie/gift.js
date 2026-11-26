import {openAcadieAccount, signIntoAcadie} from './account-client.js';
import {giftConfig} from './gift-config.js';

const french = document.documentElement.lang === 'fr-CA';
const locale = french ? 'fr-CA' : 'en';
const words = french ? {
  unavailable: 'Les cadeaux Acadie+ ne sont pas offerts pour le moment.',
  price: (amount, tax) => amount + (tax ? ' pour un an, taxes en sus' : ' pour un an'),
  salesPaused: 'Les achats de cadeaux sont suspendus. Vous pouvez utiliser un cadeau déjà reçu.',
  returned: 'Votre cadeau vous sera envoyé par courriel après la confirmation du paiement.',
  canceled: 'Vous pouvez reprendre le paiement quand vous voulez.',
  checkout: 'Ouverture de la page de paiement sécurisée…',
  checkoutFailed: 'Impossible d’ouvrir la page de paiement. Réessayez.',
  login: 'Connectez-vous avec le compte que vous utilisez dans Acadie.',
  loginFailed: 'La connexion a échoué. Réessayez.',
  claim: 'Enregistrement de votre cadeau…',
  pending: 'L’enregistrement est en cours. Consultez cette page de nouveau dans quelques minutes.',
  queued: 'Cadeau enregistré. L’année offerte commencera automatiquement à la fin de votre accès actuel à Acadie+.',
  occupied: 'Ce compte a déjà un cadeau en attente ou en cours. Conservez ce nouveau lien pour plus tard.',
  invalid: 'Ce cadeau ne peut pas être enregistré. Vérifiez le code ou communiquez avec l’assistance.',
  reversed: 'Ce cadeau ne peut pas être activé. Communiquez avec l’assistance.',
  retry: 'Attendez quelques secondes, puis réessayez.',
  failed: 'Impossible de confirmer l’enregistrement pour le moment. Réessayez.',
  redeemed: date => 'Votre cadeau Acadie+ est actif jusqu’au ' + date + '. Ouvrez Acadie et connectez-vous avec ce compte.',
  expired: 'La période d’accès offerte par ce cadeau a pris fin.',
} : {
  unavailable: 'Acadie+ gifts are currently unavailable.',
  price: (amount, tax) => amount + (tax ? ' for one year, plus applicable tax' : ' for one year'),
  salesPaused: 'Gift purchases are paused. You can still redeem a gift you already received.',
  returned: 'We’ll email the gift to you after your payment is confirmed.',
  canceled: 'You can return to checkout whenever you’re ready.',
  checkout: 'Opening secure checkout…',
  checkoutFailed: 'Couldn’t open checkout. Please try again.',
  login: 'Sign in with the account you use in Acadie.',
  loginFailed: 'Sign-in failed. Please try again.',
  claim: 'Saving your gift…',
  pending: 'We’re still confirming your gift. Check this page again in a few minutes.',
  queued: 'Gift saved. Your gift year will start automatically when your current Acadie+ access ends.',
  occupied: 'This account already has a gift waiting or in use. Keep this new link for later.',
  invalid: 'This gift couldn’t be claimed. Check the code or contact support.',
  reversed: 'This gift couldn’t be claimed. Please contact support.',
  retry: 'Wait a few seconds and try again.',
  failed: 'Couldn’t confirm the gift. Please try again.',
  redeemed: date => 'Your Acadie+ gift is active through ' + date + '. Open Acadie and sign in with this account.',
  expired: 'The access period for this gift has ended.',
};

const root = document.querySelector('[data-gift]');
const purchaseStatus = root.querySelector('[data-gift-purchase-status]');
const claimStatus = root.querySelector('[data-gift-claim-status]');
const buy = root.querySelector('[data-gift-buy]');
const form = root.querySelector('form[data-gift-claim]');
const input = form.elements.code;
const claimButton = form.querySelector('button[type=submit]');
const signIn = root.querySelector('[data-gift-sign-in]');
const signOut = root.querySelector('[data-gift-sign-out]');
const accountLabel = root.querySelector('[data-gift-account]');
const preview = new URL(location.href);
const isCode = value => /^[A-Za-z0-9_-]{43}$/.test(value);

if (isCode(preview.hash.slice(1))) {
  input.value = preview.hash.slice(1);
  const alternate = document.querySelector('a[data-gift-language]');
  alternate.hash = preview.hash;
  preview.hash = '';
  root.querySelector('[data-gift-purchase]').hidden = true;
  root.querySelector('[data-gift-show-purchase]').hidden = false;
}
const checkoutReturn = preview.searchParams.get('checkout');
if (checkoutReturn !== null) preview.searchParams.delete('checkout');
history.replaceState(null, '', preview.pathname + preview.search);
root.querySelector('[data-gift-show-purchase]').addEventListener('click', event => {
  event.currentTarget.hidden = true;
  root.querySelector('[data-gift-purchase]').hidden = false;
});

let account, currentUser, outstandingOrder, accountEpoch = 0;
let claimController = new AbortController();

async function request(body, user, signal) {
  const [attestation, id] = await Promise.all([
    account.appCheckAPI.getToken(account.appCheck), user?.getIdToken(),
  ]);
  if (user && account.auth.currentUser?.uid !== user.uid) throw Error('account-changed');
  const response = await fetch(giftConfig.apiURL, {
    method: 'POST', credentials: 'omit', cache: 'no-store', redirect: 'error', referrerPolicy: 'no-referrer',
    signal, headers: {'Content-Type': 'application/json', 'X-Firebase-AppCheck': attestation.token,
      ...(id ? {Authorization: 'Bearer ' + id} : {})}, body: JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) throw Error(data.error);
  return data;
}

buy.addEventListener('click', async () => {
  buy.disabled = true;
  purchaseStatus.textContent = words.checkout;
  try {
    outstandingOrder ??= crypto.randomUUID();
    const result = await request({action: 'checkout', locale, orderID: outstandingOrder});
    const url = new URL(result.url);
    if (url.origin !== 'https://checkout.stripe.com' || url.username || url.password) throw Error();
    location.assign(url.href);
  } catch {
    purchaseStatus.textContent = words.checkoutFailed;
    buy.disabled = false;
  }
});

signIn.addEventListener('click', async event => {
  const button = event.target.closest('button[data-provider]');
  if (!button || !account || button.disabled) return;
  const buttons = signIn.querySelectorAll('button');
  for (const item of buttons) item.disabled = true;
  try { await signIntoAcadie(account.authAPI, account.auth, button.dataset.provider, french); }
  catch { claimStatus.textContent = words.loginFailed; }
  finally { for (const item of buttons) item.disabled = false; }
});

signOut.addEventListener('click', async () => {
  try { await account.authAPI.signOut(account.auth); }
  catch { claimStatus.textContent = words.loginFailed; }
});

function displayGift(data) {
  if (data.status === 'none') return;
  if (data.status === 'pending') claimStatus.textContent = words.pending;
  else if (data.status === 'queued') claimStatus.textContent = words.queued;
  else if (data.status === 'held') claimStatus.textContent = words.reversed;
  else if (data.status === 'redeemed' && Number.isSafeInteger(data.expiresAt)) {
    if (data.expiresAt <= Date.now()) claimStatus.textContent = words.expired;
    else claimStatus.textContent = words.redeemed(new Intl.DateTimeFormat(locale === 'en' ? 'en-CA' : locale,
      {dateStyle: 'long'}).format(data.expiresAt));
  } else throw Error();
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  if (!currentUser || claimButton.disabled) return;
  const code = input.value.trim();
  if (!isCode(code)) { claimStatus.textContent = words.invalid; return; }
  const epoch = accountEpoch;
  claimButton.disabled = true;
  claimStatus.textContent = words.claim;
  try {
    const data = await request({action: 'claim', code}, currentUser, claimController.signal);
    if (epoch !== accountEpoch) return;
    displayGift(data);
    if (data.status === 'queued' || data.status === 'redeemed') {
      input.value = '';
      document.querySelector('a[data-gift-language]').hash = '';
    }
  } catch (error) {
    if (epoch !== accountEpoch) return;
    claimStatus.textContent = ({
      'invalid-gift': words.invalid, 'gift-payment-reversed': words.reversed, 'gift-already-saved': words.occupied,
      'retry-later': words.retry, 'authentication-required': words.login,
    })[error.message] ?? words.failed;
  } finally {
    if (epoch === accountEpoch) claimButton.disabled = false;
  }
});

async function start() {
  if (!giftConfig.enabled) return;
  try {
    account = await openAcadieAccount(giftConfig, french);
    account.authAPI.onAuthStateChanged(account.auth, async user => {
      accountEpoch++;
      claimController.abort();
      claimController = new AbortController();
      currentUser = user;
      signIn.hidden = !!user;
      signOut.hidden = !user;
      form.hidden = !user;
      accountLabel.textContent = user?.email ?? '';
      claimButton.disabled = false;
      claimStatus.textContent = user ? '' : words.login;
      if (!user || input.value) return;
      const epoch = accountEpoch;
      try {
        const data = await request({action: 'status'}, user, claimController.signal);
        if (epoch === accountEpoch && !claimButton.disabled && !input.value && !claimStatus.textContent) displayGift(data);
      } catch {
        if (epoch === accountEpoch && !claimButton.disabled && !input.value && !claimStatus.textContent) {
          claimStatus.textContent = words.failed;
        }
      }
    });
    const price = await request({action: 'price'});
    if (price.currency !== 'CAD' || !Number.isSafeInteger(price.amountMinor) || price.amountMinor <= 0) throw Error();
    const amount = new Intl.NumberFormat(locale === 'en' ? 'en-CA' : locale,
      {style: 'currency', currency: 'CAD', currencyDisplay: 'code'}).format(price.amountMinor / 100);
    buy.hidden = price.checkoutAvailable !== true;
    root.querySelector('[data-gift-price]').textContent = buy.hidden ? '' : words.price(amount, price.taxExclusive);
    purchaseStatus.textContent = checkoutReturn === 'returned' ? words.returned
      : buy.hidden ? words.salesPaused : checkoutReturn === 'canceled' ? words.canceled : '';
  } catch { purchaseStatus.textContent = words.unavailable; }
}
start();

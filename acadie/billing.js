import {billingConfig} from './billing-config.js';
import {acadieCallableURL, billingPresentation, createRefreshFence} from './billing-state.mjs?v=2';

const french = document.documentElement.lang === 'fr-CA';
const words = french ? {
  unavailable: 'Les abonnements sur le site ne sont pas encore offerts. Vous pouvez vous abonner dans l’application Acadie.',
  loading: 'Vérification de votre accès…',
  signedOut: 'Connectez-vous avec le même compte Apple ou Google que dans Acadie.',
  signedIn: 'Votre accès à Acadie+ est inactif. Choisissez un abonnement pour passer au paiement sécurisé avec Stripe.',
  billingHistory: 'Voir l’historique de facturation',
  manageSubscription: 'Gérer l’abonnement',
  active: 'Votre accès à Acadie+ est actif.',
  store: 'Gérez votre abonnement dans la boutique où vous l’avez acheté.',
  needsPayment: 'Votre abonnement nécessite une vérification. Gérez-le pour vérifier le paiement ou annuler les renouvellements.',
  verificationRequired: 'Ouvrez Acadie, connectez-vous à ce compte et restaurez vos achats pour vérifier votre abonnement avant d’en acheter un autre.',
  failed: 'Impossible de vérifier votre accès pour le moment. Réessayez avant de vous abonner.',
  loginFailed: 'La connexion n’a pas abouti. Réessayez avec le compte utilisé dans Acadie.',
  checkoutFailed: 'Impossible d’ouvrir le paiement. Aucun nouvel accès n’a été confirmé. Réessayez.',
  manageFailed: 'Impossible d’ouvrir le portail de facturation. Réessayez.',
  perMonth: 'par mois', perYear: 'par année', tax: 'Taxes en sus, s’il y a lieu.',
} : {
  unavailable: 'Website subscriptions are not available yet. You can subscribe in the Acadie app.',
  loading: 'Checking your access…',
  signedOut: 'Sign in with the same Apple or Google account you use in Acadie.',
  signedIn: 'You don’t have active Acadie+ access. Choose a plan to continue to Stripe’s secure checkout.',
  billingHistory: 'View billing history',
  manageSubscription: 'Manage subscription',
  active: 'Your Acadie+ access is active.',
  store: 'Manage your subscription in the store where you purchased it.',
  needsPayment: 'Your subscription needs attention. Manage it to check payment details or cancel renewals.',
  verificationRequired: 'Open Acadie, sign in to this account and restore purchases to verify your subscription before buying another one.',
  failed: 'Your access could not be checked right now. Try again before subscribing.',
  loginFailed: 'Sign-in did not finish. Try again with the account you use in Acadie.',
  checkoutFailed: 'Checkout could not be opened. No new access has been confirmed. Please try again.',
  manageFailed: 'The billing portal could not be opened. Please try again.',
  perMonth: 'per month', perYear: 'per year', tax: 'Plus applicable taxes.',
};

const root = document.querySelector('[data-billing]');
const status = root.querySelector('[data-status]');
const signedOut = root.querySelector('[data-signed-out]');
const signedIn = root.querySelector('[data-signed-in]');
const plans = root.querySelector('[data-plans]');
const subscriptionActions = root.querySelector('[data-subscription-actions]');
const management = root.querySelector('[data-management]');
const cancellation = root.querySelector('[data-cancellation]');
const storeNote = root.querySelector('[data-store-note]');
const accountLabel = root.querySelector('[data-account-label]');
const buttons = [...root.querySelectorAll('button')].filter(button => !button.closest('[data-email-preferences]'));
let epoch = 0, currentUser = null, authAPI, auth, appCheckAPI, appCheck;
let busy = false, accessKnown = false, controller = new AbortController();
const refreshFence = createRefreshFence();
let setEmailSession = () => {};
const emailRoot = root.querySelector('[data-email-preferences]');
if (emailRoot) {
  import('./email-preferences.mjs').then(({mountEmailPreferences}) => {
    setEmailSession = mountEmailPreferences(emailRoot, french ? 'fr-CA' : 'en',
      body => call('acadieEmailPreferences', body, epoch));
    setEmailSession(Boolean(currentUser));
  }).catch(() => { /* Optional preferences cannot prevent account or checkout startup. */ });
}

function setBusy(value) {
  busy = value;
  root.setAttribute('aria-busy', String(value));
  for (const button of buttons) button.disabled = value;
}
function clearAccess() {
  accessKnown = false;
  plans.hidden = true;
  subscriptionActions.hidden = true;
  cancellation.hidden = true;
  storeNote.hidden = true;
  storeNote.textContent = '';
}
function safeRedirect(value, purpose) {
  const url = new URL(value);
  const hosts = purpose === 'checkout' ? ['checkout.stripe.com']
    : ['billing.stripe.com', 'link.com', 'www.link.com'];
  if (url.protocol !== 'https:' || !hosts.includes(url.hostname)
      || url.username || url.password || url.port) throw Error('invalid-redirect');
  // Do not disclose this site's URL or any callback query to the payment service.
  const anchor = document.createElement('a');
  anchor.href = url.href;
  anchor.rel = 'noreferrer';
  anchor.referrerPolicy = 'no-referrer';
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
}
async function call(action, body, expectedEpoch) {
  const user = currentUser;
  if (!user || auth.currentUser?.uid !== user.uid) throw Error('authentication-required');
  const [idToken, attestation] = await Promise.all([
    user.getIdToken(), appCheckAPI.getToken(appCheck),
  ]);
  if (epoch !== expectedEpoch || auth.currentUser?.uid !== user.uid) throw Error('account-changed');
  const response = await fetch(acadieCallableURL(billingConfig, action), {
    method: 'POST', credentials: 'omit', cache: 'no-store', redirect: 'error',
    referrerPolicy: 'no-referrer', signal: controller.signal,
    headers: {'Content-Type': 'application/json', Authorization: `Bearer ${idToken}`,
      'X-Firebase-AppCheck': attestation.token},
    body: JSON.stringify(action === 'acadieEmailPreferences' ? {data: body} : body),
  });
  if (epoch !== expectedEpoch || auth.currentUser?.uid !== user.uid) throw Error('account-changed');
  if (action === 'acadieEmailPreferences') {
    const payload = await response.json();
    if (epoch !== expectedEpoch) throw Error('account-changed');
    if (!response.ok || !payload.result) throw Error(payload.error?.status === 'ABORTED' ? 'aborted' : 'email-unavailable');
    return payload.result;
  }
  if (!response.ok) throw Error('billing-unavailable');
  const data = await response.json();
  if (epoch !== expectedEpoch) throw Error('account-changed');
  return data;
}
function renderAccess(data) {
  const presentation = billingPresentation(data);
  clearAccess();
  if (presentation.managementLabel) {
    management.textContent = words[presentation.managementLabel];
    management.classList.toggle('secondary', presentation.managementLabel === 'billingHistory');
    subscriptionActions.hidden = false;
  }
  cancellation.hidden = !presentation.showCancellation;
  status.textContent = words[presentation.message];
  if (data.active) {
    if (['apple', 'google'].includes(data.billingSource)) {
      storeNote.textContent = words.store;
      storeNote.hidden = false;
    }
  } else if (presentation.showPlans) {
    const formatter = new Intl.NumberFormat(french ? 'fr-CA' : 'en-CA', {
      style: 'currency', currency: data.currency, currencyDisplay: 'code',
    });
    for (const plan of ['monthly', 'annual']) {
      const item = data.plans.find(row => row.id === plan);
      if (!item || !Number.isSafeInteger(item.amountMinor) || item.amountMinor <= 0) throw Error('invalid-plan');
      root.querySelector(`[data-price="${plan}"]`).textContent = formatter.format(item.amountMinor / 100);
    }
    plans.hidden = false;
  }
  accessKnown = true;
}
async function refreshAccess(expectedEpoch = epoch) {
  const refreshToken = refreshFence.begin();
  const current = () => epoch === expectedEpoch && refreshFence.accepts(refreshToken);
  clearAccess();
  status.textContent = words.loading;
  setBusy(true);
  try {
    const data = await call('getAcadieWebBilling', {}, expectedEpoch);
    if (current()) renderAccess(data);
  } catch {
    if (current()) { clearAccess(); status.textContent = words.failed; }
  } finally {
    if (current()) setBusy(false);
  }
}

root.querySelector('[data-refresh]').addEventListener('click', () => {
  if (!busy && currentUser) refreshAccess();
});
for (const button of root.querySelectorAll('[data-checkout]')) button.addEventListener('click', async () => {
  if (busy || !accessKnown || plans.hidden || !currentUser) return;
  const expectedEpoch = epoch;
  setBusy(true);
  try {
    const result = await call('createAcadieWebCheckout', {plan: button.dataset.checkout,
      locale: french ? 'fr-CA' : 'en', returnPath: location.pathname}, expectedEpoch);
    if (epoch === expectedEpoch) safeRedirect(result.url, 'checkout');
  } catch {
    if (epoch === expectedEpoch) { clearAccess(); status.textContent = words.checkoutFailed; }
  } finally { if (epoch === expectedEpoch) setBusy(false); }
});
for (const button of [management, cancellation]) button.addEventListener('click', async () => {
  if (busy || !accessKnown || subscriptionActions.hidden || button.hidden || !currentUser) return;
  const expectedEpoch = epoch;
  setBusy(true);
  try {
    const result = await call('createAcadieWebManagement', {returnPath: location.pathname,
      intent: button === cancellation ? 'cancel' : 'manage'}, expectedEpoch);
    if (epoch === expectedEpoch) safeRedirect(result.url, 'management');
  } catch { if (epoch === expectedEpoch) status.textContent = words.manageFailed; }
  finally { if (epoch === expectedEpoch) setBusy(false); }
});
root.querySelector('[data-sign-out]').addEventListener('click', async () => {
  if (busy) return;
  await authAPI.signOut(auth);
});
for (const button of root.querySelectorAll('[data-sign-in]')) button.addEventListener('click', async () => {
  if (busy || !authAPI) return;
  const provider = button.dataset.signIn === 'apple'
    ? new authAPI.OAuthProvider('apple.com') : new authAPI.GoogleAuthProvider();
  provider.setCustomParameters(button.dataset.signIn === 'apple'
    ? {locale: french ? 'fr_CA' : 'en_CA'} : {prompt: 'select_account'});
  setBusy(true);
  const expectedEpoch = epoch;
  try { await authAPI.signInWithPopup(auth, provider); }
  catch {
    if (epoch === expectedEpoch) { status.textContent = words.loginFailed; setBusy(false); }
  }
  // onAuthStateChanged starts and owns the next access refresh. Completing the
  // popup must not make that newer asynchronous verification interactive.
});

async function start() {
  signedOut.hidden = true;
  signedIn.hidden = true;
  clearAccess();
  if (!billingConfig.enabled || !billingConfig.firebase || !billingConfig.appCheckSiteKey) {
    status.textContent = words.unavailable;
    return;
  }
  try {
    const sdk = 'https://www.gstatic.com/firebasejs/13.4.0';
    const appAPI = await import(`${sdk}/firebase-app.js`);
    [authAPI, appCheckAPI] = await Promise.all([
      import(`${sdk}/firebase-auth.js`), import(`${sdk}/firebase-app-check.js`),
    ]);
    const app = appAPI.initializeApp(billingConfig.firebase);
    appCheck = appCheckAPI.initializeAppCheck(app, {
      provider: new appCheckAPI.ReCaptchaEnterpriseProvider(billingConfig.appCheckSiteKey),
      isTokenAutoRefreshEnabled: true,
    });
    auth = authAPI.getAuth(app);
    auth.languageCode = french ? 'fr' : 'en';
    authAPI.onAuthStateChanged(auth, user => {
      epoch++;
      refreshFence.invalidate();
      controller.abort(); controller = new AbortController();
      currentUser = user;
      clearAccess();
      signedOut.hidden = !!user;
      signedIn.hidden = !user;
      accountLabel.textContent = user?.email ?? '';
      setEmailSession(Boolean(user));
      if (user) refreshAccess(epoch);
      else { status.textContent = words.signedOut; setBusy(false); }
    });
  } catch { status.textContent = words.failed; }
}
start();

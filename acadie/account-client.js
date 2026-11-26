export async function openAcadieAccount(config, french) {
  const sdk = 'https://www.gstatic.com/firebasejs/13.4.0';
  const [appAPI, authAPI, appCheckAPI] = await Promise.all([
    import(sdk + '/firebase-app.js'), import(sdk + '/firebase-auth.js'), import(sdk + '/firebase-app-check.js'),
  ]);
  const app = appAPI.initializeApp(config.firebase);
  const appCheck = appCheckAPI.initializeAppCheck(app, {
    provider: new appCheckAPI.ReCaptchaEnterpriseProvider(config.appCheckSiteKey),
    isTokenAutoRefreshEnabled: true,
  });
  const auth = authAPI.getAuth(app);
  auth.languageCode = french ? 'fr' : 'en';
  return {auth, appCheck, authAPI, appCheckAPI};
}

export function signIntoAcadie(authAPI, auth, providerName, french) {
  const provider = providerName === 'apple' ? new authAPI.OAuthProvider('apple.com') : new authAPI.GoogleAuthProvider();
  provider.setCustomParameters(providerName === 'apple' ? {locale: french ? 'fr_CA' : 'en_CA'} : {prompt: 'select_account'});
  return authAPI.signInWithPopup(auth, provider);
}

import {billingConfig} from './billing-config.js';

export const giftConfig = Object.freeze(billingConfig.enabled && billingConfig.giftEnabled
  && billingConfig.firebase?.projectId === 'acadie-19d53' && billingConfig.appCheckSiteKey ? {
  enabled: true,
  firebase: billingConfig.firebase,
  appCheckSiteKey: billingConfig.appCheckSiteKey,
  apiURL: 'https://us-central1-acadie-19d53.cloudfunctions.net/acadieGiftWebsite',
} : {enabled: false});

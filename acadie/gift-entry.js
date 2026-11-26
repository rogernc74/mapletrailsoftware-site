import {giftConfig} from './gift-config.js';

if (giftConfig.enabled) {
  for (const link of document.querySelectorAll('[data-gifts-link]')) link.hidden = false;
}

console.log('[novdan] background started');

browser.browserAction.setBadgeText({ text: '?' });
browser.browserAction.setBadgeBackgroundColor({ color: '#fd0' });

const SETTINGS = {
  access_token: null,
  refresh_token: null,
  wallet_id: null,
  active_subscription: null,
};

// Load settings from storage
browser.storage.sync.get(SETTINGS).then((settings) => {
  Object.keys(settings).forEach((key) => {
    SETTINGS[key] = settings[key];
  });
  updateStatus();
});

// Listen to changes in storage
browser.storage.onChanged.addListener((changes, area) => {
  let hasChanges = false;
  if (area === 'sync') {
    Object.keys(changes).forEach((key) => {
      const { oldValue, newValue } = changes[key];
      if (SETTINGS[key] !== newValue) {
        SETTINGS[key] = newValue;
        hasChanges = true;
      }
    });
  }
  if (hasChanges) {
    updateStatus();
  }
});

// Open tab on install
browser.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    browser.tabs.create({ url: 'https://novdan.si/dash' });
  }
});

// Open tab on toolbar icon click
browser.browserAction.onClicked.addListener((tab) => {
  browser.tabs.create({ url: 'https://novdan.si/dash' });
});

async function fetchStatus() {
  return {
    wallet: '5f7fb91b-5db9-41a7-9f19-78233ca5820e', // TODO
    active_subscription: true, // TODO:
  };
}

async function updateStatus() {
  try {
    const status = await fetchStatus();
    SETTINGS.wallet_id = status.wallet;
    SETTINGS.active_subscription = status.active_subscription;
    browser.storage.sync.set({
      wallet_id: status.wallet,
      active_subscription: status.active_subscription,
    });
  } catch (error) {
    SETTINGS.wallet_id = null;
    SETTINGS.active_subscription = null;
    browser.storage.sync.set({
      wallet_id: null,
      active_subscription: null,
    });
  }
  updateBadge();
}

function updateBadge() {
  if (SETTINGS.wallet_id && SETTINGS.active_subscription) {
    browser.browserAction.setBadgeText({ text: '✔' });
    browser.browserAction.setBadgeBackgroundColor({ color: '#0d0' });
  } else {
    browser.browserAction.setBadgeText({ text: '×' });
    browser.browserAction.setBadgeBackgroundColor({ color: '#d00' });
  }
}

console.log('Background started!');

browser.browserAction.setBadgeText({ text: '×' });
browser.browserAction.setBadgeBackgroundColor({ color: '#d00' });

const SETTINGS = {
  access_token: null,
  refresh_token: null,
};

// Load settings from storage
browser.storage.sync.get(SETTINGS).then((settings) => {
  Object.keys(settings).forEach((key) => {
    SETTINGS[key] = settings[key];
  });
  updateBadge();
});

// Listen to changes in storage
browser.storage.onChanged.addListener((changes, area) => {
  if (area === 'sync') {
    Object.keys(changes).forEach((key) => {
      SETTINGS[key] = changes[key].newValue;
    });
    updateBadge();
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

function updateBadge() {
  // browser.browserAction.setBadgeText({ text: '' });
  // browser.browserAction.setBadgeText({ text: '✔' });
  // browser.browserAction.setBadgeBackgroundColor({ color: '#0d0' });
}

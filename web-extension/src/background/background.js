console.log('Background started!');

browser.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    browser.tabs.create({ url: 'https://novdan.si/dash' });
  }
});

browser.browserAction.onClicked.addListener((tab) => {
  browser.tabs.create({ url: 'https://novdan.si/dash' });
});

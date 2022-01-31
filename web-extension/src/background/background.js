console.log('[novdan] background started');

browser.browserAction.setBadgeText({ text: '?' });
browser.browserAction.setBadgeBackgroundColor({ color: '#ddd' });

// const CLIENT_ID = 'Li03SQ542sSuIePdgKxw5XYRWLCPdCCgHweo1UVL';
// const API_URL_BASE = 'http://localhost:8000';
const CLIENT_ID = '1iOuBUL0JXbogMGDIpU0uC6lH52MqTkCOwj0qhKK';
const API_URL_BASE = 'https://denarnica.novdan.si';

const UPDATE_STATUS_INTERVAL_SECONDS = 60 * 60 * 24;

const SETTINGS = {
  access_token: null,
  refresh_token: null,
  username: null,
  wallet_id: null,
  active_subscription: null,
  fetch_status_timestamp: null,
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
  updateStatus();
  browser.tabs.create({ url: 'https://novdan.si/dash' });
});

async function refreshToken() {
  const formData = new FormData();
  formData.append('client_id', CLIENT_ID);
  formData.append('grant_type', 'refresh_token');
  formData.append('refresh_token', SETTINGS.refresh_token);

  const response = await fetch(`${API_URL_BASE}/o/token/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to refresh token!');
  }

  const data = await response.json();

  SETTINGS.access_token = data.access_token;
  SETTINGS.refresh_token = data.refresh_token;
  browser.storage.sync.set({
    access_token: data.access_token,
    refresh_token: data.refresh_token,
  });
}

async function fetchStatus(allowRefresh = true) {
  if (!SETTINGS.access_token) {
    throw new Error('No access token!');
  }

  const response = await fetch(`${API_URL_BASE}/api/status`, {
    headers: {
      Authorization: `Bearer ${SETTINGS.access_token}`,
    },
  });

  if (response.status === 401 && allowRefresh && SETTINGS.refresh_token) {
    try {
      await refreshToken();
    } catch (error) {
      return response;
    }
    return fetchStatus(false);
  }

  return response;
}

async function updateStatus() {
  try {
    const response = await fetchStatus();
    const status = await response.json();
    const timestamp = Date.now();
    SETTINGS.username = status.user.username;
    SETTINGS.wallet_id = status.wallet.id;
    SETTINGS.active_subscription = status.active_subscription;
    SETTINGS.fetch_status_timestamp = timestamp;
    browser.storage.sync.set({
      username: status.user.username,
      wallet_id: status.wallet.id,
      active_subscription: status.active_subscription,
      fetch_status_timestamp: timestamp,
    });
  } catch (error) {
    SETTINGS.username = null;
    SETTINGS.wallet_id = null;
    SETTINGS.active_subscription = null;
    browser.storage.sync.set({
      username: null,
      wallet_id: null,
      active_subscription: null,
    });
  }
  updateBadge();
}

function updateBadge() {
  let badgeText = '';
  let badgeColor = '';
  const badgeTooltip = ['nov dan', ''];
  if (SETTINGS.username && SETTINGS.wallet_id) {
    badgeTooltip.push(`Uporabnik: ${SETTINGS.username}`);
    if (SETTINGS.active_subscription) {
      badgeText = '€';
      badgeColor = '#0d0';
      badgeTooltip.push('Naročnina: aktivna');
    } else {
      badgeText = '✔';
      badgeColor = '#f80';
      badgeTooltip.push('Naročnina: ni aktivna');
    }
  } else {
    badgeText = '×';
    badgeColor = '#d00';
    badgeTooltip.push('Prijava ni uspela');
  }
  browser.browserAction.setBadgeText({ text: badgeText });
  browser.browserAction.setBadgeBackgroundColor({ color: badgeColor });
  browser.browserAction.setTitle({ title: badgeTooltip.join('\n') });
}

// Update status periodically
setInterval(async () => {
  updateStatus();
}, UPDATE_STATUS_INTERVAL_SECONDS * 1000);

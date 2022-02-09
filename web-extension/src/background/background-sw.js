console.log('[novdan] background-sw started');

chrome.action.setBadgeText({ text: '?' });
chrome.action.setBadgeBackgroundColor({ color: '#ddd' });

const CLIENT_ID = 'Li03SQ542sSuIePdgKxw5XYRWLCPdCCgHweo1UVL';
const API_URL_BASE = 'http://localhost:8000';
// const CLIENT_ID = '1iOuBUL0JXbogMGDIpU0uC6lH52MqTkCOwj0qhKK';
// const API_URL_BASE = 'https://denarnica.novdan.si';

const UPDATE_STATUS_INTERVAL_SECONDS = 60 * 60 * 24;

// update status immediately on load
updateStatus();

// Listen to changes in storage
chrome.storage.onChanged.addListener((changes, area) => {
  let hasChanges = false;
  if (area === 'sync') {
    Object.keys(changes).forEach((key) => {
      const { oldValue, newValue } = changes[key];
      console.log(oldValue, newValue)
      if (oldValue !== newValue) {
        hasChanges = true;
      }
    });
  }
  if (hasChanges) {
    updateStatus();
  }
});

// Open tab on install
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    chrome.tabs.create({ url: 'https://novdan.si/dash' });
  }
});

// Open tab on toolbar icon click
chrome.action.onClicked.addListener((tab) => {
  updateStatus();
  chrome.tabs.create({ url: 'https://novdan.si/dash' });
});

async function refreshToken() {
  const { refresh_token } = await chrome.storage.sync.get(null);

  const formData = new FormData();
  formData.append('client_id', CLIENT_ID);
  formData.append('grant_type', 'refresh_token');
  formData.append('refresh_token', refresh_token);

  const response = await fetch(`${API_URL_BASE}/o/token/`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to refresh token!');
  }

  const data = await response.json();

  browser.storage.sync.set({
    access_token: data.access_token,
    refresh_token: data.refresh_token,
  });
}

async function fetchStatus(allowRefresh = true) {
  const { access_token, refresh_token } = await chrome.storage.sync.get(null);

  if (!access_token) {
    throw new Error('No access token!');
  }

  const response = await fetch(`${API_URL_BASE}/api/status`, {
    headers: {
      Authorization: `Bearer ${access_token}`,
    },
  });

  if (response.status === 401 && allowRefresh && refresh_token) {
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
  console.log('called updateStatus');
  try {
    const response = await fetchStatus();
    const status = await response.json();
    chrome.storage.sync.set({
      username: status.user.username,
      wallet_id: status.wallet.id,
      active_subscription: status.active_subscription,
    });
  } catch (error) {
    console.log('failed updateStatus', error);
    chrome.storage.sync.set({
      username: null,
      wallet_id: null,
      active_subscription: null,
    });
  }
  updateBadge();
}

async function updateBadge() {
  const { username, wallet_id, active_subscription } =
    await chrome.storage.sync.get(null);

  let badgeText = '';
  let badgeColor = '';
  const badgeTooltip = ['nov dan', ''];
  if (username && wallet_id) {
    badgeTooltip.push(`Uporabnik: ${username}`);
    if (active_subscription) {
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
  chrome.action.setBadgeText({ text: badgeText });
  chrome.action.setBadgeBackgroundColor({ color: badgeColor });
  chrome.action.setTitle({ title: badgeTooltip.join('\n') });
}
/*
// Update status periodically
setInterval(async () => {
  updateStatus();
}, UPDATE_STATUS_INTERVAL_SECONDS * 1000);
*/

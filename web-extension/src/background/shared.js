console.log('[novdan] background shared started');

// GLOBALS
// -----------------------------------------------------------------------------
export const UPDATE_STATUS_PERIOD_MINUTES = 60 * 6; // every 6 hours

const CLIENT_ID = 'Li03SQ542sSuIePdgKxw5XYRWLCPdCCgHweo1UVL';
const API_URL_BASE = 'http://localhost:8000';
// const CLIENT_ID = '1iOuBUL0JXbogMGDIpU0uC6lH52MqTkCOwj0qhKK';
// const API_URL_BASE = 'https://denarnica.novdan.si';
// -----------------------------------------------------------------------------

// global `chrome` should be defined (firefox supports it for compatibility)
if (typeof chrome === 'undefined') {
  throw new Error('`chrome` is not defined!');
}

// In chrome manifest v3 it's `chrome.action` otherwise `chrome.browserAction`
if (!chrome.action) {
  chrome.action = chrome.browserAction;
}

// Set default badge, before we know any status
chrome.action.setBadgeText({ text: '?' });
chrome.action.setBadgeBackgroundColor({ color: '#999' });

// Listen to changes in storage
chrome.storage.onChanged.addListener((changes, area) => {
  let hasChanges = false;
  if (area === 'sync') {
    Object.keys(changes).forEach((key) => {
      const { oldValue, newValue } = changes[key];
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
  chrome.tabs.create({ url: 'https://novdan.si/dash' });
});

// FIXME: this is a temporary check for promise support
// -----------------------------------------------------------------------------
{
  const setReturnValue = chrome.storage.sync.set({});
  if (!setReturnValue || !setReturnValue.then) {
    throw new Error('`chrome` storage `set` does not return a promise!');
  }
  const getReturnValue = chrome.storage.sync.get({});
  if (!getReturnValue || !getReturnValue.then) {
    throw new Error('`chrome` storage `get` does not return a promise!');
  }
}
// -----------------------------------------------------------------------------

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

  await chrome.storage.sync.set({
    access_token: data.access_token,
    refresh_token: data.refresh_token,
  });
}

async function apiFetch(urlPath, allowRefresh = true) {
  const { access_token, refresh_token } = await chrome.storage.sync.get(null);

  if (!access_token) {
    throw new Error('No access token!');
  }

  const response = await fetch(`${API_URL_BASE}${urlPath}`, {
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
    return apiFetch(urlPath, false);
  }

  return response;
}

async function fetchStatus() {
  const response = await apiFetch('/api/status');
  return response.json();
}

export async function updateStatus() {
  console.log('[novdan] called updateStatus');
  try {
    const status = await fetchStatus();
    await chrome.storage.sync.set({
      username: status.user.username,
      wallet_id: status.wallet.id,
      active_subscription: status.active_subscription,
    });
  } catch (error) {
    console.log('[novdan] failed updateStatus', error);
    await chrome.storage.sync.set({
      username: null,
      wallet_id: null,
      active_subscription: null,
    });
  }
  console.log('[novdan] finished updateStatus');
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

// Update status immediately on load
updateStatus();

// Set up alarm to update status every X minutes
chrome.alarms.create('update-status-interval', {
  periodInMinutes: UPDATE_STATUS_PERIOD_MINUTES,
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'update-status-interval') {
    updateStatus();
  }
});

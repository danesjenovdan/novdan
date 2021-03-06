console.log('[novdan] content script started');

/**
 * Load a script in full page context.
 *
 * Content scripts run in a sandbox with limited access to page, but with extra
 * features like the `browser` extension api, so bypass the sandbox if needed.
 * Any communication between scripts can be done using `window.postMessage`.
 */
function loadScript(url) {
  const s = document.createElement('script');
  s.onload = () => s.remove();
  s.src = url;
  document.documentElement.appendChild(s);
}

loadScript(
  browser.runtime.getURL('/web_accessible_resources/monetization-polyfill.js')
);

// const CLIENT_ID = 'Li03SQ542sSuIePdgKxw5XYRWLCPdCCgHweo1UVL';
// const PAGE_ORIGIN = 'http://localhost:3000';
// const PAGE_HOSTNAME = 'localhost';
// const API_URL_BASE = 'http://localhost:8000';
// const API_HOSTNAME = 'localhost';
const CLIENT_ID = '1iOuBUL0JXbogMGDIpU0uC6lH52MqTkCOwj0qhKK';
const PAGE_ORIGIN = 'https://novdan.si';
const PAGE_HOSTNAME = 'novdan.si';
const API_URL_BASE = 'https://denarnica.novdan.si';
const API_HOSTNAME = 'denarnica.novdan.si';

const TESTING_HOSTNAMES = [
  'testwebmonetization.com',
  'localhost',
  '127.0.0.1',
  '0.0.0.0',
];

const PAYMENT_INTERVAL_SECONDS = 5;

const STATE = {
  isMonetized: false,
  paymentPointer: null,
  destinationWallet: null,
  monetizationState: 'stopped',
  requestId: null,
  isVisible: true,
  timerId: null,
  timerTimestamp: 0,
};

const SETTINGS = {
  access_token: null,
  refresh_token: null,
  username: null,
  wallet_id: null,
  active_subscription: null,
};

let tokenResponseChallenge = null;

// load settings from storage
browser.storage.sync.get(SETTINGS).then((settings) => {
  Object.keys(settings).forEach((key) => {
    SETTINGS[key] = settings[key];
  });
});

// listen to changes in storage
browser.storage.onChanged.addListener((changes, area) => {
  let hasChanges = false;
  let userChanged = false;
  let walletChanged = false;
  if (area === 'sync') {
    Object.keys(changes).forEach((key) => {
      const { oldValue, newValue } = changes[key];
      if (SETTINGS[key] !== newValue) {
        SETTINGS[key] = newValue;
        hasChanges = true;
        if (key === 'username') {
          userChanged = true;
        }
        if (key === 'wallet_id') {
          walletChanged = true;
        }
      }
    });
  }
  if (hasChanges) {
    // notify we logged in
    if (userChanged && tokenResponseChallenge) {
      const username = SETTINGS.username || 'null';
      const challenge = tokenResponseChallenge;
      tokenResponseChallenge = null;
      window.postMessage(
        {
          name: 'novdan',
          event: {
            type: 'extension:hello',
            detail: { encoded: btoa(`${username}:${challenge}`) },
          },
        },
        PAGE_ORIGIN
      );
      tokenResponseChallenge = null;
    }
    // restart monetization if wallet changed
    if (walletChanged && STATE.isMonetized) {
      const paymentPointer = STATE.paymentPointer;
      stopMonetization(paymentPointer);
      startMonetization(paymentPointer);
    }
  }
});

document.addEventListener('visibilitychange', onVisibilityChange, false);

function onVisibilityChange() {
  STATE.isVisible = document.visibilityState === 'visible';

  // tab just became visible and is monetized
  if (STATE.isVisible && STATE.isMonetized) {
    const timestamp = Date.now();
    const timeDiff = timestamp - STATE.timerTimestamp;
    // add 1.5sec; browsers throttle timers to 1/sec or 1/min when in background
    const maxDiff = PAYMENT_INTERVAL_SECONDS * 1000 + 1500;
    // last payment was more than 1.5sec behind schedule
    if (timeDiff > maxDiff) {
      // clear any old timers and start paying immediately
      clearTimeout(STATE.timerId);
      pay();
    }
  }
}

window.addEventListener('message', onMessage, false);

function onMessage(messageEvent) {
  // only accept messages from the current page
  if (messageEvent.source !== window && messageEvent.data) {
    return;
  }

  const { name, event } = messageEvent.data;

  // monetization polyfill events
  if (name === 'monetization' && event) {
    const { type, detail } = event;
    if (type === 'meta-tag-added') {
      onMetaTagAdded(detail);
    } else if (type === 'meta-tag-removed') {
      onMetaTagRemoved(detail);
    }
  }

  // novdan events
  if (name === 'novdan' && event) {
    const { type, detail } = event;
    if (type === 'page:hello') {
      onHelloFromPage(messageEvent.source, detail);
    } else if (type === 'page:connect') {
      onConnectFromPage(messageEvent.source, detail);
    } else if (type === 'page:logout') {
      onLogoutFromPage(messageEvent.source, detail);
    }
  }
}

function onMetaTagAdded({ content: paymentPointer }) {
  const url = getUrlFromPaymentPointer(paymentPointer);
  if (isValidPaymentUrl(url)) {
    if (STATE.paymentPointer && STATE.isMonetized) {
      stopMonetization(STATE.paymentPointer);
    }
    startMonetization(paymentPointer);
  }
}

function onMetaTagRemoved({ content: paymentPointer }) {
  const url = getUrlFromPaymentPointer(paymentPointer);
  if (isValidPaymentUrl(url)) {
    stopMonetization(paymentPointer);
  }
}

function onHelloFromPage(source, { encoded }) {
  if (source.location.hostname !== PAGE_HOSTNAME) {
    return;
  }

  const detail = {};
  try {
    const [username, walletEnding, challenge] = atob(encoded).split(':');
    if (
      username &&
      walletEnding &&
      SETTINGS.username &&
      SETTINGS.wallet_id &&
      username === SETTINGS.username &&
      walletEnding === SETTINGS.wallet_id.slice(-12)
    ) {
      detail.encoded = btoa(`${username}:${challenge}`);
    } else {
      detail.encoded = btoa(`null:${challenge}`);
    }
  } catch (error) {
    console.log('onHelloFromPage', error);
  }

  source.postMessage(
    {
      name: 'novdan',
      event: { type: 'extension:hello', detail },
    },
    PAGE_ORIGIN
  );
}

function onConnectFromPage(source, { encoded }) {
  if (source.location.hostname !== PAGE_HOSTNAME) {
    return;
  }

  const detail = {};
  try {
    const [accessToken, refreshToken, challenge] = atob(encoded).split(':');
    if (accessToken && refreshToken) {
      SETTINGS.access_token = accessToken;
      SETTINGS.refresh_token = refreshToken;
      SETTINGS.username = null;
      SETTINGS.wallet_id = null;
      SETTINGS.active_subscription = null;
      browser.storage.sync.set({
        access_token: accessToken,
        refresh_token: refreshToken,
        username: null,
        wallet_id: null,
        active_subscription: null,
      });
      tokenResponseChallenge = challenge;
      detail.encoded = btoa(`ack:${challenge}`);
    } else {
      tokenResponseChallenge = null;
      detail.encoded = btoa(`nak:${challenge}`);
    }
  } catch (error) {}

  source.postMessage(
    {
      name: 'novdan',
      event: { type: 'extension:connect', detail },
    },
    PAGE_ORIGIN
  );
}

function onLogoutFromPage(source, detail) {
  if (source.location.hostname !== PAGE_HOSTNAME) {
    return;
  }

  const token = SETTINGS.refresh_token || SETTINGS.access_token;
  if (token) {
    const formData = new FormData();
    formData.append('client_id', CLIENT_ID);
    formData.append('token', token);

    try {
      fetch(`${API_URL_BASE}/o/revoke_token/`, {
        method: 'POST',
        body: formData,
      });
    } catch (e) {}
  }

  SETTINGS.access_token = null;
  SETTINGS.refresh_token = null;
  SETTINGS.username = null;
  SETTINGS.wallet_id = null;
  SETTINGS.active_subscription = null;
  browser.storage.sync.set({
    access_token: null,
    refresh_token: null,
    username: null,
    wallet_id: null,
    active_subscription: null,
  });
}

function getUrlFromPaymentPointer(pp) {
  const ppUrl = pp.replace(/^\$/, 'https://');
  const url = new URL(ppUrl);
  if (url.pathname === '/') {
    url.pathname = '/.well-known/pay';
  }
  if (API_HOSTNAME === 'localhost') {
    return `${API_URL_BASE}${url.pathname}`;
  }
  return url;
}

function isValidPaymentUrl(url) {
  // for testing allow all
  if (TESTING_HOSTNAMES.includes(window.location.hostname)) {
    return true;
  }
  // otherwise only allow our wallet domain
  return url.hostname === API_HOSTNAME;
}

async function fetchSpsp4(url) {
  const acceptMimeTypes = ['application/spsp4+json', 'application/spsp+json'];
  const responseMimeTypes = [...acceptMimeTypes, 'application/json'];

  const response = await fetch(url, {
    headers: { Accept: acceptMimeTypes.join(',') },
  });

  const contentType = response.headers.get('content-type');
  if (response.status !== 200 || !responseMimeTypes.includes(contentType)) {
    console.log('[novdan] bad spsp4 response', response.status, contentType);
    return;
  }

  return response.json();
}

async function startMonetization(paymentPointer) {
  STATE.paymentPointer = paymentPointer;

  const url = getUrlFromPaymentPointer(paymentPointer);
  const json = await fetchSpsp4(url);
  if (!json || !json.destination_account) {
    return;
  }

  // check if destination account is supported
  const [scheme, ...segments] = json.destination_account.split('.');
  if (scheme === 'g' && segments.length >= 2 && segments[0] === 'novdan') {
    // get wallet id
    STATE.destinationWallet = segments[1];
    console.log('[novdan] got destination wallet', STATE.destinationWallet);

    // force update visibility
    STATE.isMonetized = false;
    onVisibilityChange();

    emitMonetizationEvent('pending', paymentPointer);
    STATE.isMonetized = true;
    STATE.requestId = uuidv4();

    // clear any old timers and start paying
    clearTimeout(STATE.timerId);
    pay();
  }
}

function stopMonetization(paymentPointer) {
  if (STATE.paymentPointer === paymentPointer) {
    emitMonetizationEvent('stop', paymentPointer, true);
    clearTimeout(STATE.timerId);
    STATE.timerId = null;
    STATE.isMonetized = false;
    STATE.paymentPointer = null;
    STATE.destinationWallet = null;
    STATE.requestId = null;
  }
}

function emitMonetizationEvent(state, content, finalized) {
  if (state !== 'progress') {
    const stateString =
      state === 'start' ? 'started' : state === 'stop' ? 'stopped' : state;

    STATE.monetizationState = stateString;

    const type = 'monetizationstatechange';
    const detail = { state: stateString };

    // console.log('[novdan] posting event', type); //, detail);

    window.postMessage({
      name: 'monetization',
      event: { type, detail },
    });
  }

  const type = `monetization${state}`;
  const detail = {
    paymentPointer: content,
    requestId: STATE.requestId,
  };
  if (state === 'stop') {
    detail.finalized = Boolean(finalized);
  }
  if (state === 'progress') {
    detail.assetCode = 'NOV';
    detail.amount = String(PAYMENT_INTERVAL_SECONDS);
    detail.assetScale = 0;
  }

  // console.log('[novdan] posting event', type); //, detail);

  window.postMessage({
    name: 'monetization',
    event: { type, detail },
  });
}

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

async function fetchTransfer(allowRefresh = true) {
  if (!SETTINGS.access_token) {
    throw new Error('No access token!');
  }

  const response = await fetch(`${API_URL_BASE}/api/transfer`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${SETTINGS.access_token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: SETTINGS.wallet_id,
      to: STATE.destinationWallet,
      amount: 5,
    }),
  });

  if (response.status === 401 && allowRefresh && SETTINGS.refresh_token) {
    try {
      await refreshToken();
    } catch (error) {
      return response;
    }
    return fetchTransfer(false);
  }

  return response;
}

async function pay() {
  // schedule next payment
  STATE.timerId = setTimeout(pay, PAYMENT_INTERVAL_SECONDS * 1000);

  // dont pay if page is hidden (background tab, minimized window, etc.)
  // or there is no active subcription
  if (!STATE.isVisible || !SETTINGS.active_subscription) {
    return;
  }

  // track last timer timestamp (to detect background timer throttling by browsers)
  const timestamp = Date.now();
  const timeDiff = timestamp - STATE.timerTimestamp;
  const minDiff = PAYMENT_INTERVAL_SECONDS * 1000;
  if (timeDiff < minDiff) {
    return;
  }
  STATE.timerTimestamp = timestamp;

  console.log('[novdan] pay', Date.now(), STATE.destinationWallet);

  const response = await fetchTransfer();

  if (response.status !== 200) {
    console.log('[novdan] bad transfer response', response.status);
    return;
  }

  if (STATE.monetizationState !== 'started') {
    emitMonetizationEvent('start', STATE.paymentPointer);
  }
  emitMonetizationEvent('progress', STATE.paymentPointer);
}

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
  const { name, event } = messageEvent.data;
  if (name === 'monetization' && event) {
    const { type, detail } = event;
    if (type === 'meta-tag-added') {
      onMetaTagAdded(detail);
    } else if (type === 'meta-tag-removed') {
      onMetaTagRemoved(detail);
    }
  }
}

function onMetaTagAdded({ content: paymentPointer }) {
  const url = getUrlFromPaymentPointer(paymentPointer);
  if (isValidPaymentUrl(url)) {
    if (STATE.paymentPointer) {
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

function getUrlFromPaymentPointer(pp) {
  const ppUrl = pp.replace(/^\$/, 'https://');
  const url = new URL(ppUrl);
  if (url.pathname === '/') {
    url.pathname = '/.well-known/pay';
  }
  return url;
}

function isValidPaymentUrl(url) {
  // for testing allow all
  if (TESTING_HOSTNAMES.includes(window.location.hostname)) {
    return true;
  }
  // otherwise only allow our wallet domain
  return url.hostname === 'denarnica.novdan.si';
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
  const url = getUrlFromPaymentPointer(paymentPointer);
  const json = await fetchSpsp4(url);

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
    STATE.paymentPointer = paymentPointer;
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

async function pay() {
  // schedule next payment
  STATE.timerId = setTimeout(pay, PAYMENT_INTERVAL_SECONDS * 1000);

  // dont pay if page is hidden (background tab, minimized window, etc.)
  if (!STATE.isVisible) {
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

  const response = await fetch('https://denarnica.novdan.si/api/transfer', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: '', // TODO: get users wallet
      to: STATE.destinationWallet,
      amount: 5,
    }),
  });

  if (response.status !== 200) {
    console.log('[novdan] bad transfer response', response.status);
    return;
  }

  if (STATE.monetizationState !== 'started') {
    emitMonetizationEvent('start', STATE.paymentPointer);
  }
  emitMonetizationEvent('progress', STATE.paymentPointer);
}

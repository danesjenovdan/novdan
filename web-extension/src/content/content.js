console.log('Content started!');

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

const STATE = {
  isMonetized: false,
  paymentPointer: null,
  monetizationState: 'stopped',
  requestId: uuidv4(),
  isVisible: true,
  timerId: null,
};

document.addEventListener('visibilitychange', onVisibilityChange, false);
window.addEventListener('message', onMessage, false);

function onMessage(messageEvent) {
  const { name, event } = messageEvent.data;
  if (name === 'monetization') {
    const { type, detail } = event;
    if (type === 'meta-tag-added') {
      onMetaTagAdded(detail);
    } else if (type === 'meta-tag-remove') {
      onMetaTagRemoved(detail);
    }
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
  return true;
  // TODO: actual hostname
  // return url.hostname === 'denarnica.djnd.si';
}

function getPayeeIdFromUrl(url) {
  if (isValidPaymentUrl(url)) {
    return url.pathname.replace(/^\//, '');
  }
}

function onMetaTagAdded(detail) {
  const url = getUrlFromPaymentPointer(detail.content);
  if (isValidPaymentUrl(url)) {
    emitMonetizationEvent('pending', detail.content);
    STATE.isMonetized = true;
    STATE.paymentPointer = detail.content;

    // force update visibility
    onVisibilityChange();

    // start paying
    if (STATE.timerId === null) {
      STATE.timerId = 0;
      pay();
    }
  }
}

function onMetaTagRemoved(detail) {
  const url = getUrlFromPaymentPointer(detail.content);
  if (isValidPaymentUrl(url)) {
    emitMonetizationEvent('stop', detail.content);
    STATE.isMonetized = false;
    STATE.paymentPointer = null;
  }
}

function emitMonetizationEvent(state, content, finalized) {
  if (state !== 'progress') {
    const stateString =
      state === 'start' ? 'started' : state === 'stop' ? 'stopped' : state;

    STATE.monetizationState = stateString;

    window.postMessage({
      name: 'monetization',
      event: {
        type: 'monetizationstatechange',
        detail: { state: stateString },
      },
    });
  }

  const detail = {
    paymentPointer: content,
    requestId: STATE.requestId,
  };
  if (state === 'stop') {
    detail.finalized = Boolean(finalized);
  }
  if (state === 'progress') {
    detail.assetCode = 'XXX'; // TODO: actual currency code
    detail.amount = '5';
    detail.assetScale = 0;
    // TODO: maybe add `receipt: String`
  }

  window.postMessage({
    name: 'monetization',
    event: {
      type: `monetization${state}`,
      detail,
    },
  });
}

function onVisibilityChange() {
  STATE.isVisible = document.visibilityState === 'visible';
}

async function pay() {
  STATE.timerId = null;
  if (!STATE.isMonetized || !STATE.isVisible) {
    return;
  }

  const url = getUrlFromPaymentPointer(STATE.paymentPointer);
  const payeeId = getPayeeIdFromUrl(url);

  console.log('payeeId', payeeId);

  // TODO: call actual api
  const response = await fetch(
    `http://localhost:3000/accounts/${payeeId}/settlement`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        scale: 0,
        amount: 5,
      }),
    }
  );
  const text = await response.text();
  console.log('after pay', text);

  if (STATE.monetizationState !== 'started') {
    emitMonetizationEvent('start', STATE.paymentPointer);
  }
  emitMonetizationEvent('progress', STATE.paymentPointer);

  STATE.timerId = setTimeout(pay, 5000);
}

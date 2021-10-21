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

// monetizationpending
// monetizationstart
// monetizationstop
// monetizationprogress

// const uuid = uuidv4();
// window.postMessage({
//   name: 'monetization',
//   event: {
//     type: 'monetizationstatechange',
//     detail: { state: 'stopped' },
//   },
// });
// window.postMessage({
//   name: 'monetization',
//   event: {
//     type: 'monetizationstop',
//     detail: {
//       paymentPointer: '$test.example.com/WHATEVER',
//       requestId: 'UUIDv4',
//     },
//   },
// });

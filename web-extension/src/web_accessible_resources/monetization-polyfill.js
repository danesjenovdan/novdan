(function () {
  console.log('[novdan] monetization polyfill started');

  /**
   * Polyfill `document.monetization`.
   */
  if (!document.monetization) {
    // `document.monetization` needs to be of type `EventTarget` and elements are
    document.monetization = document.createElement('span');
    document.monetization.state = 'stopped';
  }

  /**
   * Listen to messages from extension and dispatch `document.monetization` events.
   */
  window.addEventListener('message', onMessage, false);

  function onMessage(messageEvent) {
    const { name, event } = messageEvent.data;
    if (name === 'monetization') {
      const { type, detail } = event;
      if (type === 'monetizationstatechange') {
        document.monetization.state = detail.state;
      } else {
        document.monetization.dispatchEvent(new CustomEvent(type, { detail }));
      }
    }
  }

  /**
   * Observe for new `meta` tags when DOM is ready.
   */
  if (
    document.readyState === 'interactive' ||
    document.readyState === 'complete'
  ) {
    observeHead();
  } else {
    document.addEventListener('readystatechange', () => {
      if (document.readyState === 'interactive') {
        observeHead();
      }
    });
  }

  function observeHead() {
    document.head
      .querySelectorAll('meta[name="monetization"]')
      .forEach(onMonetizationMetaTagAdded);

    const headObserver = new MutationObserver(onHeadChildListChanged);
    headObserver.observe(document.head, { childList: true });
    // TODO: detect meta attibute change
  }

  function onHeadChildListChanged(records) {
    const childListRecords = records.filter((r) => r.type === 'childList');

    const isMonetizationMetaTag = (n) =>
      n.tagName === 'META' && n.name === 'monetization';

    childListRecords.forEach((record) => {
      Array.from(record.removedNodes)
        .filter(isMonetizationMetaTag)
        .forEach(onMonetizationMetaTagRemoved);
    });

    childListRecords.forEach((record) => {
      Array.from(record.addedNodes)
        .filter(isMonetizationMetaTag)
        .forEach(onMonetizationMetaTagAdded);
    });
  }

  function onMonetizationMetaTagAdded(metaTag) {
    console.log('[novdan] detected added meta tag', metaTag.content);
    window.postMessage({
      name: 'monetization',
      event: {
        type: 'meta-tag-added',
        detail: { content: metaTag.content },
      },
    });
  }

  function onMonetizationMetaTagRemoved(metaTag) {
    console.log('[novdan] detected removed meta tag', metaTag.content);
    window.postMessage({
      name: 'monetization',
      event: {
        type: 'meta-tag-removed',
        detail: { content: metaTag.content },
      },
    });
  }

  console.log('[novdan] monetization polyfill finished');
})();

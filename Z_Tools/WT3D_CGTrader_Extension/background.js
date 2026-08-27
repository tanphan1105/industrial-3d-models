// WT3D CGTrader Extension - Background Service Worker v1.0
// Ket noi Local Bridge Server de mo Windows File Explorer truc tiep hoac mo file:// tab

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if ((message.action === 'openFolderInExplorer' || message.action === 'openFolder') && message.path) {
    const bridgeUrl = `http://127.0.0.1:58921/open?path=${encodeURIComponent(message.path)}`;
    
    fetch(bridgeUrl)
      .then(res => res.json())
      .then(data => {
        sendResponse({ success: true, via: 'bridge', data: data });
      })
      .catch(err => {
        // Fallback: neu bridge server chua bat, mo file:// URL tren tab
        const parts = message.path.split('\\');
        const fileUrl = 'file:///' + parts.join('/');
        chrome.tabs.create({ url: fileUrl }, (tab) => {
          sendResponse({ success: true, via: 'tab', tabId: tab ? tab.id : -1 });
        });
      });
    return true; // Giu kenh async response
  }
});

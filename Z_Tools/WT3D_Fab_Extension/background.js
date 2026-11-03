// WT3D Fab Extension - Background Service Worker v3.9.14
// 1. Tu dong inject content.js + dope-content.js (allFrames) vao moi tab Fab.com dang mo ngay khi Load/Reload Extension
// 2. Bam icon Extension tren thanh cong cu se bat ngay bang WT3D Fab Helper & 3D Studio
// 3. Ket noi Local Bridge Server de mo Windows File Explorer truc tiep

async function injectIntoFabTab(tabId, tabUrl = '') {
  if (!tabId) return;
  const isDopeTab = String(tabUrl || '').toLowerCase().includes('/dope/');
  if (!isDopeTab) {
    try {
      await chrome.scripting.executeScript({
        target: { tabId: tabId, allFrames: false },
        files: ["content.js"]
      });
    } catch (e) {}
  }

  try {
    await chrome.scripting.executeScript({
      target: { tabId: tabId, allFrames: true },
      files: ["render-toolbar.js", "material-presets.js", "dope-content.js"]
    });
  } catch (e) {}

  try {
    await chrome.scripting.executeScript({
      target: { tabId: tabId, allFrames: true },
      world: "MAIN",
      files: ["color-bridge.js", "render-preset.js", "render-engine.js", "render-reader.js"]
    });
  } catch (e) {}

  try {
    await chrome.scripting.executeScript({
      target: { tabId: tabId, allFrames: true },
      func: () => {
        const studioPanel = document.getElementById('wt3d-fab-studio-panel');
        if (studioPanel) {
          studioPanel.style.display = 'block';
        }
        const dopeFrame = Array.from(document.querySelectorAll('iframe')).find(frame => {
          const src = (frame.src || frame.getAttribute('src') || '').toLowerCase();
          const rect = frame.getBoundingClientRect();
          return src.includes('/dope/') && rect.width > 200 && rect.height > 200;
        });
        if (!dopeFrame) {
          const p = document.getElementById('wt3d-fab-floating-panel');
          const l = document.getElementById('wt3d-fab-launcher-btn');
          if (p) {
            p.style.display = 'block';
            if (l) l.style.display = 'none';
          }
        }
      }
    });
  } catch (e) {}
}

async function injectIntoFabTabs() {
  try {
    const tabs = await chrome.tabs.query({ url: ["https://*.fab.com/*", "https://fab.com/*"] });
    for (const tab of tabs) {
      if (tab.id) await injectIntoFabTab(tab.id, tab.url || '');
    }
  } catch (err) {
    console.warn("[WT3D Background] Query tabs error:", err);
  }
}

chrome.runtime.onInstalled.addListener(() => {
  injectIntoFabTabs();
});

chrome.runtime.onStartup.addListener(() => {
  injectIntoFabTabs();
});

chrome.action.onClicked.addListener(async (tab) => {
  if (tab && tab.id && tab.url && tab.url.includes("fab.com")) {
    await injectIntoFabTab(tab.id, tab.url || '');
  } else {
    injectIntoFabTabs();
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if ((message.action === 'openFolderInExplorer' || message.action === 'openFolder') && message.path) {
    const bridgeUrl = `http://127.0.0.1:58921/open?path=${encodeURIComponent(message.path)}`;
    
    fetch(bridgeUrl)
      .then(res => res.json())
      .then(data => {
        sendResponse({ success: true, via: 'bridge', data: data });
      })
      .catch(err => {
        const parts = message.path.split('\\');
        const fileUrl = 'file:///' + parts.join('/');
        chrome.tabs.create({ url: fileUrl }, (tab) => {
          sendResponse({ success: true, via: 'tab', tabId: tab ? tab.id : -1 });
        });
      });
    return true;
  }
});

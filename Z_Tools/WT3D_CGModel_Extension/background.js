// WT3D CGModel Background Service Worker v1.0.0
const LOCAL_BRIDGE_URL = 'http://127.0.0.1:18888/open-folder';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'openFolderInExplorer') {
        const folderPath = request.path;
        console.log('[WT3D CGModel Background] Opening Explorer for:', folderPath);

        fetch(LOCAL_BRIDGE_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: folderPath })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'ok') {
                sendResponse({ success: true, via: 'bridge', message: 'Opened via Local Bridge' });
            } else {
                fallbackOpen(folderPath, sendResponse);
            }
        })
        .catch(() => {
            fallbackOpen(folderPath, sendResponse);
        });

        return true;
    }
});

function fallbackOpen(folderPath, sendResponse) {
    const fileUrl = 'file:///' + folderPath.replace(/\\/g, '/');
    chrome.tabs.create({ url: fileUrl }, (tab) => {
        if (chrome.runtime.lastError) {
            sendResponse({ success: false, via: 'error', message: chrome.runtime.lastError.message });
        } else {
            sendResponse({ success: true, via: 'tab', tabId: tab.id });
        }
    });
}

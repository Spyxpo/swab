const path = require("path");
const { BrowserWindow } = require("electron"); // https://www.electronjs.org/docs/api/browser-window

exports.createBrowserWindow = () => {
  // https://www.electronjs.org/docs/api/browser-window#class-browserwindow
  return new BrowserWindow({
    width: 1024,
    height: 768,
    minWidth: 400, 
    minHeight: 600,
    icon: path.join(__dirname, "assets/icons/png/favicon.png"),
    // titleBarStyle: 'hidden',
    // frame: false,
    backgroundColor: "#fff",
    autoHideMenuBar: true,
    webPreferences: {
      devTools: false, // false if you want to remove dev tools access for the user
      contextIsolation: true,
      webviewTag: true, // https://www.electronjs.org/docs/api/webview-tag,
      preload: path.join(__dirname, "../preload.js"), // required for print function
      enableRemoteModule: true,
      nodeIntegration: false,
      nativeWindowOpen: true,
      webSecurity: true,
      allowRunningInsecureContent: true
    },
  });
};

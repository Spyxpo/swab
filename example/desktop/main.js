// Electron
const { app } = require("electron");

// Add app, Menu

// This method will be called when Electron has finished initialization and is ready to create browser windows
app.allowRendererProcessReuse = true;
app.on("ready", () => {
  // Main window
  const window = require("./src/window");
  mainWindow = window.createBrowserWindow(app);

  // Option 1: Uses Webtag and load a custom html file with external content
  mainWindow.loadURL(`file://${__dirname}/index.html`, { userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' });

  // Option 2: Load directly an URL if you don't need interface customization
  //mainWindow.loadURL("https://github.com");

  // Option 3: Uses BrowserView to load an URL
  //const view = require("./src/view");
  //view.createBrowserView(mainWindow);

  // Display Dev Tools
  //mainWindow.openDevTools();

  // Menu (for standard keyboard shortcuts)
  // const menu = require("./src/menu");
  // const template = menu.createTemplate(app.name);
  // const builtMenu = Menu.buildFromTemplate(template);
  // Menu.setApplicationMenu(builtMenu);

  // Print function (if enabled)
  require("./src/print");
});

// Quit when all windows are closed.
app.on("window-all-closed", () => {
  app.quit();
});

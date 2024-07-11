const { app, BrowserWindow } = require('electron')
const path = require('path')
function createWindow () {
  console.log("browser window created");
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: true,
      enableRemoteModule: true,
      preload: `${__dirname}/preload.js`,
    }
  });

  win.loadURL('http://localhost:3000/auth').then(() => {
    console.log("loaded");
  }).catch((err) => { console.log(err); });

}

app.whenReady().then(createWindow)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})



app.whenReady().then(() => {
  console.log("app ready");
    if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
});
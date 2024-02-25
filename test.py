import subprocess
import time
import webview

class Api:
    def __init__(self):
        self.window = None

    def test(self):
        print('test successful!')

    def close(self, shiftKey):
        if shiftKey:
            subprocess.Popen("thorium-browser https://youtube.com", shell=True)
            print("Shift key is pressed")
        self.window.destroy()

    def fit_window(self, width, height):
        self.window.resize(width, height)

if __name__ == '__main__':
    api = Api()
    api.window = webview.create_window(
        'Quickscripts',
        'assets/index.html',
        js_api=api,
        min_size=(100, 100),
        frameless=True,
        on_top=True,
        x=0,
        y=0,
        transparent=True
    )
    webview.start(debug=True)

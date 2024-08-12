from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView



class MainWindow(QMainWindow):
    def __init__(self, host, port):
        super().__init__()
        # Create a web view widget
        self.webview = QWebEngineView()
        # Set the URL to be displayed
        self.webview.setUrl(QUrl(f"http://{host}:{port}/"))
        # Add the web view widget to the main window
        self.setCentralWidget(self.webview)

    def setServer(self, flask_server):
        self.flask_server = flask_server

    def closeEvent(self, event):
        # Stop the Flask server when the PyQt window is closed
        self.flask_server.shutdown()
        event.accept()



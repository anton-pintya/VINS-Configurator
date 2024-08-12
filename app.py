from flask import Flask, render_template, request, redirect, url_for
import os
import sys
import webbrowser
import signal
import threading
from werkzeug.serving import make_server


from process_configs import *
from window import *


import argparse


app = Flask("VINS-Configurator")

CONFIG_DIR = '../../modules/vins_core/configurations'
TEMPLATE_DIR = "./config_templates"


@app.route('/')
def index():
    files = os.listdir(CONFIG_DIR)
    return render_template('index.html', files=files)


@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_file(filename):
    if request.method == 'POST':
        return save_file(filename)
    else:
        return get_file(filename)


def save_file(filename):
    file_path = os.path.join(CONFIG_DIR, filename)

    content = request.form.to_dict()

    result = ""

    match (filename[:-5]):
        case "config":
            template_file = os.path.join(TEMPLATE_DIR, "config_tmpl.j2")
            result = POST_save(template_file, content)

        case "dataset_config":
            template_file = os.path.join(TEMPLATE_DIR, "dataset_tmpl.j2")
            result = POST_save(template_file, content)

        case "video_config":
            template_file = os.path.join(TEMPLATE_DIR, "video_tmpl.j2")
            result = POST_save(template_file, content)
        
        case "camera_config":
            template_file = os.path.join(TEMPLATE_DIR, "camera_tmpl.j2")
            result = POST_save(template_file, content)
    
    if result != "":
        with open(file_path, "w") as file:
            file.write(result)
    
    return redirect(url_for('index'))



def get_file(filename):
    file_path = os.path.join(CONFIG_DIR, filename)

    match (filename[:-5]):
        case "config":
            return GET_config(file_path)

        case "dataset_config":
            return GET_dataset(file_path)

        case "video_config":
            return GET_video(file_path)
        
        case "camera_config":
            return GET_camera(file_path)




# Flask server class to handle start and stop
class FlaskServer(threading.Thread):
    def __init__(self, host, port, app):
        threading.Thread.__init__(self)
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


WINDOWED = False


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="VINS-Configurator app")
    parser.add_argument("--win", action="store_true", help="Launch app in windowed mode", default=False)
    parser.add_argument("--port", type=int, help="Port number", default=5000)
    parser.add_argument("--host", type=str, help="Host IP-address", default="127.0.0.1")

    args = parser.parse_args()

    port = args.port
    address = args.host

    WINDOWED = args.win 

    # Start the Flask server
    flask_server = FlaskServer(address, port, app)
    flask_server.start()

    if WINDOWED:
        # Start the PyQt5 application
        app_qt = QApplication(sys.argv)
        main_window = MainWindow(host=address, port=port)
        main_window.setServer(flask_server)
        main_window.show()

        # Run the PyQt5 application
        sys.exit(app_qt.exec_())
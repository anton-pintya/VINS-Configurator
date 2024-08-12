from flask import render_template

import jinja2
import yaml
import os





def get_file_content(file_path):
    filename = file_path.split('/')[-1][:-5]
    print(filename)

    with open(file_path, 'r') as file:
        content = yaml.load(file, Loader=yaml.SafeLoader)

    return content


def GET_config(file_path):
    filename = file_path.split('/')[-1][:-5]

    content = get_file_content(file_path=file_path)
    
    current_content = {key: value for key, value in content.items() if key == 'current'}

    display_content = {
        "source": ["dataset", "video", "camera"]
    }

    return render_template('edit.html', filename=filename, content=display_content, default=current_content)


def GET_dataset(file_path):
    filename = file_path.split('/')[-1][:-5]
    
    content = get_file_content(file_path=file_path)

    current_content = {key: value for key, value in content.items() if key == 'current'}

    datasets = os.listdir("../../datasets")
    datasets.pop(datasets.index("custom"))

    current_dataset = current_content["current"]["dataset"]

    sequences = sorted(os.listdir(f"../../datasets/{current_dataset}/sequences"))

    display_content = {
        "dataset": datasets,
        "sequence": sequences
    }

    return render_template('edit.html', filename=filename, content=display_content, default=current_content)


def GET_video(file_path):
    filename = file_path.split('/')[-1][:-5]
    
    content = get_file_content(file_path=file_path)

    current_content = {key: value for key, value in content.items() if key == 'current'}

    video_folder = "../../" + current_content["current"]["path"] + "/sequences"

    display_content = {
        "path": [current_content["current"]["path"]],
        "video": os.listdir(video_folder),
        "fps": [10, 30, 60, 120]
    }

    print(display_content)

    return render_template('edit.html', filename=filename, content=display_content, default=current_content)


def GET_camera(file_path):
    filename = file_path.split('/')[-1][:-5]
    
    content = get_file_content(file_path=file_path)

    current_content = {key: value for key, value in content.items() if key == 'current'}

    video_devices = [int(video_device[5:]) for video_device in os.listdir("/dev") if "video" in video_device]

    display_content = {
        "device": video_devices,
        "fps": [10, 30, 60, 120]
    }

    return render_template('edit.html', filename=filename, content=display_content, default=current_content)



def POST_save(tmpl_path, data):
    template_file = tmpl_path
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))
    template = env.get_template(template_file)
    result = template.render(data)
    return result
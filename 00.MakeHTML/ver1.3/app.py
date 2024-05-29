from flask import Flask, render_template, url_for, send_from_directory, request
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

with open('sample.json') as f:
    plates = json.load(f)

app.config['IMAGE_FOLDER'] = '/Volumes/kunssd01/Toma3/240508-rockimages'

def get_files_by_well(profile_folder_path):
    files = os.listdir(profile_folder_path)
    organized_files = {"d1": {"thumbnail": None, "thumbnail_low": None, "high_res": None},
                       "d2": {"thumbnail": None, "thumbnail_low": None, "high_res": None}}

    # abs_path
    profile_folder_path = os.path.abspath(profile_folder_path)
    print(f"Profile_folder_abs:{profile_folder_path}")
    for file in files:
        file_path = os.path.join(profile_folder_path, file)
        print(f"Checking file: {file_path}")
        if "d1" in file:
            if "th_low" in file:
                organized_files["d1"]["thumbnail_low"] = file_path[len(app.config['IMAGE_FOLDER']) + 1:]
            elif "th" in file:
                organized_files["d1"]["thumbnail"] = file_path[len(app.config['IMAGE_FOLDER']) + 1:]
            elif "ef" in file:
                organized_files["d1"]["high_res"] = file_path[len(app.config['IMAGE_FOLDER']) + 1:]
        elif "d2" in file:
            if "th_low" in file:
                organized_files["d2"]["thumbnail_low"] = file_path[len(app.config['IMAGE_FOLDER']) + 1:]
            elif "th" in file:
                organized_files["d2"]["thumbnail"] = file_path[len(app.config['IMAGE_FOLDER']) + 1:]
            elif "ef" in file:
                organized_files["d2"]["high_res"] = file_path[len(app.config['IMAGE_FOLDER']) + 1:]

    print(f"Organized files: {organized_files}")
    return organized_files

def get_latest_batch_folder(base_paths):
    print("get_latest_batch_folder")
    print(base_paths)
    iBaseMax = 0
    latest_path = ""
    for base_path in base_paths:
        # base_pathが"plateID_"を含まなければスキップする
        if not 'batchID_' in base_path:
            continue
        # baseIDを取得する
        batch_id = int(base_path.split('_')[1])
        if iBaseMax < batch_id: 
            iBaseMax = batch_id
            latest_path = base_path
        
    return latest_path

@app.route('/')
def index():
    return render_template('index.html', plates=plates)

@app.route('/plate/<int:plate_id>')
def plate(plate_id):
    plate_folder = f"{str(plate_id).zfill(3)}"
    base_path = os.path.join(app.config['IMAGE_FOLDER'], plate_folder, f"plateID_{plate_folder}")
    batch_folders = os.listdir(base_path)
    latest_batch_folder = get_latest_batch_folder(batch_folders)

    wells = {}
    well_folder_path = os.path.join(base_path, latest_batch_folder)
    print(f"WELL: {well_folder_path}")

    for well_folder in os.listdir(well_folder_path):
        well_num = int(well_folder.split('_')[1])
        profile_folder_path = os.path.join(well_folder_path, well_folder, 'profileID_1')
        if os.path.exists(profile_folder_path):
            print(f"PROFILE: {profile_folder_path}")
            wells[well_num] = get_files_by_well(profile_folder_path)

    drop_type = request.args.get('drop_type', 'd1')
    print(f"Drop type: {drop_type} ")

    return render_template('plate.html', plate_id=plate_id, wells=wells, drop_type=drop_type)

@app.route('/images/<path:filename>')
def static_image(filename):
    full_path = os.path.join(app.config['IMAGE_FOLDER'], filename)
    print(f"Serving image: {full_path}")
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
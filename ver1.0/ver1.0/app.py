from flask import Flask, render_template, url_for, send_from_directory
import os
import json

app = Flask(__name__)

# Load plate data from JSON file
with open('sample.json') as f:
    plates = json.load(f)

app.config['IMAGE_FOLDER'] = '/Volumes/kunssd01/Toma3/240508-rockimages/'

@app.route('/')
def index():
    return render_template('index.html', plates=plates)


@app.route('/plate/<int:plate_id>')
def plate(plate_id):
    plate_folder = f"{str(plate_id).zfill(3)}"
    # root_dir
    plate_directory = os.path.join(app.config['IMAGE_FOLDER'], plate_folder, f"plateID_{plate_folder}")
    # plate_directoryにある　ディレクトリ　かつ "batch" から始まるディレクトリのリストを取得
    batch_folders = [f for f in os.listdir(plate_directory) if os.path.isdir(os.path.join(plate_directory, f)) and f.startswith('batch')]
    latest_batch_folder = max(batch_folders, key=lambda x: int(x.split('_')[1]))
    print("Batch folder")
    print(batch_folders)
    print("Latest batch folder")
    print(latest_batch_folder)
    
    thumbnails = []
    well_folder_path = os.path.join(app.config['IMAGE_FOLDER'], plate_folder, f"plateID_{plate_folder}", latest_batch_folder)
    for well_folder in os.listdir(well_folder_path):
        well_num = int(well_folder.split('_')[1])
        profile_folder_path = os.path.join(well_folder_path, well_folder, 'profileID_1')
        print(profile_folder_path)
        if os.path.exists(profile_folder_path):
            for file in os.listdir(profile_folder_path):
                if 'th' in file and 'low' not in file and file.startswith('d1'):
                    url_text = f'{plate_folder}/plateID_{plate_folder}/{latest_batch_folder}/{well_folder}/profileID_1/{file}'
                    print("URL_TEXT:",url_text)
                    thumbnails.append((well_num, url_for('static_image', filename=url_text)))
                    # thumbnails.append((well_num, url_for(filename=f'{root_dir}/{plate_folder}/plateID_{plate_folder}/{latest_batch_folder}/{well_folder}/profileID_1/{file}')))
                    break
    thumbnails.sort(key=lambda x: x[0])
    return render_template('plate.html', plate_id=plate_id, thumbnails=thumbnails)

@app.route('/images/<path:filename>')
def static_image(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

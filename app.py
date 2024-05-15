from flask import Flask, render_template, url_for, send_from_directory, jsonify
import os
import json

app = Flask(__name__)

# JSONファイルの読み込み
with open('sample.json') as f:
    plates = json.load(f)

print(plates)

# 静的ファイルのディレクトリを設定
app.config['IMAGE_FOLDER'] = '/Volumes/kunssd01/Toma3/240508-rockimages'

@app.route('/')
def index():
    return render_template('index.html', plates=plates)

@app.route('/plate/<int:plate_id>')
def plate(plate_id):
    plate_folder = f"{str(plate_id).zfill(3)}"
    base_path = os.path.join(app.config['IMAGE_FOLDER'], plate_folder, f"plateID_{plate_folder}")
    plate_directory = os.path.join(app.config['IMAGE_FOLDER'], plate_folder, f"plateID_{plate_folder}")
    batch_folders = [f for f in os.listdir(plate_directory) if os.path.isdir(os.path.join(plate_directory, f)) and f.startswith('batch')]
    latest_batch_folder = max(batch_folders, key=lambda x: int(x.split('_')[1]))

    thumbnails = []
    large_images = []

    well_folder_path = os.path.join(app.config['IMAGE_FOLDER'], plate_folder, f"plateID_{plate_folder}", latest_batch_folder)

    for well_folder in os.listdir(well_folder_path):
        well_num = int(well_folder.split('_')[1])
        profile_folder_path = os.path.join(well_folder_path, well_folder, 'profileID_1')
        print("###################")
        print(profile_folder_path)
        print("###################")
        if os.path.exists(profile_folder_path):
            thumb_url = None
            large_url = None
            for file in os.listdir(profile_folder_path):
                # Drop 1の画像だけ、とりあえず
                if file.startswith('d1'):
                    if 'th' in file and 'low' not in file:
                        thumb_url = url_for('static_image', filename=f'{plate_folder}/plateID_{plate_folder}/{latest_batch_folder}/{well_folder}/profileID_1/{file}')
                    elif 'ef' in file:
                        large_url = url_for('static_image', filename=f'{plate_folder}/plateID_{plate_folder}/{latest_batch_folder}/{well_folder}/profileID_1/{file}')

            if thumb_url and large_url:
                thumbnails.append((well_num, thumb_url, large_url))
    
    thumbnails.sort(key=lambda x: x[0])

    return render_template('plate.html', plate_id=plate_id, thumbnails=thumbnails)

@app.route('/images/<path:filename>')
def static_image(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
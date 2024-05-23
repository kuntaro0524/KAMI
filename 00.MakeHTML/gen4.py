import os

def generate_html(plate_id):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thumbnail Display</title>
        <style>
            table {border-collapse: collapse; width: 100%;}
            th, td {border: 1px solid #000; text-align: center;}
            th {background-color: #f2f2f2;}
            img {width: 100%; height: 100%; cursor: pointer;}
        </style>
        <script>
            function showFullImage(imagePath) {
                var fullImage = document.getElementById('fullImage');
                var modal = document.getElementById('modal');
                fullImage.src = imagePath;
                modal.style.display = 'block';
            }

            function closeModal() {
                var modal = document.getElementById('modal');
                modal.style.display = 'none';
            }
        </script>
    </head>
    <body>
        <table>
            <thead>
                <tr>
                    <th></th>
    """
    
    for col in range(1, 13):
        html_content += f"<th>{col}</th>"
    
    html_content += """
                </tr>
            </thead>
            <tbody>
    """

    for row in range(1, 9):  # 8 rows
        row_letter = chr(64 + row)  # A-H
        html_content += f"<tr><th>{row_letter}</th>"
        for col in range(1, 13):  # 12 columns
            well_num = (row - 1) * 12 + col
            thumbnail_path, full_image_path = find_images(plate_id, well_num)
            if thumbnail_path and full_image_path:
                html_content += f"<td><img src='{thumbnail_path}' alt='Well {well_num}' onclick='showFullImage(\"{full_image_path}\")'></td>"
            else:
                html_content += "<td></td>"
        html_content += "</tr>"

    html_content += """
            </tbody>
        </table>

        <div id="modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background-color:rgba(0,0,0,0.8);">
            <span style="position:absolute; top:20px; right:35px; color:#fff; font-size:40px; font-weight:bold; cursor:pointer;" onclick="closeModal()">&times;</span>
            <img id="fullImage" style="display:block; margin:auto; max-width:90%; max-height:90%;">
        </div>
    </body>
    </html>
    """

    return html_content

def find_images(plate_id, well_num):
    # base_dir の中にある構造について
    # ###/plateID_###/batchID_$$$/wellNum_??/profileID_1/
    # ###: plate_id (3桁の整数)
    # $$$: batch_id (1桁から4桁の整数)
    # ??: well_num (1から96の整数)
    # 'profileID_1' は固定された文字列
    # plateID_### は plateID_{plate_id} というディレクトリ名で保存されている
    base_dir = f"./{plate_id}/plateID_{plate_id}/"

    # この中に batchID_$$$ というディレクトリが複数存在する
    # ここでは batchID が最大のものを選択する
    max_plate_id = 0
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            if dir.startswith("batchID_"):
                plate_id = int(dir.split("_")[1])
                if plate_id > max_plate_id:
                    max_plate_id = plate_id
    
    # max_plate_id のディレクトリの中から well_num に対応するサムネイル画像とフル画像を探す
    thumbnail_path = None
    full_image_path = None
     
    checkpath= os.path.join(base_dir, f"batchID_{max_plate_id}")
    print(checkpath)
    for root, dirs, files in os.walk(checkpath):
        for file in files:
            if f"wellNum_{well_num}" in root:
                if "th" in file and "low" not in file:
                    thumbnail_path = os.path.join(root, file)
                elif "th" not in file:
                    # file が "." で始まる場合はスキップ
                    if file.startswith("."):
                        continue
                    full_image_path = os.path.join(root, file)
                    print("KKK=",full_image_path)
        if thumbnail_path and full_image_path:
            break

    return thumbnail_path, full_image_path

# plateIDを指定してHTMLを生成
import sys
plate_id = int(sys.argv[1])
html_output = generate_html(plate_id)

# HTMLファイルとして保存
with open("output.html", "w") as file:
    file.write(html_output)

print("HTMLファイルが生成されました。")

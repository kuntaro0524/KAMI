import os

def generate_html(plate_id):
    base_dir = f"./{plate_id}"
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thumbnail Display</title>
        <style>
            table {border-collapse: collapse; width: 100%;}
            td {border: 1px solid #000; text-align: center;}
            img {max-width: 100%; max-height: 100%;}
        </style>
    </head>
    <body>
        <table>
    """

    for row in range(1, 9):  # 8 rows
        html_content += "<tr>"
        for col in range(1, 13):  # 12 columns
            well_num = (row - 1) * 12 + col
            thumbnail_path = find_thumbnail(base_dir, well_num)
            if thumbnail_path:
                html_content += f"<td><img src='{thumbnail_path}' alt='Well {well_num}'></td>"
            else:
                html_content += "<td></td>"
        html_content += "</tr>"

    html_content += """
        </table>
    </body>
    </html>
    """

    return html_content

def find_thumbnail(base_dir, well_num):
    print("base_dir", base_dir)
    print("searching for well", well_num)
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if f"wellNum_{well_num}" in root and "th" in file and "low" not in file:
                return os.path.join(root, file)
    return None

# plateIDを指定してHTMLを生成
plate_id = "350"  # 例としてplateIDを123に設定
html_output = generate_html(plate_id)

# HTMLファイルとして保存
with open("output.html", "w") as file:
    file.write(html_output)

print("HTMLファイルが生成されました。")
import argparse
from . import app

def main():
    parser = argparse.ArgumentParser(description='Run the KAMI Flask application.')
    parser.add_argument('--image-folder', type=str, required=True, help='Path to the image folder')
    parser.add_argument('--sample-json', type=str, required=True, help='Path to the sample JSON file')
    args = parser.parse_args()

    app.config['IMAGE_FOLDER'] = args.image_folder
    app.config['SAMPLE_JSON'] = args.sample_json

    app.load_data()

    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()

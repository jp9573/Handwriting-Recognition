from flask import Flask, request
from utils.image_parser import get_text_from_image
from utils.cloud_storage_manager import upload_data_to_gcs

app = Flask(__name__)


@app.route('/')
def welcome_page():
    return "HEY"


def send_response(message, success=True):
    return {"success": success, "message": message}


@app.route('/parseImage', methods=['POST'])
def parse_image():
    image_file = request.files['imageFile']
    image_data = image_file.read()
    upload_status, image_url = upload_data_to_gcs(image_data)
    if not upload_status:
        return send_response("Error while uploading image.", success=False)
    return send_response(get_text_from_image(image_url))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

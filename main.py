from flask import Flask, request
from utils.image_parser import get_text_from_image
from utils.cloud_storage_manager import upload_data_to_gcs
from utils.history_model import HistoricalData

app = Flask(__name__)


@app.route('/')
def welcome_page():
    return "HEY"


def send_response(message, success=True):
    return {"success": success, "message": message}


@app.route('/historicalData', methods=['GET'])
def get_historical_data():
    historical_data, offset = HistoricalData.get_historical_data(request.args.get('limit', '5'),
                                                                 request.args.get('offset', '0'))
    return_json = {'data': historical_data}
    if offset:
        return_json['offset'] = offset
    return send_response(return_json)


@app.route('/parseImage', methods=['POST'])
def parse_image():
    image_file = request.files['imageFile']
    image_data = image_file.read()
    upload_status, image_url = upload_data_to_gcs(image_data)
    if not upload_status:
        return send_response("Error while uploading image.", success=False)

    processed_text = get_text_from_image(image_url)
    HistoricalData.create_new(fileLink=image_url, processedText=processed_text)  # can be converted to async job
    return send_response(processed_text)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

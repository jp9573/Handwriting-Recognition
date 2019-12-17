from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def welcome_page():
    return "HEY"


@app.route('/parseImage', methods=['POST'])
def parse_image():
    image_file = request.files['imageFile']
    image_data = image_file.read()

    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

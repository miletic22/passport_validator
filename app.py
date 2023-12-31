from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
from utils import analyzer

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for static files

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_uploaded_file(file):
    if not file:
        print('No file attached in request')
        return None, None

    if file.filename == '':
        print('No file selected')
        return None, None

    if not allowed_file(file.filename):
        print('Invalid file type')
        return None, None

    filename = secure_filename(file.filename)
    print(filename)

    # Process the image and encode it
    img = Image.open(file.stream)
    with BytesIO() as buf:
        img.save(buf, 'jpeg')
        image_bytes = buf.getvalue()

    return filename, image_bytes


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        filename, image_bytes = process_uploaded_file(file)

        if filename is not None and image_bytes is not None:
            # Analyze the image using DummyAnalyzer
            print(type(file))
            #passport_analyzer = analyzer.PassportMachineReadableZoneAnalyzer(file)
            #result_string = passport_analyzer.parse()

            # Return result as JSON response
            #return jsonify(result_string=result_string)

    # Handle other cases or return default template
    return render_template('index.html', result_string=""), 200



if __name__ == '__main__':
    app.run(debug=True)

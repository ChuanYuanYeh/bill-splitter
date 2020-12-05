import os
import cv2
import pytesseract
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    return render_template('template.html')


@app.route('/', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Read the image
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename), 0)
    # Simple thresholding
    # ret, thresh1 = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text


if __name__ == '__main__':
    app.run(debug=True)

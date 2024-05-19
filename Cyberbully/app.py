from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import base64
import io
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Allow only up to 16MB files

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    return render_template('home.html')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            extracted_text, image_data = extract_text_from_image(file_path)
            return render_template('upload.html', extracted_text=extracted_text, image_data=image_data)
        else:
            flash('No file selected, or file type not allowed')
    return render_template('upload.html')

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return text, f"data:image/png;base64,{image_base64}"
    except Exception as e:
        return f"Error processing image: {str(e)}", None

if __name__ == '__main__':
    app.run(debug=True)

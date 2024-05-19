from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import base64
import io
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models
from tensorflow.keras.models import load_model, model_from_json
import numpy as np
from transformers import RobertaForSequenceClassification, RobertaConfig

print(tf.__version__)
# Load the configuration
config = RobertaConfig.from_pretrained("openai-community/roberta-base-openai-detector")

# Load the pre-trained Roberta model with the configuration
model = RobertaForSequenceClassification(config)

# Now the model is ready to be used for inference or further training


# Function to load the model
def load_keras_model():
    # Path to your model files
    json_file_path = os.path.join('models', 'model.json')
    h5_file_path = os.path.join('models', 'tf_model.h5')
    
    # Load the model architecture from JSON file
    with open(json_file_path, 'r') as json_file:
        loaded_model_json = json_file.read()
        model = model_from_json(loaded_model_json)
    
    # Load weights into the new model
    model.load_weights(h5_file_path)
    return model

model = load_keras_model()

if not os.path.exists('uploads'):
    os.makedirs('uploads')

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Allow only up to 16MB files

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/about')
def home():
    return render_template('home.html')

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        image = process_image(filepath)  # Preprocess the image
        prediction = model.predict(image)  # Make prediction
        return render_template('results.html', prediction=prediction)
    return render_template('upload.html')

def process_image(image_path):
    """Preprocess the image to fit your model's input requirements."""
    img = Image.open(image_path)
    img = img.resize((128, 128))  # Example resizing
    img_array = np.array(img) / 255.0  # Normalize if required
    img_array = img_array.reshape((1, 128, 128, 3))  # Adjust shape if needed
    return img_array


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
    
def predict():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        # Process the image and prepare it for prediction
        processed_image = process_image(file_path)
        # Make prediction
        prediction = model.predict(processed_image)
        return render_template('results.html', prediction=prediction)
    return redirect(url_for('upload'))
    
if __name__ == '__main__':
    app.run(debug=True)

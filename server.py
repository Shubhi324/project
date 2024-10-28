from flask import Flask, request
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64

app = Flask(__name__)

# Load your pre-trained model (example: an image classification model)
model = load_model('your_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['image']
    # Decode the image
    img_data = base64.b64decode(data)
    npimg = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))  # Resize as per your model's requirement
    img = np.expand_dims(img, axis=0) / 255.0  # Preprocess the image

    # Make prediction
    predictions = model.predict(img)
    class_index = np.argmax(predictions[0])
    return {"class_index": int(class_index)}

if __name__ == '__main__':
    app.run(debug=True)

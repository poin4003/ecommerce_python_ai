from flask import Flask, render_template, request, redirect, url_for
from models import db, Product
from werkzeug.utils import secure_filename
import os
import requests
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['ENV'] = os.getenv('FLASK_ENV')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH'))

HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
HUGGING_FACE_SENTIMENT_ANALYSIS_ENDPOINT = os.getenv("HUGGING_FACE_SENTIMENT_ANALYSIS_ENDPOINT")
HEADERS = {
    "Authorization": f"Bearer {HUGGING_FACE_TOKEN}",
    "Content-Type": "application/octet-stream"
}

db.init_app(app)

model = MobileNetV2(weights='imagenet')

with app.app_context():
    db.create_all()

def classify_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=1)[0]
    category = decoded_predictions[0][1]
    return category

@app.route('/', methods=['GET'])
def all_products():
    products = Product.query.all()
    return render_template('all_products.html', products=products)

@app.route('/create_product', methods=['POST'])
def create_product():
    name = request.form['name']
    description = request.form['description']
    file = request.files['image']
    if file:
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        image_path = image_path.replace('\\', '/')

        category = classify_image(image_path)

        product = Product(
            name=name,
            description=description,
            image_path=image_path,
            category=category
        )

        db.session.add(product)
        db.session.commit()
    return redirect(url_for('all_products'))

@app.route('/review_product', methods=['POST'])
def review_product():
    product_id = request.form['product_id']
    review = request.form['review']
    product = Product.query.get(product_id)
    if product:
        product.review = review

        response = requests.post(
            HUGGING_FACE_SENTIMENT_ANALYSIS_ENDPOINT,
            headers=HEADERS,
            json={"inputs": review}
        )

        if response.status_code == 200:
            result = response.json()
            sentiment_result = result[0]
            for item in sentiment_result:
                if item['label'] == 'POSITIVE':
                    product.sentiment = 'positive'
                    break
                elif item['label'] == 'NEGATIVE':
                    product.sentiment = 'negative'
                    break
        else:
            print(f"Error calling Hugging Face API: {response.status_code} - {response.text}")
            product.sentiment = 'error'

        db.session.commit()
    return redirect(url_for('all_products'))

@app.route('/recommendations', methods=['GET'])
def recommendations():
    positive_products = Product.query.filter_by(sentiment='positive').all()

    recommended = set()  

    for product in positive_products:
        recommended.add(product)

        similar_products = Product.query.filter(
            Product.category == product.category,
            Product.id != product.id  
        ).all()

        for similar in similar_products:
            if similar.sentiment != 'negative':
                recommended.add(similar)

    recommended = list(recommended)

    return render_template('recommendations.html', recommended=recommended)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
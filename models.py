from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    image_path = db.Column(db.String(200))
    category = db.Column(db.String(100))
    review = db.Column(db.String(500))
    sentiment = db.Column(db.String(50))
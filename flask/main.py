from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate
from dataclasses import dataclass
import requests
from producer import publish


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root1:root@db/main'
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()
    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()
    except:
        abort(400, 'You already liked this product')
    publish('product_liked', id)

    return jsonify({
        'message': 'success'
    })


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


# create table on docker
# docker-compose exec backend sh
# flask --app main db init
# flask db migrate -m "Initial migration"
# flask db upgrade

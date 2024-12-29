from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/app_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price,
            "user_id": self.user_id
        }

# initalize db
with app.app_context():
    db.create_all()

# validate user via user service
def validate_user(user_id):
    print('teste')
    user_service_url = os.getenv('USER_SERVICE_URL', 'http://user-service:5002/users')
    print(f'getting {user_service_url}/{user_id}')
    response = requests.get(f"{user_service_url}/{user_id}")
    if response.status_code == 404:
        return None
    return response.json()

# get orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

# create order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    if 'product_name' not in data or 'quantity' not in data or 'price' not in data or 'user_id' not in data:
        return jsonify({"error": "Product name, quantity, price, and user_id are required"}), 400

    user = validate_user(data['user_id'])
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_order = Order(
        product_name=data['product_name'],
        quantity=data['quantity'],
        price=data['price'],
        user_id=data['user_id']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order.to_dict())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

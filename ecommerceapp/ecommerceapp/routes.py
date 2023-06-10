from flask import Flask, request, jsonify, make_response, session, app, Response,url_for
from ecommerceapp import app, db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, MigrateCommand

from datetime import datetime,timedelta
import os
from sqlalchemy.orm import sessionmaker
from .models import*

from sqlalchemy.orm import joinedload

import base64


import json
import jwt
from functools import wraps
from flask import abort, current_app, request




'''
NOTE:
Use jsonify function to return the outputs and status code

Example:
with output
return jsonify(output),2000

only status code
return '',404


'''




# Use this token_required method for your routes where ever needed.
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		print(request.headers)
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
			print(token)
		if not token:
			return jsonify({'Message':' Token is missing'}), 401
		try:
			print("yes")
			data = jwt.decode(token, app.config['SECRET_KEY'],  algorithms='HS256')
			print(data)
			current_user = User.query.filter_by(user_id=data['user_id']).first()
			print(current_user.user_id)
			print(current_user.user_role)
		except:
			return jsonify({'Message': 'Token is invalid'}), 401
		return f(current_user, *args, **kwargs)
	return decorated

def role_required(role):
	def wrapper(fn):
		@wraps(fn)
		def decorated_view(*args, **kwargs):
			# user_id=kwargs('user_id',None)
			user_id = kwargs.pop('user_id', None)
			print(user_id)

			user_role = User.objects.get(user_id=user_id)
			print(user_role)

			roleName=user_role.user_role.role_name
			print(roleName)

			if roleName!=role:
				abort(403)
			return fn(*args, **kwargs)
		return decorated_view
	return wrapper



@app.route('/')
def index():
  return 'Index Page'


@app.route('/api/public/login', methods=['GET'])
def login():
	# uname=request.headers["Authorization"][6:]
	# print(uname)
	# pass1=str(base64.b64decode(uname))[2:-1]
	# username = pass1.split(":")[0]
	# password =  pass1.split(":")[1]
	auth_header = request.headers.get('Authorization')
	print(101,auth_header)

	#We have done split by " " as Basic encoded(username:password) in that form in test case	 
	if auth_header:
		auth_token = auth_header.split(" ")[1]
		print(105,auth_token)
		print(base64.b64decode(auth_token).decode())
		username, password = base64.b64decode(auth_token).decode().split(":")

		#We have done split by : as username:password in that form in test case	 

	# Find the user in the database based on the provided username
	user = User.query.filter_by(user_name=username).first()

	if user and check_password_hash(user.password, password):
		# Authentication successful
		token = jwt.encode({'user_id': user.user_id, 'exp': datetime.utcnow() + timedelta(hours=5)}, app.config['SECRET_KEY'], algorithm='HS256') 
		return jsonify({"token":token}), 200
	else:
		# Authentication failed
		return jsonify({"token":"0"}), 401

 
@app.route('/api/public/product/search', methods=['GET'])
def search_products():
	keyword = request.args.get('keyword')

	# Perform the join operation to retrieve the matching products
	products = db.session.query(Product).join(Category).filter(Product.product_name.contains(keyword)).all()

	if not products:
		return jsonify("Null"), 400
		

	# Prepare the response data
	response = []
	for product in products:
		category = {
			'category_id': product.category.category_id,
			'category_name': product.category.category_name
		}
		product_data = {
			'category': category,
			'product_id': product.product_id,
			'product_name': product.product_name,
			'price': product.price,
			'seller_id': product.seller_id
		}
		response.append(product_data)

	return jsonify(response), 200

# #------------------------------------Seller endpoints---------------------------------
# #----------------URL /api/auth/seller/product

@app.route('/api/auth/seller/product', methods=['GET'])
@token_required
def get_seller_products(current_user):
	if current_user.user_role != 2:
		return {
			"message": "Unauthorized Endpoint",
		}, 403  # Implement your own authentication logic

	# Retrieve the products owned by the seller
	products = Product.query.filter_by(seller_id=current_user.user_id).all()

	# If no products are found, return a 404 status code
	if not products:
		return {
			"message": "Product not found"
		}, 403

	# Prepare the response body
	response1 = []
	for product in products:
		response1.append({
			'category': {
				'category_id': product.category.category_id,
				'category_name': product.category.category_name
			},
			'price': product.price,
			'product_id': product.product_id,
			'product_name': product.product_name,
			'seller_id': product.seller_id
		})
	print(jsonify(response1))

	# return json.dumps(response1),200

	return jsonify(response1), 200

@app.route('/api/auth/seller/product/<int:product_id>', methods=['GET'])
@token_required
def get_product(current_user,product_id):
	if current_user.user_role != 2:
		return {
			"message": "Unauthorized Endpoint",
		}, 403
	
	product = Product.query.filter_by(product_id=product_id, seller_id=current_user.user_id).first()
	if not product:
		return jsonify({'error': 'Product not found'}), 404

	response =[ {
		'category': {
			'category_id': product.category.category_id,
			'category_name': product.category.category_name
		},
		'price': product.price,
		'product_id': product.product_id,
		'product_name': product.product_name,
		'seller_id': product.seller_id
	}]
	return jsonify(response), 200


@app.route('/api/auth/seller/product', methods=['POST'])
@token_required
def add_product(current_user):
	if current_user.user_role != 2:  # Assuming seller role_id is 2
		return jsonify({'message': 'Forbidden'}), 403

	data = request.get_json()
	product_id = data.get('product_id')

	# Check if the product_id already exists
	existing_product = Product.query.filter_by(product_id=product_id).first()
	if existing_product:
		return jsonify({'message': 'Product ID already exists'}), 409

	# Create and save the new product
	product = Product(
		product_id=product_id,
		product_name=data.get('product_name'),
		price=data.get('price'),
		seller_id=current_user.user_id,
		category_id=data.get('category_id')
	)
	db.session.add(product)
	db.session.commit()

	return jsonify(product.product_id), 201


@app.route('/api/auth/seller/product', methods=['PUT'])
@token_required
def update_product(current_user):
	if current_user.user_role != 2:  # Assuming seller role_id is 2
		return jsonify({'message': 'Forbidden'}), 403

	data = request.get_json()
	product_id = data.get('product_id')
	price = data.get('price')

	# Check if the product is owned by the seller
	product = Product.query.filter_by(product_id=product_id, seller_id=current_user.user_id).first()
	if not product:
		return jsonify({'message': 'Product not found or not owned by the seller'}), 404
	

	if product.price!=price:
		cartProducts=CartProduct.query.filter_by(product_id=product_id)
		for cp in cartProducts:
			cp.cart.total_amount+=cp.quantity*(price-product.price)

	# Update the product price
	product.price = price
	db.session.commit()

	return jsonify({'message': 'Product price updated successfully'}), 200


@app.route('/api/auth/seller/product/<int:prodid>', methods=['DELETE'])
@token_required
def delete_product(current_user, prodid):
	if current_user.user_role != 2:  # Assuming seller role_id is 2
		return jsonify({'message': 'Forbidden'}), 403

	# Check if the product is owned by the seller
	product = Product.query.filter_by(product_id=prodid, seller_id=current_user.user_id).first()
	if not product:
		return jsonify({'message': 'Product not found or not owned by the seller'}), 404

	cartProducts=CartProduct.query.filter_by(product_id=prodid)

	for cp in cartProducts:
		cp.cart.total_amount-=cp.quantity*product.price

	# Delete the product
	db.session.delete(product)
	db.session.commit()
    
	return jsonify({'message': 'Product deleted successfully'}), 200


# #------------------------------------Consumer endpoints---------------------------------
# #----------------URL /api/auth/consumer/product


@app.route('/api/auth/consumer/cart', methods=['GET'])
@token_required
def get_consumer_cart(current_user):
	if current_user.user_role != 1:  # Assuming consumer role_id is 1
		return jsonify({'message': 'Forbidden'}), 403

	# Perform the join on Cart, CartProduct, Product, and Category tables
	cart_data = Cart.query \
		.join(CartProduct, Cart.cart_id == CartProduct.cart_id) \
		.join(Product, CartProduct.product_id == Product.product_id) \
		.join(Category, Product.category_id == Category.category_id) \
		.filter(Cart.user_id == current_user.user_id) \
		.with_entities(
			CartProduct.cp_id,
			Cart.cart_id,
			Cart.total_amount,
			Product.product_id,
			Product.price,
			Product.product_name,
			Category.category_id,
			Category.category_name
		) \
		.all()
	print(cart_data)

	cart_items = []
	for cart_product in cart_data:
		cart_item = {
			'cartproducts': {
				'product': {
					'product_id': cart_product.product_id,
					'price': cart_product.price,
					'product_name': cart_product.product_name,
					'category': {
						'category_name': cart_product.category_name,
						'category_id': cart_product.category_id
					}
				},
				'cp_id': cart_product.cp_id
			},
			'cart_id': cart_product.cart_id,
			'total_amount': cart_product.total_amount
		}
		cart_items.append(cart_item)

	return jsonify(cart_items), 200



@app.route('/api/auth/consumer/cart', methods=['POST'])
@token_required
def add_to_consumer_cart(current_user):
    if current_user.user_role != 1:  # Assuming consumer role_id is 1
        return jsonify({'message': 'Forbidden'}), 403

    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Check if the product is already present in the cart
    existing_cart_product = CartProduct.query \
        .join(Cart, CartProduct.cart_id == Cart.cart_id) \
        .filter(Cart.user_id == current_user.user_id, CartProduct.product_id == product_id) \
        .first()

    if existing_cart_product:
        return jsonify({'message': 'Product already in cart'}), 409

    # Get the price of the product
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Calculate the total amount
    total_amount = current_user.cart.total_amount + (product.price * quantity)

    # Create a new CartProduct instance and add it to the cart
    new_cart_product = CartProduct(cart_id=current_user.cart.cart_id, product_id=product_id, quantity=quantity)
    db.session.add(new_cart_product)
    db.session.commit()

    # Update the total amount of the cart
    current_user.cart.total_amount = total_amount
    db.session.commit()

    return jsonify(total_amount), 200

@app.route('/api/auth/consumer/cart', methods=['PUT'])
@token_required
def update_consumer_cart(current_user):
    if current_user.user_role != 1:  # Assuming consumer role_id is 1
        return jsonify({'message': 'Forbidden'}), 403

    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Check if the product is present in the cart
    cart_product = CartProduct.query \
        .join(Cart, CartProduct.cart_id == Cart.cart_id) \
        .filter(Cart.user_id == current_user.user_id, CartProduct.product_id == product_id) \
        .first()

    if not cart_product:
        return jsonify({'message': 'Product not found in cart'}), 404

    # Get the price of the product
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Update the quantity and total amount
    total_amount = current_user.cart.total_amount + (quantity- cart_product.quantity) *(product.price)
    cart_product.quantity = quantity
    current_user.cart.total_amount = total_amount
    db.session.commit()

    return jsonify(total_amount), 200


@app.route('/api/auth/consumer/cart', methods=['DELETE'])
@token_required
def remove_from_consumer_cart(current_user):
	if current_user.user_role != 1:  # Assuming consumer role_id is 1
		return jsonify({'message': 'Forbidden'}), 403

	data = request.get_json()
	product_id = data.get('product_id')

	# Check if the product is present in the cart
	cart_product = CartProduct.query \
		.join(Cart, CartProduct.cart_id == Cart.cart_id) \
		.filter(Cart.user_id == current_user.user_id, CartProduct.product_id == product_id) \
		.first()

	if not cart_product:
		return jsonify({'message': 'Product not found in cart'}), 404

	# Get the price and quantity of the product
	product = Product.query.filter_by(product_id=product_id).first()
	if not product:
		return jsonify({'message': 'Product not found'}), 404

	# Calculate the total amount
	total_amount = current_user.cart.total_amount - (product.price * cart_product.quantity)

	# Remove the cart product from the cart
	db.session.delete(cart_product)
	db.session.commit()

	print(total_amount)

	# Update the total amount of the cart
	current_user.cart.total_amount = total_amount
	db.session.commit()

	return jsonify(total_amount), 200



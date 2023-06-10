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

"""
CONSUMER APIs
"""

# CONSUMER STARTS here

# @check_access decorator function
	
#Write your code here for the API end points
# @role_required('CONSUMER')

@app.route('/api/auth/consumer/cart', methods=['GET'])
@token_required
def get_consumer_cart(current_user):
	if current_user.user_role!=1:
		return {
		"message": "Unauthorized Endpoint",
	}, 401

	cart = Cart.query.filter_by(user_id=current_user.user_id).first()
	user_cart_id=cart.cart_id
	# Perform a join to retrieve the cart details
	cart_details = Cart.query\
		.join(CartProduct, Cart.cart_id == CartProduct.cart_id)\
		.join(Product, CartProduct.product_id == Product.product_id)\
		.join(Category, Product.category_id == Category.category_id)\
		.options(joinedload(Cart.cartproducts).joinedload(CartProduct.product))\
		.options(joinedload(Cart.cartproducts).joinedload(CartProduct.product).joinedload(Product.category))\
		.filter(Cart.cart_id == user_cart_id)\
		.all()
    
    # Create a dictionary to store the unfolded cart details
	unfolded_cart = {
		"cart_id": user_cart_id,
		"total_amount": 0,
		"products": []
	}
    
    # Iterate over the cart details and add product information
	for cart in cart_details:
		unfolded_cart["total_amount"] += cart.cartproducts.quantity * cart.cartproducts.product.price
		unfolded_cart["products"].append({
			"product_id": cart.cartproducts.product.product_id,
			"product_name": cart.cartproducts.product.product_name,
			"price": cart.cartproducts.product.price,
			"quantity": cart.cartproducts.quantity,
			"category_id": cart.cartproducts.product.category.category_id,
			"category_name": cart.cartproducts.product.category.category_name
		})

	return jsonify(unfolded_cart)

@app.route('/api/auth/consumer/cart', methods=['POST'])
@token_required
def add_product_to_cart(current_user):
	if not request.is_json:
		return jsonify({"error": "Request body must be in JSON format"}), 400
	if current_user.user_role!=1:
		return {
		"message": "Unauthorized Endpoint",
	}, 401

	product_id = request.json.get('product_id')
	quantity = request.json.get('quantity')

	if not product_id or not quantity:
		return jsonify({"error": "Product ID and quantity are required in the request body"}), 400

	# Find the product in the cart
	existing_product = CartProduct.query.filter_by(product_id=product_id).first()

	if existing_product:
		return jsonify({"error": "Product already exists in the cart"}), 409

	# Create a new cart product
	new_cart_product = CartProduct(product_id=product_id, quantity=quantity)
	db.session.add(new_cart_product)
	db.session.commit()

	# Get the cart associated with the new cart product
	cart = Cart.query.get(new_cart_product.cart_id)

	# Recalculate the total amount of the cart
	cart.total_amount = sum(cp.product.price * cp.quantity for cp in cart.cartproducts)
	db.session.commit()

	return jsonify({
		"message": "Product added to cart",
		"total_amount": cart.total_amount
	})

@app.route('/api/auth/consumer/cart', methods=['PUT'])
@token_required
def update_cart_product_quantity(current_user):
    # Unauthorized access
	if current_user.user_role!=1:
		return {
		"message": "Unauthorized Endpoint",
	}, 401

	if not request.is_json:
		return jsonify({"error": "Request body must be in JSON format"}), 400
    
	product_id = request.json.get('product_id')
	quantity = request.json.get('quantity')

	if not product_id or not quantity:
		return jsonify({"error": "Product ID and quantity are required in the request body"}), 400

    # Find the product in the cart
	cart_product = CartProduct.query.filter_by(product_id=product_id).first()
    
	if not cart_product:
		return jsonify({"error": "Product not found in the cart"}), 404

    # Update the quantity of the cart product
	cart_product.quantity = quantity
	db.session.commit()
    
	# Get the cart associated with the cart product
	cart = Cart.query.get(cart_product.cart_id)

	# Recalculate the total amount of the cart
	cart.total_amount = sum(cp.product.price * cp.quantity for cp in cart.cartproducts)
	db.session.commit()
    
	return jsonify({
		"message": "Product quantity updated in cart",
		"total_amount": cart.total_amount
	})

@app.route('/api/auth/consumer/cart',methods=["DELETE"])
@token_required
def deleteProductFromCart(current_user):
	# Unauthorized access
	if current_user.user_role!=1:
		return {
		"message": "Unauthorized Endpoint",
	}, 401

	product_id = request.json.get('product_id')
	# Find the product in the cart
	cart_product = CartProduct.query.filter_by(product_id=product_id).first()
	# Retrieve the cart for the current user (assuming you have user authentication implemented)
	user_cart = Cart.query.filter_by(user_id=current_user.user_id).first()

	if user_cart:
		# Retrieve the cart product to be removed
		cart_product = CartProduct.query.filter_by(cart_id=user_cart.cart_id, product_id=product_id).first()
		
		if cart_product:
			# Delete the cart product from the database
			db.session.delete(cart_product)
			db.session.commit()

			print(user_cart.cartproducts)
			
			# Recalculate the total amount of the cart
			user_cart.total_amount = sum(cp.product.price * cp.quantity for cp in user_cart.cartproducts)
			db.session.commit()
			
			return jsonify({'total_amount': user_cart.total_amount}), 200
		else:
			return jsonify({'message': 'Product not found in cart'}), 404
	else:
		return jsonify({'message': 'Cart not found for the user'}), 404

# CONSUMER ENDS here


"""
SELLER APIs
"""

@app.route('/api/auth/seller/product/<id>', methods=['GET'])
@token_required
def getProduct(current_user,id):
	if current_user.user_role!=2:
		return {
		"message": "Unauthorized Endpoint",
	}, 401
	seller_id=current_user.user_id
	productId=id

	product = Product.query.filter_by(seller_id=seller_id,product_id=productId).first()
	if product:
		category=Category.query.filter(Category.category_id==product.category_id).first()
		prod1={
			"category": {
			"category_id":category.category_id,
			"category_name": category.category_name
			},
			"price": product.price,
			"product_id": product.product_id,
			"product_name": product.product_name,
			"seller_id": product.seller_id
		}
		return {
		"data":prod1,
		}, 200
	return {
		"message":"product id not found",
		}, 404


@app.route('/api/auth/seller/product', methods=['GET'])
@token_required
def getSellerProducts(current_user):
	if current_user.user_role!=2:
		return {
		"message": "Unauthorized Endpoint",
	}, 401
	seller_id=current_user.user_id

	product = Product.query.filter_by(seller_id=seller_id).all()
	res=[]
	if product:
		for i in product:
			category=Category.query.filter(Category.category_id==i.category_id).first()
			prod1={
				"category": {
				"category_id":i.category_id,
				"category_name": category.category_name
				},
				"price": i.price,
				"product_id": i.product_id,
				"product_name": i.product_name,
				"seller_id": i.seller_id
			}
			res.append(prod1)
		return {
		"data":res,
		}, 200

	return{
		"message": "No products for seller present",
		}, 404
	
@app.route('/api/auth/seller/product',methods=["POST"])
@token_required
def addProduct(current_user):
	if current_user.user_role!=2:
		return {
		"message": "Unauthorized Endpoint",
	}, 401
	productId=request.json["product_id"]
	price=request.json["price"]
	productName=request.json["product_name"]
	categoryId=request.json["category_id"]
	
	product = Product.query.filter_by(product_id=productId).first()
	if product:
		return {
		"message": "Product already present",
		}, 409
	else:
		# add product
		productObj=Product(product_id=productId,product_name=productName,price=price,seller_id=current_user.user_id,category_id=categoryId)
		db.session.add(productObj)
		db.session.commit()
		return {
			"response": productId,
		},201


@app.route('/api/auth/seller/product',methods=["PUT"])
@token_required
def putProduct(current_user):
	if current_user.user_role!=2:
		return {
		"message": "Unauthorized Endpoint",
	}, 401
	productId=request.json["product_id"]
	price=request.json["price"]

	product = Product.query.filter_by(seller_id=current_user.user_id, product_id=productId).first()
	if product:
		print(product.price)
		product.price=price
		print("price heree")
		print(product.price)
		db.session.commit()
		return {
			"message": "success",
		},200
	else:
		return {
		"message": "failure",
		}, 404
	

@app.route('/api/auth/seller/product/<id>',methods=["DELETE"])
@token_required
def deleteProduct(current_user,id):
		# Unauthorized access
	if current_user.user_role!=2:
		return {
		"message": "Unauthorized Endpoint",
	}, 401
	product = Product.query.get(id)
	if product:
		db.session.delete(product)
		db.session.commit()
		return {
			"message": "success",
		},200
	else:
		return {
		"message": "failure",
		}, 404



@app.route('/')
def index():
  return 'Index Page'


@app.route('/api/public/login',methods=["POST"])
def login():
	data = request.json

	if not data or not data.get("username") or not data.get("password"):  
		return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

	user = User.query.filter_by(user_name=data.get("username")).first()   
	print(user)

	if user:
		if check_password_hash(user.password, data.get("password")):  
			token = jwt.encode({'user_id': user.user_id, 'exp' :datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")  
			return jsonify({'token' : token},200)
		else:
			return jsonify({'Message' : "Invalid Creds"},401)

	return {
		"message": "Error fetching auth token!, invalid email or password",
		"data": None,
		"error": "Unauthorized"
	}, 401



# @app.route('/api/public/product/search', methods=['GET'])
# def search():
# 	args = request.args
# 	productName = args.get('keyword')
# 	print(productName)
# 	res=[]

# 	products = Product.query.filter(Product.product_name.like('%'+productName+'%')).all()

# 	if len(products)>0:
# 		for i in products:
# 			print(i)
# 			category=Category.query.filter(Category.category_id==i.category_id).first()
# 			print(category)
# 			prod1={
# 				"category": {
# 				"category_id":i.category_id,
# 				"category_name": category.category_name
# 				},
# 				"price": i.price,
# 				"product_id": i.product_id,
# 				"product_name": i.product_name,
# 				"seller_id": i.seller_id
# 			}
# 			res.append(prod1)
# 		print(res)

# 		return {
# 		res,
# 		}, 200


# 	return {
# 		"message": "No product",
# 	}, 400

@app.route('/api/public/product/search', methods=['GET'])
def search_products():
	keyword = request.args.get('keyword')

	# Perform the join operation to retrieve the matching products
	products = db.session.query(Product).join(Category).filter(Product.product_name.contains(keyword)).all()

	if not products:
		return jsonify("Null"), 200
		

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







    # response = {"status": 404, "message": "Users not available"}
    # def put(self, user_id):
    #     user = User.query.filter_by(id=user_id).first()
    #     if user:
    #         user_data = request.get_json()
    #         first_name = user_data["first_name"]
    #         last_name = user_data["last_name"]
    #         email = user_data["email"]
    #         user.first_name = first_name
    #         user.last_name = last_name
    #         user.email = email
    #         db.session.commit()
    #         self.response["status"] = 200
    #         self.response["message"] = "User updated successfully"
    #         return self.response, 200
    #     else:
    #         return self.response, 404
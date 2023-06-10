from ecommerceapp import db
from datetime import datetime

class Product(db.Model):
	product_id=db.Column(db.Integer,primary_key=True)
	product_name=db.Column(db.String(80),nullable=False)
	price=db.Column(db.Float,nullable=False)
	seller_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
	category_id=db.Column(db.Integer, db.ForeignKey('category.category_id'))

	
class Category(db.Model):
	category_id=db.Column(db.Integer,primary_key=True)
	category_name=db.Column(db.String(80),nullable=False)
	products=db.relationship("Product", cascade="all, delete-orphan", backref='category')
	
	
class Cart(db.Model):
	cart_id=db.Column(db.Integer,primary_key=True)
	total_amount=db.Column(db.Float,nullable=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
	cartproducts=db.relationship("CartProduct", cascade="all, delete-orphan", backref='cart')
	
class CartProduct(db.Model):
	cp_id=db.Column(db.Integer,primary_key=True)
	cart_id=db.Column(db.Integer, db.ForeignKey('cart.cart_id'))
	product_id=db.Column(db.Integer, db.ForeignKey('product.product_id'))
	quantity=db.Column(db.Integer)

class Role(db.Model):
	role_id=db.Column(db.Integer,primary_key=True)
	role_name=db.Column(db.String(20),nullable=False)
	users=db.relationship("User", cascade="all, delete-orphan", backref='role')

	
	
class User(db.Model):
	user_id=db.Column(db.Integer,primary_key=True)
	user_name=db.Column(db.String(20),nullable=False)
	password=db.Column(db.String(150),nullable=False)
	user_role=db.Column(db.Integer, db.ForeignKey('role.role_id'))
	cart = db.relationship('Cart', backref='user', uselist=False)
	
		
		

	



	
	






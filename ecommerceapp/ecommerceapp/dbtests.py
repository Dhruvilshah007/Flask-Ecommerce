import pytest
from ecommerceapp import app, db
from flask import Flask, session
from .models import*
from difflib import SequenceMatcher
import string
import base64, json
import random
from flask import Flask, request, jsonify, make_response, session, app, Response,url_for
from ecommerceapp import app, db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate, MigrateCommand

from datetime import datetime,timedelta
import os
from sqlalchemy.orm import sessionmaker
	
import json
import jwt
from functools import wraps
from .models import *
class Test_API:
	client  = app.test_client()

    
	
	

	
	
	@pytest.fixture(autouse=True, scope='session')
	def setUp(self):
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerceapp.db'
	
	#Product table
	def test_product_table(self):
		all_prods=Product.query.all()
		num=0
		for prod in all_prods:
			num=num+1
		assert num==2
	
	#User
	def test_user_table(self):
		all_users=User.query.all()
		num=0
		for useri in all_users:
			num=num+1
		assert num==4
		
	#Category
	def test_category_table(self):
		all_cats=Category.query.all()
		num=0
		for cats in all_cats:
			num=num+1
		assert num==5
		
	#CartProduct
	def test_CartProduct_table(self):
		all_cats=CartProduct.query.all()
		num=0
		for cats in all_cats:
			num=num+1
		assert num==1
		
	#Cart
	def test_Cart_table(self):
		all_cats=Cart.query.all()
		num=0
		for cats in all_cats:
			num=num+1
		assert num==2
		
	#Role
	def test_Role_table(self):
		all_cats=Role.query.all()
		num=0
		for cats in all_cats:
			num=num+1
		assert num==2
		
	#--------Default_values_check---------------
	#Product table
	def test_productvalues_table(self):
		all_prods=Product.query.all()
		output=[]
		for prod in all_prods:
			output.append(prod.product_name)
		output.sort()
		assert output==['crocin','ipad']
	
	#User
	def test_uservalues_table(self):
		all_users=User.query.all()
		output=[]
		for useri in all_users:
			output.append(useri.user_name)
		output.sort()
		assert output==['apple','bob','glaxo','jack']
		
	#Category
	def test_categoryvalues_table(self):
		all_cats=Category.query.all()
		output=[]
		for cats in all_cats:
			output.append(cats.category_name)
		output.sort()
		output1=['Fashion','Electronics','Books','Groceries','Medicines']
		output1.sort()
		assert output==output1
		
	#CartProduct
	def test_CartProduct_table(self):
		all_cats=CartProduct.query.all()
		output=[]
		for cats in all_cats:
			output.append(cats.quantity)
		assert output==[2]
		
	#Cart
	def test_Cartvalues_table(self):
		all_cats=Cart.query.all()
		output=[]
		for cats in all_cats:
			output.append(cats.total_amount)
		output.sort()
		assert output[1]==20
		
	#Role
	def test_Rolevalues_table(self):
		all_cats=Role.query.all()
		output=[]
		for cats in all_cats:
			output.append(cats.role_name)
		output.sort()
		assert output==['CONSUMER','SELLER']
		
	#------------add values test------------
	def test_useradd(self):
		user=User(user_id=5,user_name='test', password='pass_word',user_role=1)
		db.session.add(user)
		db.session.commit()
		added_user=User.query.filter_by(user_id=5).first()
		assert added_user.user_name=='test'
		
	def test_categoryadd(self):
		cat=Category(category_id=6,category_name='testcategory')
		db.session.add(cat)
		db.session.commit()
		added_cat=Category.query.filter_by(category_id=6).first()
		assert added_cat.category_name=='testcategory'
				
		
	def test_productadd(self):
		prod=Product(product_id=3,price=45.90, product_name='testproduct', category_id=6, seller_id=3)
		db.session.add(prod)
		db.session.commit()
		added_prod=Product.query.filter_by(product_id=3).first()
		assert added_prod.product_name=='testproduct'
		
		
	#----------put values test-----------
	
	
	def test_userput(self):
		
		added_user=User.query.filter_by(user_id=5).first()
		added_user.user_name='test1'
		db.session.commit()
		updated_user=User.query.filter_by(user_id=5).first()
		assert updated_user.user_name=='test1'
		
	def test_categoryput(self):
		
		added_cat=Category.query.filter_by(category_id=6).first()
		added_cat.category_name='testcategory1'
		db.session.commit()
		updated_cat=Category.query.filter_by(category_id=6).first()
		
		assert updated_cat.category_name=='testcategory1'
				
		
	def test_productput(self):
		
		added_prod=Product.query.filter_by(product_id=3).first()
		added_prod.product_name='testproduct1'
		db.session.commit()
		updated_prod=Product.query.filter_by(product_id=3).first()
		assert updated_prod.product_name=='testproduct1'
		
	#----------delete values test-----------
	
	
	def test_userdelete(self):
		
		added_user=User.query.filter_by(user_id=5).first()
		db.session.delete(added_user)
		db.session.commit()
		added_user=User.query.filter_by(user_id=5).first()
		print(added_user)
		assert added_user==None
		
		
	def test_categorydelete(self):
		
		added_cat=Category.query.filter_by(category_id=6).first()
		db.session.delete(added_cat)
		db.session.commit()
		added_cat=Category.query.filter_by(category_id=6).first()
		print(added_cat)
		assert added_cat==None
		
				
		
	def test_productdelete(self):
		
		added_prod=Product.query.filter_by(product_id=3).first()
		db.session.delete(added_prod)
		db.session.commit()
		added_prod=Product.query.filter_by(product_id=3).first()
		print(added_prod)
		assert added_prod==None
	
		
	
	
	
	
	
import pytest
from ecommerceapp import app, db
from flask import Flask, session
from .models import*
from difflib import SequenceMatcher
import string
import base64, json
import random
class Test_API:
    
	
	client  = app.test_client()
	word =  ''.join(random.choice(string.ascii_lowercase) for i in range(10)) 
	r1 = random.randint(0, 10)
	id1=1
	id2=2
	
	
	# @pytest.fixture(autouse=True, scope='session')
	# def setUp(self):
	# 	app.config['TESTING'] = True
	# 	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
	# 	from . import seed #//newly added line
			
	
	
	
	#----------------The url /api/public/login test cases-----------------------
	def test_seller_sucess_Login(self):
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		print("creden")
		print(user_credentials)
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		assert response.json['token']
	def test_seller_fail_Login(self):
		url = "/api/public/login"
		user_credentials = 'admin:nopassword'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 401
		#assert response.json['token']


	def test_consumer_sucess_Login(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		assert response.json['token']
		
		
	def test_consumer_fail_Login(self):
		url = "/api/public/login"
		user_credentials = 'bob:nopassword'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code==401	



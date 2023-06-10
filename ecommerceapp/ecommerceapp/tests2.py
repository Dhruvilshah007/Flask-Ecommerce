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
	# from . import seed #//newly added line
			
	
	
	
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


	#---Public endpoint /api/public/product/search	test cases---- ---
	def test_public_endpoint_success(self):
		word='crocin'
		url='/api/public/product/search?keyword='+word
		headers = { 'Content-Type': "application/json"}
		response = self.client.get(url, headers=headers)
		ans=response.get_data(as_text=True).strip()
		check_ans='[{"category":{"category_id":5,"category_name":"Medicines"},"price":10.0,"product_id":2,"product_name":"crocin","seller_id":4}]'
		assert ans==check_ans
		assert response.status_code==200
	def test_public_endpoint_failure(self):
		word1='noooo'
		url='/api/public/product/search?keyword='+word1
		headers = { 'Content-Type': "application/json"}
		response = self.client.get(url, headers=headers)
		
		assert response.status_code==400

#------------------------------------Seller endpoints---------------------------------
#----------------URL /api/auth/seller/product ----testcases
	def test_seller_products_success(self):
		
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/seller/product'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		response1 = self.client.get(url1, headers=headers1)
		ans=response1.get_data(as_text=True).strip()
		check_ans='[{"category":{"category_id":2,"category_name":"Electronics"},"price":29190.0,"product_id":1,"product_name":"ipad","seller_id":3}]'
		assert ans==check_ans
		assert response1.status_code == 200

	def test_seller_products_failure_consumer_login(self):
		
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/seller/product'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		response1 = self.client.get(url1, headers=headers1)
		assert response1.status_code == 403

	def test_seller_products_failure_without_token(self):
		
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/seller/product'
		headers1 = { 'Content-Type': "application/json"  }
		response1 = self.client.get(url1, headers=headers1)
		#assert response1.status_code == 403
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is missing")
		match = round(s.ratio(), 3)
		assert match > 0.8
	def test_seller_products_failure_invalid_token(self):
		
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token='invalidtokeninput'
		
		url1='/api/auth/seller/product'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		response1 = self.client.get(url1, headers=headers1)
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is invalid")
		match = round(s.ratio(), 3)
		assert match > 0.8

# URL-----------/api/auth/seller/product/<prodid> testcases-------
	def test_seller_single_product_success(self):

		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/seller/product/1'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		response1 = self.client.get(url1, headers=headers1)
		print(response1)
		ans=response1.get_data(as_text=True).strip()
		print(ans)
		check_ans='[{"category":{"category_id":2,"category_name":"Electronics"},"price":29190.0,"product_id":1,"product_name":"ipad","seller_id":3}]'
		assert ans==check_ans
		assert response1.status_code == 200
	def test_seller_single_product_failure_different_seller(self):

		url = "/api/public/login"
		user_credentials = 'glaxo:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/seller/product/1'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		response1 = self.client.get(url1, headers=headers1)
		#ans=response1.get_data(as_text=True).strip()
		#print(ans)
		#check_ans='[{"category":{"category_id":2,"category_name":"Electronics"},"price":29190.0,"product_id":1,"product_name":"ipad","seller_id":3}]'
		#assert ans==check_ans
		assert response1.status_code == 404
	def test_seller_single_product_failure_consumer_login(self):

		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/seller/product/1'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		response1 = self.client.get(url1, headers=headers1)
		#ans=response1.get_data(as_text=True).strip()
		#print(ans)
		#check_ans='[{"category":{"category_id":2,"category_name":"Electronics"},"price":29190.0,"product_id":1,"product_name":"ipad","seller_id":3}]'
		#assert ans==check_ans
		assert response1.status_code == 403

	def test_seller_single_product_failure_invalid_token(self):

		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token='invalid token'
		
		url1='/api/auth/seller/product/1'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		response1 = self.client.get(url1, headers=headers1)
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is invalid")
		match = round(s.ratio(), 3)
		assert match > 0.8
	
	def test_seller_single_product_failure_without_token(self):

		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/seller/product/1'
		headers1 = { 'Content-Type': "application/json"}
		response1 = self.client.get(url1, headers=headers1)
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is missing")
		match = round(s.ratio(), 3)
		assert match > 0.8

	#URL-------/api/auth/seller/product------
	def test_seller_add_product_success(self):
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/seller/product'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":3,	"product_name":"phone",	"price":80000,	"category_id":2}'
		response1 = self.client.post(url1, headers=headers1,data=payload1)
		ans=response1.get_data(as_text=True).strip()
		print(254,ans)
		check_ans='[{"category":{"category_id":2,"category_name":"Electronics"},"price":29190.0,"product_id":1,"product_name":"ipad","seller_id":3}]'
		assert ans=='3'
		assert response1.status_code == 201
	def test_seller_add_product_failure_consumer(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/seller/product'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":3,	"product_name":"phone",	"price":80000,	"category_id":2}'
		response1 = self.client.post(url1, headers=headers1,data=payload1)
		assert response1.status_code == 403
	
	def test_seller_add_product_failure_sameproductagain(self):
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/seller/product'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":3,	"product_name":"phone",	"price":80000,	"category_id":2}'
		response1 = self.client.post(url1, headers=headers1,data=payload1)
		assert response1.status_code == 409
	#-----------URL	/api/auth/seller/product -----PUT-------
	def test_seller_update_product_success(self):
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']

		url1='/api/auth/seller/product'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":3,	"price":8768678}'
		response1 = self.client.put(url1, headers=headers1,data=payload1)
		assert response1.status_code == 200
	def test_seller_update_product_failure_another_seller(self):
		url = "/api/public/login"
		user_credentials = 'glaxo:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']

		url1='/api/auth/seller/product'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":3,	"price":8768678}'
		response1 = self.client.put(url1, headers=headers1,data=payload1)
		assert response1.status_code == 404
	def test_seller_update_product_failure_consumer(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']

		url1='/api/auth/seller/product'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":3,	"price":8768678}'
		response1 = self.client.put(url1, headers=headers1,data=payload1)
		assert response1.status_code == 403
	
#------/api/auth/seller/product/<prodid>---DELETE TEST CASEs---
	def test_seller_delete_product_failure_anotherseller(self):
		url = "/api/public/login"
		user_credentials = 'glaxo:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']

		url1='/api/auth/seller/product/3'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		
		response1 = self.client.delete(url1, headers=headers1)
		assert response1.status_code == 404

	def test_seller_delete_product_failure_consumer(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']

		url1='/api/auth/seller/product/3'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		
		response1 = self.client.delete(url1, headers=headers1)
		assert response1.status_code == 403
	def test_seller_delete_product_success(self):
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']

		url1='/api/auth/seller/product/3'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		
		response1 = self.client.delete(url1, headers=headers1)
		assert response1.status_code == 200


#--------------------------Consumer Endpoints
#-------/api/auth/consumer/cart testcases-------------------
	def test_consumer_cart_success(self):
		
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		response1 = self.client.get(url1, headers=headers1)
		ans=response1.get_data(as_text=True).strip()
		print(384,ans)
		check_ans='[{"cart_id":1,"cartproducts":{"cp_id":1,"product":{"category":{"category_id":5,"category_name":"Medicines"},"price":10.0,"product_id":2,"product_name":"crocin"}},"total_amount":20.0}]'
		assert ans==check_ans
		assert response1.status_code == 200

	
	def test_consumer_cart_failure_seller_login(self):
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		response1 = self.client.get(url1, headers=headers1)
		assert response1.status_code == 403

	def test_consumer_cart_failure_without_token(self):
		
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json"  }
		response1 = self.client.get(url1, headers=headers1)
		#assert response1.status_code == 403
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is missing")
		match = round(s.ratio(), 3)
		assert match > 0.8
	def test_consumer_cart_failure_invalid_token(self):
		
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token='invalidtokeninput'
		
		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		response1 = self.client.get(url1, headers=headers1)
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is invalid")
		match = round(s.ratio(), 3)
		assert match > 0.8

#-------/api/auth/consumer/cart POST testcases-------------------
	def test_consumer_add_product_success(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":1,	"quantity":1}'
		response1 = self.client.post(url1, headers=headers1,data=payload1)
		ans=response1.get_data(as_text=True).strip()
		print(451,ans)
		check_ans='[{"category":{"category_id":2,"category_name":"Electronics"},"price":29190.0,"product_id":1,"product_name":"ipad","seller_id":3}]'
		assert ans=='29210.0'
		assert response1.status_code == 200
	def test_consumer_add_product_failure_sameproduct(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":2,	"quantity":2}'
		response1 = self.client.post(url1, headers=headers1,data=payload1)
		assert response1.status_code == 409
		
	def test_consumer_add_product_failure_seller_login(self):
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":2,	"quantity":2}'
		response1 = self.client.post(url1, headers=headers1,data=payload1)
		assert response1.status_code == 403
		
	def test_consumer_add_product_failure_token_invalid(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token='invalid'
		
		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":2,	"quantity":2}'
		response1 = self.client.post(url1, headers=headers1,data=payload1)
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is invalid")
		match = round(s.ratio(), 3)
		assert match > 0.8
	def test_consumer_add_product_failure_token_missing(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']
		
		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json"}
		payload1='{	"product_id":2,	"quantity":2}'
		response1 = self.client.post(url1, headers=headers1,data=payload1)
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is missing")
		match = round(s.ratio(), 3)
		assert match > 0.8

#---------------------/api/auth/consumer/cart------------PUT----------------	
	def test_consumer_update_product_success(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']

		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":1,	"quantity":2}'
		response1 = self.client.put(url1, headers=headers1,data=payload1)
		ans=response1.get_data(as_text=True).strip()
		print(530,ans)
		#check_ans='[{"category":{"category_id":2,"category_name":"Electronics"},"price":29190.0,"product_id":1,"product_name":"ipad","seller_id":3}]'
		assert ans=='58400.0'
		assert response1.status_code == 200
		
	def test_consumer_update_product_failure_seller_login(self):
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']

		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":1,	"quantity":2}'
		response1 = self.client.put(url1, headers=headers1,data=payload1)
		assert response1.status_code == 403
	def test_consumer_update_product_failure_invalid_token(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token='invalid'

		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":1,	"quantity":2}'
		response1 = self.client.put(url1, headers=headers1,data=payload1)
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is invalid")
		match = round(s.ratio(), 3)
		assert match > 0.8
		
	def test_consumer_update_product_failure_missing_token(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token='invalid'

		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json" }
		payload1='{	"product_id":1,	"quantity":2}'
		response1 = self.client.put(url1, headers=headers1,data=payload1)
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is missing")
		match = round(s.ratio(), 3)
		assert match > 0.8
##---------------------/api/auth/consumer/cart------------DELETE------------
	def test_consumer_delete_product_failure_seller_login(self):
		url = "/api/public/login"
		user_credentials = 'apple:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']

		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":1}'
		response1 = self.client.delete(url1, headers=headers1,data=payload1)		
		assert response1.status_code == 403
		
	def test_consumer_delete_product_failure_invalid_token(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token='invalid'

		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":1}'
		response1 = self.client.delete(url1, headers=headers1,data=payload1)		
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is invalid")
		match = round(s.ratio(), 3)
		assert match > 0.8
		
	def test_consumer_delete_product_failure_invalid_token(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']


		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json"}
		payload1='{	"product_id":1}'
		response1 = self.client.delete(url1, headers=headers1,data=payload1)		
		assert response1.status_code == 401
		s = SequenceMatcher(lambda x: x == " ", response1.json['Message'].strip(), "Token is missing")
		match = round(s.ratio(), 3)
		assert match > 0.8
	def test_consumer_delete_product_success(self):
		url = "/api/public/login"
		user_credentials = 'jack:pass_word'
		valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
		response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
		assert response.status_code == 200
		token=response.json['token']


		url1='/api/auth/consumer/cart'
		headers1 = { 'Content-Type': "application/json",  'x-access-token': ""+token  }
		payload1='{	"product_id":1}'
		response1 = self.client.delete(url1, headers=headers1,data=payload1)
		ans=response1.get_data(as_text=True).strip()
		print(644,ans)
		check_ans='[{"category":{"category_id":2,"category_name":"Electronics"},"price":29190.0,"product_id":1,"product_name":"ipad","seller_id":3}]'
		assert ans=='20.0'
		assert response1.status_code == 200
	


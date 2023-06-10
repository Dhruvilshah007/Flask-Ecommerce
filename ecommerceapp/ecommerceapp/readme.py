# @app.route('/api/auth/consumer/cart', methods=['GET'])
# @token_required
# def getCart(current_user):

# 	# print(current_user.user_id)
# 	# print(current_user.user_name)
# 	# print(current_user.user_role)

# 	if current_user.user_role!=1:
# 		return {
# 			"message": "Unauthorized Endpoint",
# 		}, 401


# 	res=[]

# 	# cart = Cart.query.filter_by(user_id=current_user.user_id).first()
# 	# cartProduct=CartProduct.query.filter_by(cart_id=cart.cart_id).first()

# 	# product=Product.query.filter_by(product_id=cartProduct.product_id).first()
# 	# category=Category.query.filter(category_id=product.category_id).first()

# 	# print(cart)
# 	# print(cartProduct)
# 	# print(product)
# 	# print(category)
# 	# print(query)

# 	# for i in product:
# 	# 	print("category id here")
# 	# 	print(i.category_id)
# 	# 	category=Category.query.filter(category_id=i.category_id).first()
# 	# 	print(category)
# 	# 	prod1={
# 	# 		"price": i.price,
# 	# 		"product_id": i.product_id,
# 	# 		"product_name": i.product_name,
# 	# 		"category": {
# 	# 			"category_id":i.category_id,
# 	# 			"category_name": category.category_name
# 	# 		},

# 	# 	}
# 	# print(prod1)

# 	# {
#     # "cartproducts": {
#     #     "product": {
#     #         "product_id": 2,
#     #         "price": 10.0,
#     #         "product_name": "crocin",
#     #         "category": {
#     #             "category_name": "Medicines",
#     #             "category_id": 5
#     #         }
#     #     },
#     #     "cp_id": cartProduct.cp_id
#     # },
#     # "cart_id": cart.cart_id,
#     # "total_amount": cart.total_amount
# 	# }

# 	return "hii"

# @app.route('/api/auth/consumer/cart',methods=["POST"])
# @token_required
# def consumerCart(current_user):

# 	# Unauthorized access
# 	if current_user.user_role!=1:
# 		return {
# 		"message": "Unauthorized Endpoint",
# 	}, 401

# 	data = request.json
# 	print(data.get("product_id"))
# 	print(data.get("quantity"))

# 	return "consumerCart"
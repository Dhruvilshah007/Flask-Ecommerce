from werkzeug.security import generate_password_hash
from . import db
from .models import Product, Role, Cart, CartProduct, Category,User

db.drop_all()
db.session.commit()
try:
    db.drop_all()
    db.create_all()
    c1=Category(category_name='Fashion')
    db.session.add(c1)
    db.session.commit()

    c2=Category(category_name='Electronics')
    db.session.add(c2)
    db.session.commit()

    c3=Category(category_name='Books')
    db.session.add(c3)
    db.session.commit()

    c4=Category(category_name='Groceries')
    db.session.add(c4)
    db.session.commit()

    c5=Category(category_name='Medicines')
    db.session.add(c5)
    db.session.commit()


    r1=Role(role_name='CONSUMER')
    db.session.add(r1)
    db.session.commit()

    r2=Role(role_name='SELLER')
    db.session.add(r2)
    db.session.commit()

    password=generate_password_hash("pass_word",method='pbkdf2:sha256',salt_length=8)
    u1=User(user_name='jack',password=password,user_role=1)
    db.session.add(u1)
    db.session.commit()

    u2=User(user_name='bob',password=password,user_role=1)
    db.session.add(u2)
    db.session.commit()

    u3=User(user_name='apple',password=password,user_role=2)
    db.session.add(u3)
    db.session.commit()

    u4=User(user_name='glaxo',password=password,user_role=2)
    db.session.add(u4)
    db.session.commit()

    cart1=Cart(total_amount=20, user_id=1)
    db.session.add(cart1)
    db.session.commit()

    cart2=Cart(total_amount=0, user_id=2)
    db.session.add(cart2)
    db.session.commit()

    p1=Product(price=29190,product_name='ipad',category_id=2,seller_id=3)
    db.session.add(p1)
    db.session.commit()
    p2=Product(price=10,product_name='crocin',category_id=5,seller_id=4)
    db.session.add(p2)
    db.session.commit()

    cp1=CartProduct(cart_id=1,product_id=2,quantity=2)
    db.session.add(cp1)
    db.session.commit()
    print('database successfully initialized')
except Exception:
    db.session.rollback()
    print('error in adding data to db')




import base64

user_credentials = 'jack:pass_word'
valid_credentials = base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')

print(valid_credentials)
print(str(base64.b64decode(valid_credentials))[2:-1])


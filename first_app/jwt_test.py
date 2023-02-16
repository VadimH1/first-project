import jwt

SECRET = '12344555'

token_data = {'user_id': '1'}

access_token = jwt.encode(token_data, SECRET, algorithm='HS256')
print(access_token)

payload = jwt.decode(access_token, SECRET, algorithms=["HS256"])
assert payload == token_data
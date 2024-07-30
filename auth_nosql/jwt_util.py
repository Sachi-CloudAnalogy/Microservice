import jwt
import datetime

SECRET_KEY = 'your_secret_key'

def generate_jwt(email):
    payload = {
        'email': str(email),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['email']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

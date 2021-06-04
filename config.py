import random
import string

API_HOST = '127.0.0.1'
API_PORT = 5000
API_BASE_URL = '/api'

LOGIN_TESTE = 'admin@admin.com'
SENHA_TESTE = 'Admin1234@'

# Gera uma chave aleatória para geração do JWT
gen = string.ascii_letters + string.digits + string.ascii_uppercase
SECRET_KEY = ''.join(random.choice(gen) for i in range(32))


DEBUG = True
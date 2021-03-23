import os
import pytz
from dotenv import load_dotenv
load_dotenv()

# TIBBER
TIBBER_URL = os.getenv('TIBBER_URL', default='https://api.tibber.com/v1-beta/gql')
TIBBER_TOKEN = os.getenv('TIBBER_TOKEN', default='your_secret_tibber_token_here')
TIBBER_HEADERS = {
    'Authorization': f'Bearer {TIBBER_TOKEN}',
    'Content-Type': 'application/json'
}

# My WebCore Piston
PISTON_URL = TOKEN = os.getenv('PISTON_URL', default='your_secret_webcore_url_here')
TZ = pytz.timezone('Europe/Oslo')
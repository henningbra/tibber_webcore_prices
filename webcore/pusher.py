import requests
import settings


def update_piston(data):
    requests.post(settings.PISTON_URL, data=data)
    

if __name__ == "__main__":

    update_piston(level='test')



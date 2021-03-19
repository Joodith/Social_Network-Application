from django.conf import settings
import requests

def send_verification_code(user):
    data={
        'api_key':settings.AUTHY_KEY,
        'via':'sms',
        'country_code':'+91',
        'phone_number':user.phone_no,
    }
    url = 'https://api.authy.com/protected/json/phones/verification/start'
    response=requests.post(url,data=data)
    return response

def verify_code_sent(otp,user):
    data={
        'api_key':settings.AUTHY_KEY,
        'country_code': '+91',
        'phone_number':user.phone_no,
        'verification_code':otp,
    }
    url = 'https://api.authy.com/protected/json/phones/verification/check'
    response=requests.get(url,data=data)
    return response


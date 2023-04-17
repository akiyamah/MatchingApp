import random
import string

from .models import User

def create_account_id(email):
    local_part = email.split('@')[0]
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return local_part + random_string

def create_user_by_google(strategy, details, response, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = {
        'email': details['email'],
        'first_name': details['first_name'],
        'last_name': details['last_name'],
    }

    account_id = create_account_id(details['email'])
    fields['account_id'] = account_id

    if 'verified_email' in response and response['verified_email']:
        fields['is_active'] = True

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }

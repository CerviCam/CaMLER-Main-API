from urllib import parse
from urllib.request import urlopen, Request
import json

def fetch(
    url,
    header = {},
    body = {},
    method = 'GET',
):
    header = {} if header == None else header
    data = json.dumps(body).encode()
    print(data)
    return urlopen(Request(
        url = url,
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            **header,
        },
        data = data,
        method = method,
    )).read().decode()

def get_user_or_none(request):
    if request.user.is_authenticated:
        account = request.user
        user = account.user
        return user
    else:
        return None

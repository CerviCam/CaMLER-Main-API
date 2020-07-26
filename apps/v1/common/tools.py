from urllib import parse
from urllib.request import urlopen, Request

def fetch(
    url,
    headers = {},
    body = {},
    method = 'GET',
):
    headers = {} if headers == None else headers
    data = parse.urlencode(body).encode()
    return urlopen(Request(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            **headers,
        },
        data = data,
        method = method,
    )).read().decode()


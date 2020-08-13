from shutil import move
import os

def get_user_or_none(request):
    if request.user.is_authenticated:
        account = request.user
        user = account.user
        return user
    else:
        return None

def move_file(old_path, new_path):
    dirname = os.path.dirname(new_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    move(old_path, new_path)

"""
Deprecated function, feel free to uncomment if you want to modify/use it
"""
# from urllib.request import urlopen, Request
# from requests_toolbelt import MultipartEncoder
# def fetch(
#     url,
#     header = {},
#     body = {},
#     method = 'GET',
# ):
#     # data = json.dumps(body).encode()
#     data = MultipartEncoder(fields = body)
#     return urlopen(Request(
#         url = url,
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
#             **header,
#         },
#         # files = files,
#         data = data,
#         method = method,
#     )).read().decode()

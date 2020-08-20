from shutil import move
import os
from django.utils import timezone
from django.utils.deconstruct import deconstructible

def get_user_or_none(request):
    if request.user.is_authenticated:
        account = request.user
        user = account.user
        return user
    else:
        return None

def get_object_or_none(model, *args, **kwargs):
    try:
        object = model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
    return object

def move_file(old_path, new_path):
    dirname = os.path.dirname(new_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    move(old_path, new_path)

def rename_file_name(instance, field_name, new_name, should_save=True):
    new_file_name = os.path.join(
        os.path.dirname(getattr(instance, field_name).name),
        new_name,
    )
    new_file_path = os.path.join(
        os.path.dirname(getattr(instance, field_name).path),
        new_name,
    )
    print(new_name, getattr(instance, field_name).path, new_file_path)
    move_file(getattr(instance, field_name).path, new_file_path)
    getattr(instance, field_name).name = new_file_name
    
    if should_save:
        instance.save()
    
    return instance

def get_date_format(instance, file_name):
        ext = file_name.split('.')[-1]
        file_name = "{}.{}".format(timezone.now().strftime("%Y %m %d %H:%M:%S"), ext)
        return file_name

@deconstructible
class DefaultFileNameFormat(object):
    def __init__(self, prefix="", suffix=""):
        self.prefix = prefix
        self.suffix = suffix

    def __call__(self, instance, filename):
        file_name = os.path.join(
            self.prefix,
            get_date_format(instance, filename),
            self.suffix,
        )

        if file_name.endswith('/'):
            return file_name[:-1]
        return file_name

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

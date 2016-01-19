'''
This is the actual lambda fuction that will get called. The actual image
processing will happen in a seperate process since the LD_LIBRARY_PATH
environment variable needs to be adjusted for our bundled openCV
'''


import tempfile
import base64
import subprocess
import json
import boto
import os.path
import os
import requests


dummyfile = '/home/bashton/Desktop/profile.jpg'
libdir = './lib'
aws_bucket = 'puppyfacetrain'
aws_model_key = 'eigenModel.xml'
model_path = '/tmp/model_v1.xml'


def puppyhandler(event, context):
    fileb64 = event['file']

    img_file = tempfile.NamedTemporaryFile(delete=False)
    img_file.write(base64.b64decode(fileb64))
    img_file.close()
    print(img_file.name)

    init_model()
    results = wrapper(img_file.name)

    os.remove(img_file.name)

    return results


def apihandler(event, context):
    url = event['imgUrl']
    img_file = tempfile.NamedTemporaryFile(delete=False)

    resp = requests.get(url)

    if resp.status_code != 200:
        return {"error": "Could not fetch image"}

    if resp.headers['Content-Type'] not in ['image/jpeg', 'image/png']:
        return {"error": "Invalid img type"}

    img_file.write(resp.content)
    img_file.close()
    print(img_file.name)

    init_model()
    results = wrapper(img_file.name)

    os.remove(img_file.name)

    return results


def init_model():
    if not os.path.isfile(model_path):
        print("Fetch model")
        conn = boto.connect_s3(anon=True)
        b = conn.get_bucket(aws_bucket)
        k = b.get_key(aws_model_key)
        k.get_contents_to_filename(model_path)
    else:
        print("Model already exists")


def wrapper(img_file):
    result_file = tempfile.NamedTemporaryFile(delete=False)
    result_file.close()

    command = ('LD_LIBRARY_PATH={} python2.7 recognizeface.py ' + \
              '-i "{}" --result_out "{}" -m "{}" -t 100000')\
              .format(libdir,img_file, result_file.name, model_path)
    print(command)
    output = subprocess.check_output(command, shell=True)
    print('Shell output ', output)
    with open(result_file.name, 'r') as resultf:
        results = json.load(resultf)
    print(results)
    os.remove(result_file.name)
    return results


if __name__ == '__main__':
    with open(dummyfile, 'rb') as test_file:
        fileb64 = base64.b64encode(test_file.read())
    event = {'file':fileb64}
    puppyhandler(event, None)

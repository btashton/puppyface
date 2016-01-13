import requests
import os
import time


api_key = os.environ['CSE_API_KEY']
search_engine_id = '003446489956207928063:buup1fjpixg'
url = 'https://www.googleapis.com/customsearch/v1'
fields = 'items(mime,link)'
url_param = {
    'searchType':'image',
    'key':api_key,
    'cx':search_engine_id,
    'fields':fields
    }


def get_image_urls(query, count):
    results = []
    params = url_param
    params['q'] = query
    start = 1
    while count > 0:
        url_param['start'] = start
        if count > 10:
            url_param['num'] = 10
            count -= 10
            start += 10
        else:
            url_param['num'] = count
            count = 0
        try:
            r = requests.get(url, params=url_param)
            results += r.json()['items']
        except:
            print(r.json())
            return results
        time.sleep(1.5)
    return results


def download_img(path, url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def save_img_set(base_path, imgs):
    try:
        os.makedirs(base_path)
    except:
        pass
    idx = 0
    for img in imgs:
        if img['mime'] == 'image/jpeg':
            ext = 'jpg'
        elif img['mime'] == 'image/png':
            ext = 'png'
        else:
            continue
        try:
            download_img('%s/%d.%s'%(base_path,idx,ext), img['link'])
        except:
            continue
        idx += 1


def main():
    img_count = 100
    characters = [
#        'Darth Vader',
#        'Obi-Wan Kenobi',
        'Luke Skywalker',
        'Han Solo',
        'Yoda',
#        'Darth Maul',
#        'Boba Fett',
        'Chewbacca',
        'Anakin Skywalker',
#        'Boss Nass',
#        'Dexter Jettster',
        'Princess Leia Organa',
        'Mace Windu',
        'Emperor Palpatine',
        'C-3PO',
#        'General Grievous',
        'Qui-Gon Jinn',
        'Darth Sidious',
#        'Revan',
#        'Jango Fett',
        'Lando Calrissian']
    for char in characters:
        print("Getting images for: %s"%char)
        imgs = get_image_urls(char, img_count)
        save_img_set('/tmp/imgset/%s/'%(char,), imgs)


if __name__ == '__main__':
    main()


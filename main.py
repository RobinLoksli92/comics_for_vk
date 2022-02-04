import os
import random
from urllib.error import HTTPError
from urllib.parse import urlsplit, unquote

from dotenv import load_dotenv
import requests


def check_vk_response(content):
    try:
        error_code = content['error']['error_code']
        error_text = content['error']['error_msg']
        raise requests.HTTPError(f'Code: {error_code}. Error: {error_text}.')
    except KeyError:
        return


def get_upload_url(vk_access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': vk_access_token,
        'v': '5.131',
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    content = response.json()
    check_vk_response(content)
    upload_url = content['response']['upload_url']
    return upload_url


def load_comics(upload_url, comics_name):
    with open(comics_name, 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    content = response.json()
    check_vk_response(content)
    uploaded_image_server = content['server']
    uploaded_image_photo = content['photo']
    uploaded_image_hash = content['hash']
    return uploaded_image_server, uploaded_image_photo, uploaded_image_hash
    

def save_comics_on_wall(vk_access_token, uploaded_image_server, uploaded_image_photo, uploaded_image_hash):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    
    params = {
        'access_token':vk_access_token,
        'v': '5.131',
        'server': uploaded_image_server,
        'photo': uploaded_image_photo,
        'hash': uploaded_image_hash
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    content = response.json()
    check_vk_response(content)
    owner_id = content["response"][0]["owner_id"]
    media_id = content["response"][0]["id"]
    return owner_id, media_id


def publish_comics(vk_access_token, owner_id, media_id, comics_title, vk_group_id, comics_comment):
    url = 'https://api.vk.com/method/wall.post'

    params = {
        'v': '5.131',
        'access_token': vk_access_token,
        'owner_id': f'-{vk_group_id}',
        'message': f'{comics_title}.\n{comics_comment}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    content = response.json()
    check_vk_response(content)
    response.raise_for_status()


def get_latest_comics_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    latest_comics_number = response.json()['num']
    return latest_comics_number


def save_image(image_link):
    parsed_image_link = urlsplit(image_link)
    image_name = os.path.split(parsed_image_link[2])
    comics_name = unquote(image_name[1])
    response = requests.get(image_link)
    response.raise_for_status()
    with open(comics_name, 'wb') as file:
        file.write(response.content)
    return comics_name


def get_comics_page(comics_number):
    url = f'https://xkcd.com/{comics_number}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()
    comics_page = response.json()
    return comics_page
    

def main():
    load_dotenv()
    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    comics_page = get_comics_page(random.randint(1, get_latest_comics_number()))
    image_link = comics_page['img']
    comics_title = comics_page['safe_title']
    try:
        comics_name = save_image(image_link)
        comics_comment = comics_page['alt']
        upload_url = get_upload_url(vk_access_token)
        uploaded_image_server, uploaded_image_photo, uploaded_image_hash = load_comics(upload_url, comics_name)
        owner_id, media_id = save_comics_on_wall(vk_access_token, uploaded_image_server, uploaded_image_photo, uploaded_image_hash)
        publish_comics(vk_access_token, owner_id, media_id, comics_title, vk_group_id, comics_comment)
    except HTTPError:
        print('Ошибочка закралась')
    finally:
        os.remove(comics_name)


if __name__ == '__main__':
    main()
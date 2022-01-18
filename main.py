import os
import random

from dotenv import load_dotenv
import requests


def get_upload_url(vk_access_token):
    url = f'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': vk_access_token,
        'v': '5.131',
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response = response.json()
    upload_url = response['response']['upload_url']
    return upload_url


def load_comics(upload_url):
    with open('comics.png', 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    uploaded_image = response.json()
    uploaded_image_server = uploaded_image['server']
    uploaded_image_photo = uploaded_image['photo']
    uploaded_image_hash = uploaded_image['hash']
    return uploaded_image_server, uploaded_image_photo, uploaded_image_hash


def save_comics_on_wall(vk_access_token, uploaded_image_server, uploaded_image_photo, uploaded_image_hash):
    url = f'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token':{vk_access_token},
        'v': '5.131',
        'server': uploaded_image_server,
        'photo': uploaded_image_photo,
        'hash': uploaded_image_hash
    }

    response = requests.post(url, params=params)
    response.raise_for_status()
    image_params = response.json()
    owner_id = image_params["response"][0]["owner_id"]
    media_id = image_params["response"][0]["id"]
    return owner_id, media_id


def publish_comics(vk_access_token, owner_id, media_id, comics_title, vk_group_id, comics_comment):
    url = f'https://api.vk.com/method/wall.post'    
    params = {
        'v': '5.131',
        'access_token': vk_access_token,
        'owner_id': f'-{vk_group_id}',
        'message': f'{comics_title}.{comics_comment}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()


def get_latest_comics_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    latest_comics_number = response.json()['num']
    return latest_comics_number


def save_image(image_link):
    comics_name = 'comics.png'
    response = requests.get(image_link)
    response.raise_for_status()
    with open(comics_name, 'wb') as file:
        file.write(response.content)

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
        save_image(image_link)
        comics_comment = comics_page['alt']
        upload_url = get_upload_url(vk_access_token)
        uploaded_image_server, uploaded_image_photo, uploaded_image_hash = load_comics(upload_url)
        owner_id, media_id = save_comics_on_wall(vk_access_token, uploaded_image_server, uploaded_image_photo, uploaded_image_hash)
        publish_comics(vk_access_token, owner_id, media_id, comics_title, vk_group_id, comics_comment)
    finally:
        os.remove('comics.png')


if __name__ == '__main__':
    main()
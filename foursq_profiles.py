# -*-coding: utf-8-*-
import json
from foursq_utils import *



sys_api_token = 0
sys_client_version = 0


def cut_from_to(line, after_tag, left_tag, right_tag):
    p0 = line.find(after_tag)
    p1 = line.find(left_tag, p0) + len(left_tag)
    p2 = line.find(right_tag, p1)
    return line[p1: p2]


def retrieve_api_keys(line):
    API_TOKEN = 'API_TOKEN'
    CLIENT_VERSION = 'CLIENT_VERSION'
    api_token = cut_from_to(line, API_TOKEN, '\'', '\'')
    client_version = cut_from_to(line, CLIENT_VERSION, '\'', '\'')

    return api_token, client_version


def fetch_anonymous_token():
    global sys_api_token, sys_client_version
    content = get_raw_info("http://foursquare.com/")
    if content == -1 or content == -2:
        return 'missing', 0

    content = content.split("\n")

    for line in content:
        if 'window.fourSq.config.api' in line:
            sys_api_token, sys_client_version = retrieve_api_keys(line)
            break


def fetch_user_profile(UID):
    if sys_client_version == 0 or sys_api_token == 0:
        fetch_anonymous_token()

    url = 'https://api.foursquare.com/v2/users/' + str(UID) + '?oauth_token=' + str(sys_api_token) + '&v=' + str(
        sys_client_version)
    try:
        raw = get_raw_info(url)
        data = json.loads(raw)
        if data['meta']['code'] != 200:
            return -1
        data = data['response']['user']
        user_info = {}
        user_info.setdefault('exist', 1)
        user_info.setdefault('user id', str(UID))
        user_info.setdefault('imgURL', data['photo']['prefix'] + '256x256' + data['photo']['suffix'])
        user_info.setdefault('address', data['homeCity'])
        
        if data['gender'] == 'male':
            gender = 'm'
        elif data['gender'] == 'female':
            gender = 'f'
        else:
            gender = '-'
        user_info.setdefault('gender', gender)
        return user_info
    except:
        return -1


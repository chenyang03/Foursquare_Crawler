# -*- coding: utf-8 -*-
import json
import guess_language
from textblob import TextBlob
from foursq_utils import *


def get_venue_category(venue_category_name):
    if venue_category_name in category_Arts_Entertainment:
        return 'Arts_Entertainment'
    elif venue_category_name in category_College_University:
        return 'College_University'
    elif venue_category_name in category_Event:
        return 'Event'
    elif venue_category_name in category_Food:
        return 'Food'
    elif venue_category_name in category_Nightlife_Spot:
        return 'Nightlife_Spot'
    elif venue_category_name in category_Outdoors_Recreation:
        return 'Outdoors_Recreation'
    elif venue_category_name in category_Professional_Other_Places:
        return 'Professional_Other_Places'
    elif venue_category_name in category_Residence:
        return 'Residence'
    elif venue_category_name in category_Shop_Service:
        return 'Shop_Service'
    elif venue_category_name in category_Travel_Transport:
        return 'Travel_Transport'
    else:
        return 'unknown'


def fetch_usr_tips(user_id):
    success = 0
    retry = 0
    content = ''
    while success == 0:
        try:
            super_token = 'QEJ4AQPTMMNB413HGNZ5YDMJSHTOHZHMLZCAQCCLXIX41OMP'
            fetch_url_str = 'https://api.foursquare.com/v2/users/' + str(user_id) + '/tips?oauth_token='+super_token + \
                            '&limit=5000&v=20141231'
            content = get_raw_info(fetch_url_str)
            if content != -1 and content != -2:
                success = 1
        except:
            time.sleep(3)
            retry += 1
            if retry == AUTO_RECONNECT_TIMES:
                return -2
    output_dict = {}
    content_json = json.loads(content)
    output_dict['tips content'] = []
    a = {}
    if content_json['meta']['code'] != 200:
        output_dict['error_meta'] = str(content_json['meta']['code'])
        if str(content_json['meta']['errorDetail']) == "Must provide a valid user ID or 'self.'":
            output_dict['user existence'] = '-1'
        return output_dict

    output_dict['count'] = content_json['response']['tips']['count']
    for item in (content_json['response']['tips']['items']):
        if 'cc' in item['venue']['location']:
            venue_country = item['venue']['location']['cc']
        else:
            venue_country = '-'
        a = {}
        a['len'] = len(item['text'])
        a['text'] = item['text'].encode('utf-8')
        a['venue name'] = item['venue']['name'].encode('utf-8')
        a['timespam'] = str(item['createdAt'])
        a['venue country'] = venue_country

        if 'photo' in item:
            a['photo'] = "y "
        else:
            a['photo'] = "n "
        cate_info = item['venue']['categories']
        if len(cate_info) > 0:
            for xx in cate_info:
                a['category'] = get_venue_category(xx['name'])
        else:
            a['category'] = '-'

        tip_text = a['text']
        tip_language = guess_language.guessLanguage(tip_text)
        if tip_language == 'en':
            testimonial = TextBlob(tip_text)
            polarity = testimonial.sentiment.polarity
            a['polarity'] = polarity
        else:
            a['polarity'] = '-'
        output_dict['tips content'].append(a)
    return output_dict


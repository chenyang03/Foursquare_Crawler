# -*-coding: utf-8-*-
import json
import codecs
import foursq_profiles
import foursq_tips
import random

#sys_api_token = 0
#sys_client_version = 0
min_id = 1
max_id = 532419618
total_user = 0
valid_user = 0
users_with_tips = 0
users_w_tips = 0

def get_json(user_id):
    global users_w_tips
    crawl_tips = {}
    crawl_tips['user info'] = foursq_profiles.fetch_user_profile(user_id)
    if crawl_tips['user info'] != -1:
        crawl_tips['tips'], users_w_tips = foursq_tips.fetch_usr_tips(user_id)
    else:
        return -1
    return crawl_tips


def run(start_point, finish_point, step):
    global valid_user
    global users_with_tips
    global users_w_tips
    output_file = codecs.open("4sq_tips_chunk_%d_to_%d.txt" % (start_point, finish_point), "w", "utf-8-sig")
    for UID in range(start_point, finish_point + 1, step):
        result = get_json(str(UID))
        if result != -1:
            print UID, 'Done'
            output_file.write("%s\n" % json.dumps(result))
            valid_user = valid_user + 1
            users_with_tips = users_with_tips + users_w_tips
    output_file.close()


if __name__ == '__main__':
    count = 0
    while(count < 5):
        a=random.randint(min_id,max_id)
        b=random.randint(5000,10000)
        if a-b > 0:
            start_point = a-b
            finish_point = a
        elif a-b < 0:
            start_point = b-a
            finish_point = b
        else:
            continue
        step = 1
        run(start_point, finish_point , step)
        total_user = total_user + finish_point - start_point + 1
        count = count + 1

    print "valid_user: " , valid_user
    print "total_user: " , total_user
    print "users_with_tips: " , users_with_tips

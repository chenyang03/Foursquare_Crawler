# -*-coding: utf-8-*-
import json
import codecs
import foursq_profiles
import foursq_tips

sys_api_token = 0
sys_client_version = 0


def get_json(user_id):
    crawl_tips = {}
    crawl_tips['user info'] = foursq_profiles.fetch_user_profile(user_id)
    if crawl_tips['user info'] != -1:
        crawl_tips['tips'] = foursq_tips.fetch_usr_tips(user_id)
    else:
        return -1
    return crawl_tips


def run(start_point, finish_point, step):
    output_file = codecs.open("4sq_tips_chunk_%d_to_%d.txt" % (start_point, finish_point), "w", "utf-8-sig")
    for UID in range(start_point, finish_point + 1, step):
        result = get_json(str(UID))
        if result != -1:
            print UID, 'Done'
            output_file.write("%s\n" % json.dumps(result))
    output_file.close()


if __name__ == '__main__':
    start_point = 32
    finish_point = 32
    step = 1
    run(start_point, finish_point, step)

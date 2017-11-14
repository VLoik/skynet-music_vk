import vkapi
import time
import random
import lastfmapi
import config
from datetime import datetime

standart_tag = ["Rock", "Hip-Hop", "Jazz", "Blues", "Dance", "Pop"]


def get_post(mode):
    if mode == 1: # шаблонный тег, артист
        tag = random.choice(standart_tag)
        artist=lastfmapi.get_artist_by_tag(tag)
        text, cov_url, tracks = lastfmapi.get_tracks_by_artist(artist)
        post_tag = "#"+tag.lower()+"@skynetmusic\n"
    if mode == 2: # шаблонный тег, подборка
        tag = random.choice(standart_tag)
        cov_url, tracks = lastfmapi.get_track_by_tag(tag)
        text=""
        post_tag = "#" + tag.lower() + "@skynetmusic"
    if mode == 3: # русский артист
        tag = "Russian"
        artist = lastfmapi.get_artist_by_tag(tag)
        text, cov_url, tracks = lastfmapi.get_tracks_by_artist(artist)
        post_tag = "#" + tag.lower() + "@skynetmusic\n"
    if mode == 4: # подборка русских треков
        tag = "Russian"
        cov_url, tracks = lastfmapi.get_track_by_tag(tag)
        text=""
        post_tag = "#" + tag.lower() + "@skynetmusic"
    if mode==5:
        tag = random.choice(tags_list)
        artist = lastfmapi.get_artist_by_tag(tag)
        text, cov_url, tracks = lastfmapi.get_tracks_by_artist(artist)
        text="Рандомный тег поста: "+tag+text
        post_tag = "#random@skynetmusic\n"
    if mode==6:
        tag = random.choice(tags_list)
        cov_url, tracks = lastfmapi.get_track_by_tag(tag)
        text = "Рандомный тег поста: " + tag
        post_tag = "#random@skynetmusic\n"
    if (cov_url is None): return -1
    cover = vkapi.upload_image(cov_url, flag=1)
    attach = cover
    for track in tracks:
        audio = vkapi.find_audio(track)
        if (audio != -1):
            attach = attach + "," + "audio" + str(audio["owner_id"]) + "_" + str(audio["id"])
        time.sleep(1)
    if ("audio" not in attach): return -1
    vkapi.bot.wall.post(owner_id=-139136042, from_group=1, message=post_tag+"\n" + text, attachments=attach)
    return 1

def post():
    mode = random.uniform(0, 100)
    print(mode)
    if (mode < 20): get_post(1)
    if (mode > 20 and mode < 40): get_post(2)
    if (mode > 40 and mode < 60): get_post(3)
    if (mode > 57 and mode < 73): get_post(4)
    if (mode > 73 and mode < 85): get_post(5)
    if (mode > 85): get_post(6)


def main():
    global tags_list
    random.seed()
    tag_file = open('lastfm_tags.txt')
    tags_list = []
    for line in tag_file:
        tags_list.append(line.split('\t')[0])
    try:
        post()
        last_post_time=datetime.now()
    except Exception as error:
        print("Error from first post!")
        print(error)
    while(True):
        try:
            delta = datetime.now() - last_post_time
            if(delta.total_seconds() > config.time_to_post*3600):
                post()
                last_post_time = datetime.now()
        except:
            continue



if __name__ == '__main__':
    main()

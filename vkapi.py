import vk
import requests
from config import *
import re


def auth_vk(id, login, passwd, scope):
    session = vk.AuthSession(app_id=id, user_login=login, user_password=passwd, scope=scope)
    return vk.API(session, v='5.50')


def upload_image(url, flag=0):

    p = requests.get(url)
    out = open("cover.jpg", "wb")
    out.write(p.content)
    out.close()

    img = {'photo': ('img.jpg', open(r'cover.jpg', 'rb'))}

    if (flag == 0):
        response = bot.photos.getMessagesUploadServer()
    else:
        response = bot.photos.getWallUploadServer()
    upload_url = response['upload_url']

    response = requests.post(upload_url, files=img)
    result = response.json()

    photo1 = result['photo']
    hash1 = result['hash']
    server1 = result['server']

    if (photo1 != '[]'):
        if (flag == 0):
            response = bot.photos.saveMessagesPhoto(server=server1, photo=photo1, hash=hash1)
        else:
            response = bot.photos.saveWallPhoto(owner_id=-139136042, server=server1, photo=photo1, hash=hash1)
        attach = "photo" + str(response[0]['owner_id']) + "_" + str(response[0]['id'])
        return attach


def find_audio(track):
    s_track_list = bot.audio.search(q=track, auto_complete=1, count=100, sort=2)["items"]
    name = re.split(" - ", track)[0]
    title = re.split(" - ", track)[1]
    ban_word = ["remix", "minus", "ремикс", "cover", "ковер", "кавер", "минус", "bassboosted", "live", "mix"]

    for s_track in s_track_list:
        if((s_track["artist"] == name) and (s_track["title"] == title)):
            return({"id":s_track['id'], "owner_id":s_track['owner_id']})

    for s_track in s_track_list:
        if((name.lower() in s_track["artist"].lower()) and (s_track["title"].lower() == title.lower())):
            return({"id":s_track['id'], "owner_id":s_track['owner_id']})

    flag = 0
    for s_track in s_track_list:
        if((s_track["artist"] == name) and (len(s_track["title"].split(" ")) < 7)):
            for word in ban_word:
                if(word in s_track["title"].lower()): flag=1
            if (flag == 0):
                return({"id":s_track['id'], "owner_id":s_track['owner_id']})
            else: flag=0
    return -1

bot = auth_vk(app_id, v_login, v_password, 'wall,messages,photos,audio,offline')
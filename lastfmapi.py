import pylast
from config import *
import re
import random

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =API_SECRET, username = lfm_username, password_hash = pylast.md5(lfm_password))


def get_tracks_by_artist(artist_name):
    artist = network.get_artist(artist_name)
    cover = artist.get_cover_image()
    top = artist.get_top_tracks(limit=9)
    tracks=[]
    for track in top:
        title_track = artist.get_name() + " - " + track.item.get_title()
        tracks.append(title_track)
    biography=artist.get_bio_summary(language="ru")
    biography = re.sub("<a.*a>", "", biography) + "\n Читать далее:\n"+artist.get_url(domain_name=9)
    return biography, cover, tracks


def get_track_by_tag(tag_name):
    tag = network.get_tag(tag_name)
    list_tracks = tag.get_top_tracks(600)
    tracks = []
    for i in range(0,10):
        track = random.choice(list_tracks)
        title_track = track.item.get_artist().get_name() + " - " + track.item.get_name()
        tracks.append(title_track)
    artist = track.item.get_artist()
    cover = artist.get_cover_image()
    return cover, tracks

def get_artist_by_tag(tag_name):
    tag=network.get_tag(tag_name)
    list_artists = tag.get_top_artists(limit=100)
    artist = random.choice(list_artists)
    return artist.item.get_name()


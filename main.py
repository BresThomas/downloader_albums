from pytube import YouTube
from pytube import Playlist
import os
from mutagen.mp4 import MP4, MP4Cover
import requests
import shutil
#IMPORT THESE PACKAGES
import selenium
from selenium import webdriver
import time

from selenium.webdriver.common.by import By

driver = webdriver.Chrome("/Users/Thomas/PycharmProjects/pytube/chromedriver")


link = "https://www.youtube.com/playlist?list=OLAK5uy_nISeEvbAHuWotMBWEg2qnXEcpY5ER5ESA"



# Lien de l'album a telecharger
playlist = Playlist(link)


xpath_cookie = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div/div/button/span"
xpath_cover = "/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-playlist-sidebar-renderer/div/ytd-playlist-sidebar-primary-info-renderer/ytd-playlist-thumbnail/a/div[1]/ytd-playlist-custom-thumbnail-renderer/yt-img-shadow/img"
xpath_artist = "/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-playlist-video-list-renderer/div[3]/ytd-playlist-video-renderer[1]/div[2]/div[1]/div/ytd-video-meta-block/div[1]/div[1]/ytd-channel-name/div/div/yt-formatted-string/a"
xpath_title = "/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-playlist-sidebar-renderer/div/ytd-playlist-sidebar-primary-info-renderer/h1/yt-formatted-string/a"
driver.get(link)
time.sleep(2)
driver.find_element(by=By.XPATH, value=xpath_cookie).click()
album = driver.find_element(by=By.XPATH, value=xpath_title).text
artist = driver.find_element(by=By.XPATH, value=xpath_artist).text
cover = driver.find_element(by=By.XPATH, value=xpath_cover).get_attribute("src")

r = requests.get(cover, stream=True, headers={'User-agent': 'Mozilla/5.0'})
if r.status_code == 200:
    with open("cover.jpeg", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)




lieu = "/Users/Thomas/PycharmProjects/pytube/"
directory = artist + " - " + album
path = os.path.join(lieu, directory)
os.makedirs(path)



# Parmi les liens telecharger l'audio
for url in playlist:
    YouTube(url).streams.filter(only_audio=True).first().download(path)

files = os.listdir(path)
files2 = sorted([os.path.join(path, file) for file in os.listdir(path)], key=os.path.getctime)
files2.sort(key=os.path.getmtime, reverse=True)

n = 0
for name in reversed(files2):
    n = n + 1
    mp4_video_tags = MP4(name)
    tmp = name.split("/")
    name_song = tmp[-1].split(".")
    mp4_video_tags['\xa9nam'] = name_song[0]
    mp4_video_tags['\xa9alb'] = album
    mp4_video_tags['\xa9ART'] = artist
    mp4_video_tags['trkn'] = [(int(n), int(len(playlist)))]
    with open("/Users/Thomas/PycharmProjects/pytube/cover.jpeg", "rb") as f:
        mp4_video_tags["covr"] = [
            MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
        ]
    mp4_video_tags.save()
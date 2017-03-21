# -*- coding: utf-8 -*-
import os
import codecs
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_band_name(title):
    return title.split(' - ')[0]


def get_song_name(title):
    s = title.split(' - ')[1]
    return s[s.find('"') + len('"'):s.rfind('"')]


def is_tab_type_guitar(title):
    return "guitar" in title.rsplit('"', 1)[1].lower()


def save_tab(band_name, song_name, soup):
    if not os.path.exists(band_name):
        os.makedirs(band_name)

    os.chdir(os.getcwd() + "\\" + band_name)

    with open(song_name + ".txt", 'w') as f:
        f.write(str(soup.text))

    os.chdir("..")


def determine_song_tuning(soup):
    tuning_keywords = ["tune", "tuning", "standard", "dropped", "half step", "half-step"]

    txt = str(soup.text).lower()

    txt_list = list(txt.split("\n"))
    for i in range(len(txt_list)):
        if any(keyword in txt_list[i] for keyword in tuning_keywords):
            return txt_list[i]
    return "UNKNOWN TUNING"


def process_tab_link(metal_url):

    band_name = ""
    song_name = ""
    tuning = ""
    # We only process guitar tab text files (can't process Guitar Pro files):
    # If there is no plain text link, pass.
    tab_page_request = requests.get(metal_url)
    if tab_page_request.status_code == 200:

        # URL is valid, proceed to check if URL pointing to
        # the text file is also valid.
        tab_url = metal_url + "@d=1.html"
        tab_txt_request = requests.get(tab_url)
        if tab_txt_request.status_code == 200:

            metal_url_html = urlopen(metal_url)
            metal_url_soup = BeautifulSoup(metal_url_html, "lxml")

            tab_url_html = urlopen(tab_url)
            tab_url_soup = BeautifulSoup(tab_url_html, "lxml")

            title = metal_url_soup.find('h1').getText()

            band_name = get_band_name(title)
            song_name = get_song_name(title)

            if is_tab_type_guitar(title):
                tuning = determine_song_tuning(tab_url_soup)
            else:
                pass

    else:
        # Website is not valid, move onto the next one.
        pass

    return [band_name, song_name, tuning]


# Total number of tabs (as of 3/18/2017).
max_tab_num = 14008
#max_tab_num = 633

metal_tuning_file = "metal_tunings.txt"

for i in range(1, max_tab_num):

    print("Processing tab " + str(i) + " of " + str(max_tab_num))
    metal_tab_url = "http://metaltabs.com/tab/" + str(i) + "/index.html"
    [band_name, song_name, tuning] = process_tab_link(metal_tab_url)

    if song_name != "" and band_name != "" and tuning != "":
        output = "SONG ID: " + str(i) + " --- " + song_name + " by " + band_name + " ::: " + tuning
        print(output)
        with codecs.open(metal_tuning_file, 'a', "utf-8-sig") as f:
            f.write(output + "\n")

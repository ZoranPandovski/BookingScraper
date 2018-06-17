import sys
sys.path.insert(0, "./lib/python3.5/site-packages")


import os
os.system('pip install -r ./requirements.txt')

import requests
from bs4 import BeautifulSoup


def get_booking_page(offset):
      url = 'https://www.booking.com/searchresults.en-gb.html?aid=304142&label=gen173nr-1DCAEoggJCAlhYSDNYBGiTAYgBAZgBLsIBCndpbmRvd3MgMTDIAQzYAQPoAQGSAgF5qAID&' \
            'sid=716ea5d78c4043fd78b7a1410d639e3d&checkin_month=6&checkin_monthday=8&checkin_year=2018&checkout_month=6&checkout_monthday=11&checkout_year=2018' \
            '&class_interval=1&dest_id=125&dest_type=country&dtdisc=0&from_sf=1&genius_rate=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef' \
            '&no_rooms=1&postcard=0&raw_dest_type=country&room1=A%2CA&sb_price_type=total&src=searchresults&src_elem=sb&ss=Macedonia&ss_all=0&ssb=empty&sshis=0&ssne=Macedonia' \
            '&ssne_untouched=Macedonia&rows=15&offset=' + str(offset)
      r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/48.0'})
      html = r.content
      parsed_html = BeautifulSoup(html, "lxml")
      return parsed_html


def get_data():
    '''
    Get all accomodations in Macedonia and save them in file
    :return: hotels-in-macedonia.txt file
    '''
    offset = 15
    parsed_html = get_booking_page(offset)
    all_offset = parsed_html.find_all("li", {'class': 'sr_pagination_item'})[-1].get_text()

    # change hotels to set if you like to remove duplicate Hotels returned by Booking
    hotels = []
    number = 0
    for i in range(int(all_offset)):
        offset += 15
        number+=1
        parsed_html = get_booking_page(offset)
        hotel = parsed_html.find_all("div", {"class": "sr_item"})

        for ho in hotel:
            name = ho.find('a', {'class': 'jq_tooltip'})['title']
            hotels.append(str(number) + ' : ' + name)
            number += 1

    import json
    with open('hotels-in-macedonia.txt', 'w', encoding='utf-8') as outfile:
        json.dump(hotels, outfile, indent=2, ensure_ascii=False)

    print('All accommodations are saved.')
    print('You can find them in hotels-in-macedonia.txt file')

if __name__ == "__main__":
    get_data()


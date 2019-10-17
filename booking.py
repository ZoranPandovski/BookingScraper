#! /usr/bin/env python3.6
import argparse
import argcomplete
from argcomplete.completers import ChoicesCompleter
from argcomplete.completers import EnvironCompleter
import requests
from bthread import BookingThread
from bs4 import BeautifulSoup
from file_writer import FileWriter

hotels = []


def get_countries():
    with open("countries.txt", "r") as f:
         countries = f.read().splitlines()
    return countries


def get_booking_page(session, offset, rooms, country):
    '''
    Make request to booking page and parse html
    :param offset:
    :return: html page
    '''
    url = 'https://www.booking.com/searchresults.en-gb.html?' \
            'aid=304142&label' \
            '=gen173nr-1DCAEoggJCAlhYSDNYBGiTAYgBAZgBLsIBCnd' \
            'pbmRvd3MgMTDIAQzYAQPoAQGSAgF5qAID&' \
            'sid=716ea5d78c4043fd78b7a1410d639e3d&checkin_month=' \
            '6&checkin_monthday=8&checkin_year=2018&checkout_month=6&' \
            'checkout_monthday=11&checkout_year=2018' \
            '&class_interval=1&dest_id=125&dest_type=country&dtdisc=0&from_sf'\
            '=1&genius_rate=1&no_rooms={rooms}&group_adults=2&group_children=0&inac=0&' \
            'index_postcard=0&label_click=undef' \
            '&no_rooms=1&postcard=0&raw_dest_type=country&room1=' \
            'A%2CA&sb_price' \
            '_type=total&src=searchresults&src_elem=sb&ss={country}&ss_all=' \
            '0&ssb=empty&sshis=0&ssne={country}' \
            '&ssne_untouched={country}&rows=15&offset='.format(
                rooms=rooms,
                country=country.replace(' ', '+')
            ) + str(offset)
    r = requests.get(url, headers=
      {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)'
                     ' Gecko/20100101 Firefox/48.0'})
    html = r.content
    parsed_html = BeautifulSoup(html, 'lxml')
    return parsed_html


def process_hotels(session, offset, rooms, country):
    parsed_html = get_booking_page(session, offset, rooms, country)
    hotel = parsed_html.find_all('div', {'class': 'sr_item'})
    for ho in hotel:
        name = ho.find('a', {'class': 'jq_tooltip'})['title']
        hotels.append(str(len(hotels) + 1) + ' : ' + name)


def prep_data(rooms=1, country='Macedonia', out_format=None):
    '''
    Prepare data for saving
    :return: hotels: set()
    '''
    offset = 15
    
    session = requests.Session()

    parsed_html = get_booking_page(session, offset, rooms, country)
    all_offset = parsed_html.find_all('li', {'class':
                                      'sr_pagination_item'})[-1].get_text().splitlines()[-1]
    threads = []
    for i in range(int(all_offset)):
        offset += 15
        t = BookingThread(session, offset, rooms, country, process_hotels)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    hotels2 = hotels
    return hotels2


def get_data(rooms=1, country='Macedonia', out_format=None):
    '''
    Get all accomodations in Macedonia and save them in file
    :return: hotels-in-macedonia.{txt/csv/xlsx} file
    '''
    hotels_list = prep_data(rooms,country,out_format)
    save_data(hotels_list , out_format=out_format, country=country)


def save_data(data, out_format, country):
    '''
    Saves hotels list in file
    :param data: hotels list
    :param out_format: json, csv or excel
    :return:
    '''
    writer = FileWriter(data, out_format, country)
    file = writer.output_file()

    print('All accommodations are saved.')
    print('You can find them in', file, 'file')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    countries = get_countries()

    parser.add_argument("--rooms",
                        help='Add the number of rooms to the booking request.',
                        default=1,
                        type=int,
                        nargs='?')
    parser.add_argument("--country",
                        help='Add the country to the booking request.',
                        default='Macedonia',
                        nargs='?').completer = ChoicesCompleter(countries)
    parser.add_argument("--out_format",
                        help='Add the format for the output file. Add excel, json or csv.',
                        default='json',
                        choices=['json', 'excel', 'csv'],
                        nargs='?').completer = EnvironCompleter
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    get_data(args.rooms, args.country, args.out_format)

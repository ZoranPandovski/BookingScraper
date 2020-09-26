#! /usr/bin/env python3.6
import argparse
import argcomplete
from argcomplete.completers import ChoicesCompleter
from argcomplete.completers import EnvironCompleter
import requests
import datetime
from bthread import BookingThread
from bs4 import BeautifulSoup
from file_writer import FileWriter

hotels = []


def get_countries():
    with open("countries.txt", "r") as f:
        countries: list = f.read().splitlines()
    f.close()
    return countries


def valid_date(given_date):
    try:
        return datetime.datetime.strptime(given_date, "%Y-%m-%d")
    except ValueError:
        msg = "{0} is not a valid date.".format(given_date)
        raise argparse.ArgumentTypeError(msg)


def default_start_date():
    try:
        today: str = datetime.datetime.today()
        return today.strftime("%Y-%m-%d")
    except Exception as e:
        msg = "Error creating default date"
        raise argparse.ArgumentError(e, msg)


def default_end_date():
    try:
        today: str = datetime.datetime.today() + datetime.timedelta(days=1)
        return today.strftime("%Y-%m-%d")
    except Exception as e:
        msg = "Error creating default date"
        raise argparse.ArgumentError(e, msg)


def get_booking_page(session, offset, rooms, country, startdate, enddate):
    """
    Make request to booking page and parse html
    :param offset:
    :return: html page
    """
    checkin: list = str(startdate).split("-")
    checkout: list = str(enddate).split("-")
    url: str = (
        "https://www.booking.com/searchresults.en-gb.html?"
        "aid=304142&label"
        "=gen173nr-1DCAEoggJCAlhYSDNYBGiTAYgBAZgBLsIBCnd"
        "pbmRvd3MgMTDIAQzYAQPoAQGSAgF5qAID&"
        "sid=716ea5d78c4043fd78b7a1410d639e3d&checkin_month="
        "{checkin_m}&checkin_monthday={checkin_d}&checkin_year={checkin_y}&checkout_month={checkout_m}&"
        "checkout_monthday={checkout_d}&checkout_year={checkout_y}"
        "&class_interval=1&dest_id=125&dest_type=country&dtdisc=0&from_sf"
        "=1&genius_rate=1&no_rooms={rooms}&group_adults=2&group_children=0&inac=0&"
        "index_postcard=0&label_click=undef"
        "&no_rooms=1&postcard=0&raw_dest_type=country&room1="
        "A%2CA&sb_price"
        "_type=total&src=searchresults&src_elem=sb&ss={country}&ss_all="
        "0&ssb=empty&sshis=0&ssne={country}"
        "&ssne_untouched={country}&rows=15&offset=".format(
            rooms=rooms,
            country=country.replace(" ", "+"),
            checkin_m=checkin[1],
            checkin_d=checkin[2],
            checkin_y=checkin[0],
            checkout_m=checkout[1],
            checkout_d=checkout[2],
            checkout_y=checkout[0],
        )
        + str(offset)
    )
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)"
            " Gecko/20100101 Firefox/48.0"
        },
    )
    html = r.content
    parsed_html = BeautifulSoup(html, "lxml")
    return parsed_html


def process_hotels(session, offset, rooms, country, start, end):
    parsed_html = get_booking_page(session, offset, rooms, country, start, end)
    hotel = parsed_html.find_all("div", {"class": "sr_item_content"})
    for ho in hotel:
        name = ho.find("span", {"class": "sr-hotel__name"}).text
        hotels.append(str(len(hotels) + 1) + " : " + name)


def prep_data(
    rooms=1,
    country="Macedonia",
    out_format=None,
    start_date=default_start_date(),
    end_date=default_end_date(),
):
    """
    Prepare data for saving
    :return: hotels: set()
    """
    offset: int = 15

    session = requests.Session()

    parsed_html = get_booking_page(
        session, offset, rooms, country, start_date, end_date
    )
    all_offset = (
        parsed_html.find_all("li", {"class": "sr_pagination_item"})[-1]
        .get_text()
        .splitlines()[-1]
    )
    threads: list = []
    for i in range(int(all_offset)):
        offset += 15
        t = BookingThread(
            session, offset, rooms, country, process_hotels, start_date, end_date
        )
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    hotels2: list = hotels
    return hotels2


def get_data(
    rooms=1,
    country="Macedonia",
    out_format=None,
    start_date=default_start_date(),
    end_date=default_end_date(),
):
    """
    Get all accomodations in Macedonia and save them in file
    :return: hotels-in-macedonia.{txt/csv/xlsx} file
    """
    hotels_list: list = prep_data(rooms, country, out_format, start_date, end_date)
    save_data(hotels_list, out_format=out_format, country=country)


def save_data(data, out_format, country):
    """
    Saves hotels list in file
    :param data: hotels list
    :param out_format: json, csv or excel
    :return:
    """
    writer = FileWriter(data, out_format, country)
    file = writer.output_file()

    print("All accommodations are saved.")
    print("You can find them in", file, "file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    countries = get_countries()

    parser.add_argument(
        "-r",
        "--rooms",
        help="Add the number of rooms to the booking request.",
        default=1,
        type=int,
        nargs="?",
    )
    parser.add_argument(
        "-c",
        "--country",
        help="Add the country to the booking request.",
        default="Macedonia",
        nargs="?",
    ).completer = ChoicesCompleter(countries)
    parser.add_argument(
        "-o",
        "--out_format",
        help="Add the format for the output file. Add excel, json or csv.",
        default="json",
        choices=["json", "excel", "csv"],
        nargs="?",
    ).completer = EnvironCompleter
    parser.add_argument(
        "-s",
        "--startdate",
        help="The start date for the booking (format: YYYY-MM-DD)",
        default=default_start_date(),
        type=valid_date,
    )
    parser.add_argument(
        "-e",
        "--enddate",
        help="The end date for the booking (format: YYYY-MM-DD)",
        default=default_end_date(),
        type=valid_date,
    )
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    get_data(args.rooms, args.country, args.out_format, args.startdate, args.enddate)

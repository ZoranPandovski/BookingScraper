import unittest
import os
import requests
import requests_mock

from unittest.mock import patch

from bs4 import BeautifulSoup

from booking import get_countries
from booking import get_booking_page
from booking import process_hotels
from booking import prep_data
from booking import get_data

offset = 15
rooms = 2
country = 'Albania'

hotels_fixture = [
    "1 : Solun's Riverside Rooms, Skopje",
    '2 : Hotel Aleksandrija, Ohrid',
    '3 : Central Exclusive Apartment/Penthouse, Bitola',
    '4 : Vila Kumani, Ohrid',
    '5 : Best Western Hotel Turist, Skopje',
    '6 : Hotel Arka, Skopje',
    '7 : Opera House Hotel, Skopje',
    '8 : Hotel Panoramika Design & Spa, Skopje',
    '9 : Quiet, bright and cozy apartment near the center, Skopje',
    '10 : Hotel Vlaho, Skopje',
    '11 : Alexandar Square Apartments, Skopje',
    '12 : Luxury Skopje Apartments Premium, Skopje',
    '13 : Aen Hotel, Skopje',
    '14 : Hotel Dolce International, Skopje',
    '15 : Hotel Treff, Bitola'
]


def booking_response_fixture():
    with open("booking_response_fixture.txt", "r") as f:
        countries = f.read()
    return countries.encode('utf-8')


class BookingTests(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_booking_page(self, mock):
        ''' Verify get_booking_page '''
        mock.get(
            'https://www.booking.com/searchresults.en-gb.html',
            content=booking_response_fixture())

        session = requests.Session()
        result = get_booking_page(session, offset, rooms, country)

        self.assertIsInstance(result, BeautifulSoup)
        self.assertEqual(mock.call_count, 1)

    @patch('booking.myThread')
    def test_prep_data(self, thread_mock):
        ''' Verify prep_data '''
        with requests_mock.Mocker() as mock:
            mock.get(
                requests_mock.ANY,
                content=booking_response_fixture())

            result = prep_data(rooms, country)

            self.assertEqual(thread_mock.call_count, 67)
            self.assertIsInstance(result, list)

    def test_get_countries_list(self):
        countries = get_countries()

        self.assertEqual(len(countries), 264)

    def test_can_process_hotels(self):
        with requests_mock.Mocker() as mock:
            mock.get(
                requests_mock.ANY,
                content=booking_response_fixture())

            session = requests.Session()
            result = process_hotels(session, offset, rooms, country)

            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 15)

    @patch('booking.prep_data')
    def test_get_excel(self, prep_data_mock):
        ''' Verify excel output '''
        prep_data_mock.return_value = hotels_fixture
        try:
            get_data(rooms, country, out_format='excel')
            if not os.path.isfile('hotels-in-{}.xls'.format(country)):
                raise AssertionError()
        except IOError:
            print('Failure: File cannot be read.')

    @patch('booking.prep_data')
    def test_get_csv(self, prep_data_mock):
        ''' Verify csv output '''
        prep_data_mock.return_value = hotels_fixture
        try:
            get_data(rooms, country, out_format='csv')
            if not os.path.isfile('hotels-in-{}.csv'.format(country)):
                raise AssertionError()
        except IOError:
            print('Failure: File cannot be read.')

    @patch('booking.prep_data')
    def test_get_default_json(self, prep_data_mock):
        ''' Verify json output '''
        prep_data_mock.return_value = hotels_fixture
        try:
            get_data(rooms, country, out_format='json')
            if not os.path.isfile('hotels-in-{}.txt'.format(country)):
                raise AssertionError()
        except IOError:
            print('Failure: File cannot be read.')


if __name__ == '__main__':
    unittest.main()

import unittest
import booking as b
from os import path

offset = 15
rooms = 2
country = 'Macedonia'

class BookingTests(unittest.TestCase):

    def test_get_booking_page(self):
        ''' Verify get_booking_page
            :return: True
        '''
        try:
            assert b.get_booking_page(offset,rooms,country) is not None, 'FAIL'
        except TypeError:
            raise
        except NameError:
            raise
        except AttributeError:
            raise

    def test_save_data(self):
        ''' Verify save_data
        '''
        offset = 15
        html = b.get_booking_page(offset,rooms,country)
        all_offset = html.find_all('li', {'class': 'sr_pagination_item'})[-1].get_text()

        hotels = set()
        number = 0
        for i in range(int(all_offset)):
            offset += 15
            number+=1
            parsed_html = b.get_booking_page(offset, rooms, country)
            hotel = parsed_html.find_all('div', {'class': 'sr_item'})

            for ho in hotel:
                name = ho.find('a', {'class': 'jq_tooltip'})['title']
                hotels.add(str(number) + ' : ' + name)
                number += 1

        try:
            b.save_data(hotels, out_format='excel', country=country)
            if path.isfile('hotels-in-{}.xls'.format(country)):
                print('XLS - Pass')
        except IOError:
            print('File cannot be read.')

        try:
            b.save_data(hotels, out_format='csv', country=country)
            if path.isfile('hotels-in-{}.xls'.format(country)):
                print('CSV - Pass')
        except IOError:
            print('File cannot be read.')

        try:
            b.save_data(hotels, out_format='json', country=country)
            if path.isfile('hotels-in-{}.xls'.format(country)):
                print('JSON - Pass')
        except IOError:
            print('File cannot be read.')    
            
if __name__ == '__main__':
    unittest.main()

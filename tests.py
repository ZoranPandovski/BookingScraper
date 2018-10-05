import unittest
import booking as b
import os

offset = 15
rooms = 2
country = 'Macedonia'

class BookingTests(unittest.TestCase):

    def test_get_booking_page(self):
        ''' Verify get_booking_page '''
        i = b.get_booking_page(offset,rooms,country)
        assert i is not None, 'Fail'

    def test_get_excel(self):
        ''' Verify excel output '''
        try:
            b.get_data(rooms,country,out_format='excel')
            assert os.path.isfile('hotels-in-{}.xlsx'.format(country)) is True, 'Failure: File does not exist'
        except IOError:
            print('Failure: File cannot be read.')

    def test_get_csv(self):
        ''' Verify csv output '''
        try:
            b.get_data(rooms,country,out_format='csv')
            assert os.path.isfile('hotels-in-{}.csv'.format(country)) is True, 'Failure: File does not exist'
        except IOError:
            print('Failure: File cannot be read.')

    def test_get_default_json(self):
        ''' Verify json output '''
        try:
            b.get_data(rooms,country,out_format='json')
            assert os.path.isfile('hotels-in-{}.txt'.format(country)) is True, 'Failure: File does not exist'
        except IOError:
            print('Failure: File cannot be read.')    
            

if __name__ == '__main__':
    unittest.main()

import unittest
import booking as b
import os

offset = 15
rooms = 2
country = 'Albania'

class BookingTests(unittest.TestCase):

    @classmethod
    def test_get_booking_page(self):
        ''' Verify get_booking_page '''
        i = b.get_booking_page(offset,rooms,country)
        if not i:
            raise AssertionError()

    @classmethod
    def test_prep_data(self):
        ''' Verify prep_data '''
        i = b.prep_data(rooms,country)
        if not i:
            raise AssertionError()

    @classmethod
    def test_get_excel(self):
        ''' Verify excel output '''
        try:
            b.get_data(rooms,country,out_format='excel')
            if not os.path.isfile('hotels-in-{}.xls'.format(country)):
                raise AssertionError()
        except IOError:
            print('Failure: File cannot be read.')

    @classmethod
    def test_get_csv(self):
        ''' Verify csv output '''
        try:
            b.get_data(rooms,country,out_format='csv')
            if not os.path.isfile('hotels-in-{}.csv'.format(country)):
                raise AssertionError()
        except IOError:
            print('Failure: File cannot be read.')

    @classmethod
    def test_get_default_json(self):
        ''' Verify json output '''
        try:
            b.get_data(rooms,country,out_format='json')
            if not os.path.isfile('hotels-in-{}.txt'.format(country)):
                raise AssertionError()
        except IOError:
            print('Failure: File cannot be read.')

if __name__ == '__main__':
    unittest.main()

import unittest
import booking as b
import os
import requests
import csv

offset = 15
rooms = 1
country = "Macedonia"
start_date = b.default_start_date()
end_date = b.default_end_date()


class BookingTests(unittest.TestCase):
    @classmethod
    def test_get_booking_page(self):
        """ Verify get_booking_page """
        session = requests.Session()
        i = b.get_booking_page(session, offset, rooms, country, start_date, end_date)
        assert i

    @classmethod
    def test_prep_data(self):
        """ Verify prep_data """
        i = b.prep_data(rooms, country, start_date, end_date)
        assert i

    @classmethod
    def test_get_countries(self):
        """ Get Countries """
        c: list = b.get_countries()
        assert c != []

    @classmethod
    def test_default_start_end_date(self):
        """ Verify Start/End Date """
        try:
            s: str = b.default_start_date()
            e: str = b.default_end_date()
            # Assertions
            assert b.valid_date(s)
            assert b.valid_date(e)
        except Exception as err:
            raise ValueError(err)

    @classmethod
    def test_get_excel(self):
        """ Verify excel output """
        try:
            b.get_data(
                rooms,
                country,
                out_format="excel",
                start_date=b.default_start_date(),
                end_date=b.default_end_date(),
            )
            assert os.path.isfile("hotels-in-{}.xls".format(country))
        except IOError:
            print("Failure: File cannot be read.")

    @classmethod
    def test_get_csv(self):
        """ Verify csv output """
        try:
            b.get_data(
                rooms,
                country,
                out_format="csv",
                start_date=b.default_start_date(),
                end_date=b.default_end_date(),
            )
            assert os.path.isfile("hotels-in-{}.csv".format(country))
        except IOError:
            print("Failure: File cannot be read.")

    @classmethod
    def test_get_default_json(self):
        """ Verify json output """
        try:
            b.get_data(
                rooms,
                country,
                out_format="json",
                start_date=b.default_start_date(),
                end_date=b.default_end_date(),
            )
            assert os.path.isfile("hotels-in-{}.txt".format(country))
        except IOError:
            print("Failure: File cannot be read.")

    def test_csv_output(self):
        """ Verify that csv output file contains the expected elements"""
        try:
            mock_country = "MacedoniaMock"

            mock_data = [
                "1 : Skopje Panorama, Skopje",
                "2 : Chic & Cozy Central Loft, Skopje",
                "3 : Villa Dislievski, Ohrid",
                "4 : Velestovo House, Ohrid",
                "5 : Ibis Skopje City Center, Skopje",
                "6 : Villa Tabana, Ohrid",
                "7 : Villa Mishe, Ohrid",
                "8 : Navona 58, Skopje",
                "9 : Hotel Monako & Fish Restaurant Skopje, Skopje",
                "10 : Villa Toneli, Skopje",
            ]

            b.save_data(mock_data, out_format="csv", country=mock_country)
            assert os.path.isfile("hotels-in-{}.csv".format(mock_country))
            with open("hotels-in-{}.csv".format(mock_country)) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                line_count = 0
                for row in csv_reader:
                    name = mock_data[line_count].split(", ")[0].split(": ")[1]
                    city = mock_data[line_count].split(", ")[1]

                    # Assert that the first element in the output row is the item number
                    self.assertEqual(str(line_count + 1), row[0].strip())
                    # Assert that the second element in the output row is the hotel name
                    self.assertEqual(name, row[1].strip())
                    # Assert that the third element in the output row is the city
                    self.assertEqual(city, row[2].strip())

                    line_count += 1

                # Assert that the number of output items is equal to the number of input items.
                self.assertEqual(len(mock_data), line_count)

        except IOError:
            print("Failure: File cannot be read.")


if __name__ == "__main__":
    unittest.main()

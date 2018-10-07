[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a17cb028c594405e9235c724d6b45b50)](https://app.codacy.com/app/ZoranPandovski/BookingScraper?utm_source=github.com&utm_medium=referral&utm_content=ZoranPandovski/BookingScraper&utm_campaign=badger)
[![BCH compliance](https://bettercodehub.com/edge/badge/ZoranPandovski/BookingScraper?branch=master)](https://bettercodehub.com/)
[![Known Vulnerabilities](https://snyk.io/test/github/ZoranPandovski/BookingScraper/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/ZoranPandovski/BookingScraper?targetFile=requirements.txt)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)


# Booking site web scraper

Web scraper that downloads all of the accommodations in Macedonia and saves them in a file.

## Installation
Create virtual environment and run:

`pip install -r requirements.txt`

After that just run booking script:

`python booking.py`

## Autocompletion
If you want to use the feature of the autocompletion run:

`activate-global-python-argcomplete`

After that open new terminal in order to update and load new settings.

## TBD
* Add option for choosing which country should be scrapped.
* Add option for choosing a time frame.
* Add option for choosing the number of rooms.
* Add option for choosing file format.
* Setup travis ci
* Add tests

## Disclaimer
Data fetched from booking is only for personal use, you are not allowed to copy and paste content from Booking.com on to your own or third party pages (including social media pages such as Facebook, Twitter, Instagram etc.).

This applies to all types of content that can be found on Booking.com pages, including but not limited to hotel descriptions, reviews, hotel and room photos, hotel facility information, and prices. Moreover, this restriction also applies to content from Booking.com partner hotel websites and Booking Holdings Group company brands: such as Agoda, Priceline, Kayak, OpenTable, Rentalcars.

Clause 4.1.5 from Booking.com Affiliate Agreement: The Affiliate shall not programmatically evaluate and extract information (including guest reviews) from any part of the Booking.com Website (e.g. screen scrape).

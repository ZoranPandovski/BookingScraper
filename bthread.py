import threading


class BookingThread(threading.Thread):
    def __init__(
        self, session, offset, rooms, country, process_hotels, start_date, end_date
    ):
        threading.Thread.__init__(self)
        self.session = session
        self.offset = offset
        self.rooms = rooms
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.process_hotels = process_hotels

    def run(self):
        self.process_hotels(
            self.session,
            self.offset,
            self.rooms,
            self.country,
            self.start_date,
            self.end_date,
        )

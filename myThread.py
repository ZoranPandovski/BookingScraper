import threading


class myThread (threading.Thread):
    def __init__(self, session, offset, rooms, country, process_hotels):
        super().__init__()
        self.session = session
        self.offset = offset
        self.rooms = rooms
        self.country = country
        self.process_hotels = process_hotels

    def run(self):
        self.process_hotels(self.session,
                            self.offset,
                            self.rooms,
                            self.country)

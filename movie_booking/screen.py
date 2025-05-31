class Screen:
    def __init__(self, screen_id, screen_number, total_seats, cinema=None):
        self.screen_id = screen_id
        self.screen_number = screen_number
        self.total_seats = total_seats
        self.cinema = cinema  # Cinema object
        self.shows = []  # list of Show objects
        self.seats = []  # list of Seat objects (will be populated later)

    def add_show(self, show):
        if show not in self.shows:
            self.shows.append(show)
            show.screen = self # Set the screen for the show

    def remove_show(self, show):
        if show in self.shows:
            self.shows.remove(show)
            show.screen = None # Unset the screen for the show

    def get_shows(self):
        return self.shows

    def get_seats(self):
        return self.seats

    def get_details(self):
        return {
            "screen_id": self.screen_id,
            "screen_number": self.screen_number,
            "total_seats": self.total_seats,
            "cinema_id": self.cinema.cinema_id if self.cinema else None,
            "shows_count": len(self.shows),
            "seats_count": len(self.seats)
        }
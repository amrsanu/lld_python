from datetime import datetime

class Show:
    def __init__(self, show_id, movie, screen, start_time, end_time, price):
        self.show_id = show_id
        self.movie = movie  # Movie object
        self.screen = screen  # Screen object
        self.start_time = start_time # datetime object
        self.end_time = end_time   # datetime object
        self.price = price
        self.available_seats = [] # list of Seat objects (initially all seats from screen)
        self._initialize_seats()

    def _initialize_seats(self):
        if self.screen and self.screen.seats:
            # Initially, all seats in the screen are available for the show
            self.available_seats = list(self.screen.seats)

    def get_available_seats(self):
        return [seat for seat in self.available_seats if seat.is_available()]

    def book_seats(self, seats_to_book):
        booked_successfully = []
        failed_to_book = []
        for seat in seats_to_book:
            if seat in self.available_seats and seat.book_seat():
                booked_successfully.append(seat)
                # Remove from available_seats list for this show instance
                # Note: The Seat object itself is marked as booked, affecting all shows on that screen at that time.
                # A more robust system might track seat availability per show instance.
                # For this simple in-memory model, we'll rely on the Seat object's is_booked status.
            else:
                failed_to_book.append(seat)
        return booked_successfully, failed_to_book

    # Cancellation logic would typically involve finding the booking and unbooking the seats
    # This method signature is simplified for now.
    def cancel_booking(self, booking_id):
        # This would require access to Booking objects, which we'll handle in BookingSystem
        pass

    def get_details(self):
        return {
            "show_id": self.show_id,
            "movie_id": self.movie.movie_id if self.movie else None,
            "screen_id": self.screen.screen_id if self.screen else None,
            "start_time": self.start_time.isoformat() if isinstance(self.start_time, datetime) else str(self.start_time),
            "end_time": self.end_time.isoformat() if isinstance(self.end_time, datetime) else str(self.end_time),
            "price": self.price,
            "available_seats_count": len(self.get_available_seats())
        }
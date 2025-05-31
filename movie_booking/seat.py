class Seat:
    def __init__(self, seat_id, seat_number, row_number, screen=None):
        self.seat_id = seat_id
        self.seat_number = seat_number
        self.row_number = row_number
        self.screen = screen  # Screen object
        self.is_booked = False

    def book_seat(self):
        if not self.is_booked:
            self.is_booked = True
            return True
        return False # Seat is already booked

    def unbook_seat(self):
        if self.is_booked:
            self.is_booked = False
            return True
        return False # Seat is not booked

    def is_available(self):
        return not self.is_booked

    def get_details(self):
        return {
            "seat_id": self.seat_id,
            "seat_number": self.seat_number,
            "row_number": self.row_number,
            "screen_id": self.screen.screen_id if self.screen else None,
            "is_booked": self.is_booked
        }
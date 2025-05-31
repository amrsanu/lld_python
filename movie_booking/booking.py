from datetime import datetime

class Booking:
    def __init__(self, booking_id, user, show, booked_seats, total_amount):
        self.booking_id = booking_id
        self.user = user  # User object
        self.show = show  # Show object
        self.booked_seats = booked_seats  # list of Seat objects
        self.booking_time = datetime.now()
        self.total_amount = total_amount
        self.status = 'Pending' # e.g., 'Pending', 'Confirmed', 'Cancelled'

    def confirm_booking(self):
        if self.status == 'Pending':
            self.status = 'Confirmed'
            # In a real system, this would involve payment processing
            return True
        return False # Cannot confirm a non-pending booking

    def cancel_booking(self):
        if self.status == 'Pending' or self.status == 'Confirmed':
            self.status = 'Cancelled'
            # Unbook seats associated with this booking
            for seat in self.booked_seats:
                seat.unbook_seat()
            return True
        return False # Cannot cancel a booking that is already cancelled

    def get_details(self):
        return {
            "booking_id": self.booking_id,
            "user_id": self.user.user_id if self.user else None,
            "show_id": self.show.show_id if self.show else None,
            "booked_seat_ids": [seat.seat_id for seat in self.booked_seats],
            "booking_time": self.booking_time.isoformat(),
            "total_amount": self.total_amount,
            "status": self.status
        }
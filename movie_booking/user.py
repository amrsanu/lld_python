class User:
    def __init__(self, user_id, name, email, phone_number):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.bookings = []  # list of Booking objects

    def view_bookings(self):
        return self.bookings

    def add_booking(self, booking):
        if booking not in self.bookings:
            self.bookings.append(booking)

    def get_details(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "bookings_count": len(self.bookings)
        }
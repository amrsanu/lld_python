from movie import Movie
from cinema import Cinema
from screen import Screen
from seat import Seat
from show import Show
from booking import Booking
from user import User
from payment_gateway import PaymentGateway
from datetime import datetime
import uuid  # To generate unique IDs


class BookingSystem:
    def __init__(self):
        self.movies = {}  # movie_id: Movie object
        self.cinemas = {}  # cinema_id: Cinema object
        self.users = {}  # user_id: User object
        self.shows = {}  # show_id: Show object
        self.bookings = {}  # booking_id: Booking object
        self.payment_gateway = PaymentGateway()

    def add_movie(self, title, duration, genre, language, release_date, description):
        movie_id = str(uuid.uuid4())
        movie = Movie(
            movie_id, title, duration, genre, language, release_date, description
        )
        self.movies[movie_id] = movie
        print(f"Added movie: {title} with ID: {movie_id}")
        return movie

    def add_cinema(self, name, address):
        cinema_id = str(uuid.uuid4())
        cinema = Cinema(cinema_id, name, address)
        self.cinemas[cinema_id] = cinema
        print(f"Added cinema: {name} with ID: {cinema_id}")
        return cinema

    def add_screen_to_cinema(self, cinema_id, screen_number, total_seats):
        cinema = self.cinemas.get(cinema_id)
        if not cinema:
            print(f"Cinema with ID {cinema_id} not found.")
            return None

        screen_id = str(uuid.uuid4())
        screen = Screen(screen_id, screen_number, total_seats, cinema)
        cinema.add_screen(screen)

        # Initialize seats for the screen
        for i in range(1, total_seats + 1):
            seat_id = str(uuid.uuid4())
            # Simple seat numbering: row 1, seat 1 to total_seats
            seat = Seat(seat_id, i, 1, screen)
            screen.seats.append(seat)

        print(
            f"Added screen {screen_number} to cinema {cinema.name} with ID: {screen_id}"
        )
        return screen

    def add_user(self, name, email, phone_number):
        user_id = str(uuid.uuid4())
        user = User(user_id, name, email, phone_number)
        self.users[user_id] = user
        print(f"Added user: {name} with ID: {user_id}")
        return user

    def add_show(self, movie_id, screen_id, start_time_str, end_time_str, price):
        movie = self.movies.get(movie_id)
        screen = None
        # Find the screen across all cinemas
        for cinema in self.cinemas.values():
            for s in cinema.get_screens():
                if s.screen_id == screen_id:
                    screen = s
                    break
            if screen:
                break

        if not movie:
            print(f"Movie with ID {movie_id} not found.")
            return None
        if not screen:
            print(f"Screen with ID {screen_id} not found.")
            return None

        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            print("Invalid time format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")
            return None

        show_id = str(uuid.uuid4())
        show = Show(show_id, movie, screen, start_time, end_time, price)
        self.shows[show_id] = show
        screen.add_show(show)  # Add show to the screen's list of shows
        print(
            f"Added show for movie '{movie.title}' on screen {screen.screen_number} at {start_time_str} with ID: {show_id}"
        )
        return show

    def search_movies(self, title=None, genre=None, language=None):
        results = []
        for movie in self.movies.values():
            match = True
            if title and title.lower() not in movie.title.lower():
                match = False
            if genre and genre.lower() not in movie.genre.lower():
                match = False
            if language and language.lower() != movie.language.lower():
                match = False
            if match:
                results.append(movie)
        return results

    def get_shows_by_movie(self, movie_id):
        movie = self.movies.get(movie_id)
        if not movie:
            print(f"Movie with ID {movie_id} not found.")
            return []
        shows_for_movie = []
        for show in self.shows.values():
            if show.movie.movie_id == movie_id:
                shows_for_movie.append(show)
        return shows_for_movie

    def get_shows_by_cinema(self, cinema_id):
        cinema = self.cinemas.get(cinema_id)
        if not cinema:
            print(f"Cinema with ID {cinema_id} not found.")
            return []
        return cinema.get_shows()

    def find_available_seats(self, show_id):
        show = self.shows.get(show_id)
        if not show:
            print(f"Show with ID {show_id} not found.")
            return []
        return show.get_available_seats()

    def make_booking(self, user_id, show_id, seat_ids):
        user = self.users.get(user_id)
        show = self.shows.get(show_id)

        if not user:
            print(f"User with ID {user_id} not found.")
            return None
        if not show:
            print(f"Show with ID {show_id} not found.")
            return None

        seats_to_book = []
        available_seats = show.get_available_seats()
        for seat_id in seat_ids:
            # Find the seat object by ID within the show's screen's seats
            found_seat = None
            if show.screen and show.screen.seats:
                for seat in show.screen.seats:
                    if seat.seat_id == seat_id:
                        found_seat = seat
                        break

            if found_seat and found_seat in available_seats:
                seats_to_book.append(found_seat)
            else:
                print(
                    f"Seat with ID {seat_id} is not available or does not exist for this show."
                )
                return (
                    None  # Fail the entire booking if any seat is invalid/unavailable
                )

        if not seats_to_book:
            print("No valid seats provided for booking.")
            return None

        # Calculate total amount
        total_amount = show.price * len(seats_to_book)

        # Process payment (using the placeholder gateway)
        payment_successful = self.payment_gateway.process_payment(
            total_amount, {"user_id": user_id, "show_id": show_id, "seat_ids": seat_ids}
        )

        if not payment_successful:
            print("Payment failed. Booking not created.")
            return None

        # Attempt to book the seats in the show
        booked_successfully, failed_to_book = show.book_seats(seats_to_book)

        if failed_to_book:
            print(
                f"Failed to book some seats: {[seat.seat_id for seat in failed_to_book]}. Rolling back booking."
            )
            # Unbook any seats that were successfully booked before failure
            for seat in booked_successfully:
                seat.unbook_seat()
            return None

        # Create the booking object
        booking_id = str(uuid.uuid4())
        booking = Booking(booking_id, user, show, booked_successfully, total_amount)
        booking.confirm_booking()  # Confirm the booking after successful payment and seat booking

        self.bookings[booking_id] = booking
        user.add_booking(booking)  # Add booking to the user's list of bookings

        print(f"Booking successful! Booking ID: {booking_id}")
        return booking

    def cancel_booking(self, booking_id):
        booking = self.bookings.get(booking_id)
        if not booking:
            print(f"Booking with ID {booking_id} not found.")
            return False

        if booking.cancel_booking():
            print(f"Booking {booking_id} cancelled successfully.")
            return True
        else:
            print(f"Could not cancel booking {booking_id}.")
            return False

    def get_booking_details(self, booking_id):
        booking = self.bookings.get(booking_id)
        if not booking:
            print(f"Booking with ID {booking_id} not found.")
            return None
        return booking.get_details()

    def get_user_bookings(self, user_id):
        user = self.users.get(user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return []
        return [booking.get_details() for booking in user.view_bookings()]

    def get_movie_details(self, movie_id):
        movie = self.movies.get(movie_id)
        if not movie:
            print(f"Movie with ID {movie_id} not found.")
            return None
        return movie.get_details()

    def get_cinema_details(self, cinema_id):
        cinema = self.cinemas.get(cinema_id)
        if not cinema:
            print(f"Cinema with ID {cinema_id} not found.")
            return None
        return cinema.get_details()

    def get_screen_details(self, screen_id):
        # Find the screen across all cinemas
        for cinema in self.cinemas.values():
            for screen in cinema.get_screens():
                if screen.screen_id == screen_id:
                    return screen.get_details()
        print(f"Screen with ID {screen_id} not found.")
        return None

    def get_show_details(self, show_id):
        show = self.shows.get(show_id)
        if not show:
            print(f"Show with ID {show_id} not found.")
            return None
        return show.get_details()

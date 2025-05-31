# Movie Booking System

## Core Classes

### Movie

- Attributes: movie_id, title, duration, genre, language, release_date, description
- Methods: get_details(), search_by_title(title), search_by_genre(genre)

### Cinema

- Attributes: cinema_id, name, address, screens (list of Screen objects)
- Methods: add_screen(screen), remove_screen(screen), get_screens(), get_shows()

### Screen

- Attributes: screen_id, screen_number, total_seats, cinema (Cinema object), shows (list of Show objects), seats (list of Seat objects)
- Methods: add_show(show), remove_show(show), get_shows(), get_seats()

### Seat

- Attributes: seat_id, seat_number, row_number, screen (Screen object), is_booked (boolean)
- Methods: book_seat(), unbook_seat(), is_available()

### Show

- Attributes: show_id, movie (Movie object), screen (Screen object), start_time, end_time, price, available_seats (list of Seat objects)
- Methods: get_available_seats(), book_seats(seats), cancel_booking(booking_id)

### Booking

- Attributes: booking_id, user (User object), show (Show object), booked_seats (list of Seat objects), booking_time, total_amount, status (e.g., 'Confirmed', 'Cancelled')
- Methods: confirm_booking(), cancel_booking(), get_details()

### User

- Attributes: user_id, name, email, phone_number, bookings (list of Booking objects)
- Methods: view_bookings(), create_booking(show, seats)

### PaymentGateway (Abstract or Interface)

- Methods: process_payment(amount, payment_details)

### BookingSystem (Central orchestrator)

- Attributes: movies (list of Movie objects), cinemas (list of Cinema objects), users (list of User objects)
- Methods: add_movie(movie), add_cinema(cinema), add_user(user), search_movies(criteria), get_shows_by_movie(movie_id), get_shows_by_cinema(cinema_id), find_available_seats(show_id), make_booking(user_id, show_id, seat_ids), cancel_booking(booking_id)

## Relationships

- A Cinema has multiple Screens.
- A Screen belongs to one Cinema.
- A Screen has multiple Seats.
- A Seat belongs to one Screen.
- A Screen hosts multiple Shows.
- A Show is on one Screen.
- A Show features one Movie.
- A Movie can be featured in multiple Shows.
- A User can have multiple Bookings.
- A Booking belongs to one User.
- A Booking is for one Show.
- A Booking includes multiple Seats.
The BookingSystem manages instances of Movie, Cinema, and User and orchestrates interactions between other objects.
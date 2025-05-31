from booking_system import BookingSystem
from datetime import datetime, timedelta


def main():
    system = BookingSystem()

    # Add some movies
    movie1 = system.add_movie(
        "The Matrix",
        136,
        "Sci-Fi",
        "English",
        "1999-03-31",
        "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
    )
    movie2 = system.add_movie(
        "Inception",
        148,
        "Sci-Fi",
        "English",
        "2010-07-16",
        "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
    )

    # Add a cinema and screens
    cinema1 = system.add_cinema("Cineplex", "123 Movie Lane")
    screen1 = system.add_screen_to_cinema(
        cinema1.cinema_id, 1, 100
    )  # Screen 1 with 100 seats
    screen2 = system.add_screen_to_cinema(
        cinema1.cinema_id, 2, 150
    )  # Screen 2 with 150 seats

    # Add a user
    user1 = system.add_user("Alice", "alice@example.com", "123-456-7890")

    # Add shows
    now = datetime.now()
    show1_time = now + timedelta(hours=2)
    show2_time = now + timedelta(hours=5)

    show1 = system.add_show(
        movie1.movie_id,
        screen1.screen_id,
        show1_time.isoformat(),
        (show1_time + timedelta(minutes=movie1.duration)).isoformat(),
        10.00,
    )
    show2 = system.add_show(
        movie2.movie_id,
        screen2.screen_id,
        show2_time.isoformat(),
        (show2_time + timedelta(minutes=movie2.duration)).isoformat(),
        12.00,
    )

    # Search for movies
    print("\nSearching for 'Matrix':")
    matrix_movies = system.search_movies(title="Matrix")
    for movie in matrix_movies:
        print(f"- {movie.get_details()['title']}")

    # Find available seats for a show
    print(f"\nAvailable seats for Show {show1.show_id}:")
    available_seats_show1 = system.find_available_seats(show1.show_id)
    print(f"Total available: {len(available_seats_show1)}")
    # print([seat.get_details()['seat_number'] for seat in available_seats_show1]) # Uncomment to see seat numbers

    # Make a booking
    if len(available_seats_show1) >= 2:
        seats_to_book = [
            available_seats_show1[0].seat_id,
            available_seats_show1[1].seat_id,
        ]
        print(
            f"\nAttempting to book seats {seats_to_book} for user {user1.user_id} on show {show1.show_id}"
        )
        booking1 = system.make_booking(user1.user_id, show1.show_id, seats_to_book)

        if booking1:
            print("\nBooking details:")
            print(booking1.get_details())

            # Verify seats are booked
            print(f"\nAvailable seats for Show {show1.show_id} after booking:")
            available_seats_after_booking = system.find_available_seats(show1.show_id)
            print(f"Total available: {len(available_seats_after_booking)}")

            # View user's bookings
            print(f"\nBookings for user {user1.name}:")
            user_bookings = system.get_user_bookings(user1.user_id)
            for booking_details in user_bookings:
                print(
                    f"- Booking ID: {booking_details['booking_id']}, Status: {booking_details['status']}"
                )

            # Cancel booking
            print(f"\nAttempting to cancel booking {booking1.booking_id}")
            system.cancel_booking(booking1.booking_id)

            # Verify booking status and seat availability after cancellation
            print(f"\nBooking details after cancellation:")
            print(system.get_booking_details(booking1.booking_id))

            print(f"\nAvailable seats for Show {show1.show_id} after cancellation:")
            available_seats_after_cancellation = system.find_available_seats(
                show1.show_id
            )
            print(f"Total available: {len(available_seats_after_cancellation)}")


if __name__ == "__main__":
    main()

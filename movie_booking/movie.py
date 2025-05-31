class Movie:
    def __init__(self, movie_id, title, duration, genre, language, release_date, description):
        self.movie_id = movie_id
        self.title = title
        self.duration = duration  # in minutes
        self.genre = genre
        self.language = language
        self.release_date = release_date
        self.description = description

    def get_details(self):
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "duration": self.duration,
            "genre": self.genre,
            "language": self.language,
            "release_date": self.release_date,
            "description": self.description
        }

    # We can add search methods later if needed, but for in-memory storage,
    # searching will likely be handled by the BookingSystem class.
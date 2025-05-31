class Cinema:
    def __init__(self, cinema_id, name, address):
        self.cinema_id = cinema_id
        self.name = name
        self.address = address
        self.screens = []  # list of Screen objects

    def add_screen(self, screen):
        if screen not in self.screens:
            self.screens.append(screen)
            screen.cinema = self # Set the cinema for the screen

    def remove_screen(self, screen):
        if screen in self.screens:
            self.screens.remove(screen)
            screen.cinema = None # Unset the cinema for the screen

    def get_screens(self):
        return self.screens

    def get_shows(self):
        all_shows = []
        for screen in self.screens:
            all_shows.extend(screen.get_shows())
        return all_shows

    def get_details(self):
        return {
            "cinema_id": self.cinema_id,
            "name": self.name,
            "address": self.address,
            "screens_count": len(self.screens)
        }
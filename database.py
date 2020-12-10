from models import Club


class Database:
    def __init__(self):
        self.clubs = {}
        self.club_key = 0
        self.club_name = ""

    def add_club(self, club):
        self.club_key += 1
        self.clubs[self.club_key] = club
        return self.club_key

    def delete_club(self, club_key):
        if club_key in self.clubs:
            del self.clubs[club_key]

    def get_club(self, name):
        club = self.clubs.get(name)
        if club is None:
            return None
        club_ = Club(name=club.name, description=club.description)
        return club_

    def get_clubs(self):
        clubs = []
        for club_key, club in self.clubs.items():
            club_ = Club(club.name, description=club.description)
            clubs.append((club_key, club_))
        return clubs
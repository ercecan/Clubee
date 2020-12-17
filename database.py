from models import Club


class Database:
    def __init__(self):
        self.clubs = {}
        self.club_key = 0

    def add_club(self, club):
        self.club_key += 1
        self.clubs[self.club_key] = club
        return self.club_key

    def delete_club(self, club_key):
        if club_key in self.clubs:
            del self.clubs[club_key]

    def get_club(self, club_key):
        club = self.clubs.get(club_key)
        if club is None:
            return None
        club_ = Club(name=club.name,
                     description=club.description,
                     history=club.history,
                     announcements=club.announcements,
                     events=club.events,
                     vision=club.vision,
                     mission=club.mission,
                     student_count=club.student_count,
                     image_url=club.image_url)
        return club_

    def get_clubs(self):
        clubs = []
        for club_key, club in self.clubs.items():
            club_ = Club(name=club.name,
                         description=club.description,
                         history=club.history,
                         announcements=club.announcements,
                         events=club.events,
                         vision=club.vision,
                         mission=club.mission,
                         student_count=club.student_count,
                         image_url=club.image_url)
            clubs.append((club_key, club_))
        return clubs
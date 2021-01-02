from models import Club, Announcement, Event
import psycopg2 as dbapi2
from config import Config


class Database:
    def __init__(self):
        self.conn = dbapi2.connect(Config.db_url)
        self.clubs = {}
        self.announcements = {}
        self.events = {}
        self.ann_key = 0
        self.club_key = 0
        self.event_key = 0

    def add_club(self, club):
        self.club_key += 1
        self.clubs[self.club_key] = club
        return self.club_key

    def add_announcement(self, announcement):
        self.ann_key += 1
        self.announcements[self.ann_key] = announcement
        return self.ann_key

    def add_event(self, event):
        self.event_key += 1
        self.events[self.event_key] = event
        return self.event_key

    def delete_club(self, club_key):
        if club_key in self.clubs:
            del self.clubs[club_key]

    def delete_announcement(self, ann_key):
        if ann_key in self.announcements:
            del self.announcements[ann_key]

    def delete_event(self, event_key):
        if event_key in self.events:
            del self.events[event_key]

    def get_club(self, club_key):

        query_select_one = "SELECT * FROM clubs WHERE id = " + str(
            club_key) + ";"
        club_ = []
        with self.conn.cursor() as curr:
            curr.execute(query_select_one)
            club_ = curr.fetchone()
        """
        #old style   
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
        """
        return club_

    def get_announcement(self, ann_key):
        announcement = self.announcements.get(ann_key)
        if announcement is None:
            return None
        announcement_ = Announcement(header=announcement.header,
                                     content=announcement.content,
                                     image_url=announcement.image_url)
        return announcement_

    def get_event(self, ann_key):
        event = self.events.get(ann_key)
        if event is None:
            return None
        event_ = Event(header=event.header,
                       content=event.content,
                       image_url=event.image_url)
        return event_

    def get_clubs(self):
        query_select = "SELECT * FROM clubs"
        clubs = []
        with self.conn.cursor() as curr:
            curr.execute(query_select)
            clubs = curr.fetchall()
        """
        for club in self.clubs.items():
            club_ = Club(name=clubs[1],
                         description=clubs[2],
                         history=clubs[3],
                         announcements=clubs[4],
                         events=clubs[5],
                         vision=clubs[6],
                         mission=clubs[7],
                         student_count=clubs[8],
                         image_url=clubs[9])
            clubs.append((club_key, club_))
        """
        return clubs

    def get_announcements(self, ann_key):
        announcements = []
        for ann_key, announcement in self.announcements.items():
            announcement_ = Announcement(header=announcement.header,
                                         content=announcement.content,
                                         image_url=announcement.image_url)
            announcements.append((ann_key, announcement_))
        return announcements

    def get_events(self, ann_key):
        events = []
        for event_key, event in self.events.items():
            event_ = Event(header=event.header,
                           content=event.content,
                           image_url=event.image_url)
            events.append((event_key, event_))
        return events

    def get_member_clubs(self, user_id):
        member_clubs = []
        get_member_clubs_statement = """ SELECT clubs.id, clubs.name, clubs.description, 
                                            clubs.history, clubs.student_count, clubs.source, clubs.mission, clubs.vision, clubs.image_url
                                            FROM clubs, members, users 
                                            WHERE ( (users.id = """ + str(
            user_id) + """)
                                            AND (members.club_id = clubs.id) 
                                            AND (members.user_id = users.id) ) """
        data = {'x': user_id}
        with self.conn.cursor() as curr:
            curr.execute(get_member_clubs_statement)
            member_clubs = curr.fetchall()
        return member_clubs


"""
id SERIAL PRIMARY KEY,
name VARCHAR(100) UNIQUE NOT NULL, 
description TEXT,
history TEXT,
student_count INTEGER DEFAULT 0,
source VARCHAR, 
mission TEXT,
vision TEXT,
image_url TEXT
"""
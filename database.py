from models import Club, Announcement, Event
import psycopg2 as dbapi2
from config import Config


class Database:
    def __init__(self):
        self.conn = dbapi2.connect(
            Config.db_url)  #FOR HEROKU add to paramters: sslmode='require'
        self.clubs = {}
        self.announcements = {}
        self.events = {}
        self.ann_key = 0
        self.club_key = 0
        self.event_key = 0

    """
    def add_club(self, club):
        self.club_key += 1
        self.clubs[self.club_key] = club
        return self.club_key
    """

    def add_announcement(self, announcement, id):
        try:
            with self.conn.cursor() as cursor:
                add_ann_statement = """INSERT INTO announcements (club_id,header,content,blob_image) 
                VALUES ((select club_id from club_managers where admin_id = %(id)s),%(ah)s,%(ac)s, %(ai)s); """
                data = {
                    'id': id,
                    'ah': announcement.header,
                    'ac': announcement.content,
                    'ai': announcement.image
                }
                cursor.execute(add_ann_statement, data)
                self.conn.commit()
        except (Exception, dbapi2.Error) as error:
            print("Error while adding announcement: {}".format(error))

    #id adminin idsi, ann_id announcement idsi, announcement da announcement objesi
    def update_announcement(self, ann_id, announcement, img_update):
        update_statement = ""
        try:
            with self.conn.cursor() as cursor:
                if img_update:
                    update_statement = """UPDATE announcements SET 
                    header = %(ah)s, content = %(ac)s, blob_image = %(ai)s 
                    WHERE id = """ + str(ann_id)
                else:
                    update_statement = """UPDATE announcements SET 
                    header = %(ah)s, content = %(ac)s
                    WHERE id = """ + str(ann_id)
                data = {
                    'ah': announcement.header,
                    'ac': announcement.content,
                    'ai': announcement.image
                }
                cursor.execute(update_statement, data)
                self.conn.commit()
                print(id)
        except (Exception, dbapi2.Error) as error:
            print("Error while updating announcement: {}".format(error))

    def add_event(self, event, id):  ####FIX IAMGE_URL TYPO
        try:
            with self.conn.cursor() as cursor:
                add_event_statement = """INSERT INTO events (club_id, header, content,date_, blob_image) 
                VALUES ((select club_id from club_managers where admin_id = %(id)s),%(eh)s,%(ec)s,%(ed)s,%(ei)s); """
                data = {
                    'id': id,
                    'eh': event.header,
                    'ec': event.content,
                    'ed': event.date,
                    'ei': event.image
                }
                cursor.execute(add_event_statement, data)
                self.conn.commit()
        except (Exception, dbapi2.Error) as error:
            print("Error while adding event: {}".format(error))

    #id adminin idsi, ann_id announcement idsi, announcement da announcement objesi
    def update_event(self, event_id, event,
                     img_update):  ####FIX IAMGE_URL TYPO
        update_statement = ""
        try:
            with self.conn.cursor() as cursor:
                if img_update:
                    update_statement = """UPDATE events SET 
                    header = %(eh)s, content = %(ec)s, date_ = %(ed)s, blob_image = %(ei)s 
                    WHERE id = """ + str(event_id)
                else:
                    update_statement = """UPDATE events SET 
                    header = %(eh)s, content = %(ec)s, date_ = %(ed)s
                    WHERE id = """ + str(event_id)
                data = {
                    'eh': event.header,
                    'ec': event.content,
                    'ed': event.date,
                    'ei': event.image
                }
                cursor.execute(update_statement, data)
                self.conn.commit()
        except (Exception, dbapi2.Error) as error:
            print("Error while updating event: {}".format(error))

    """
    def delete_club(self, club_key):
        if club_key in self.clubs:
            del self.clubs[club_key]
    """

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

    def get_announcement(self, ann_id):
        try:
            with self.conn.cursor() as cursor:
                get_ann_statement = """SELECT id,club_id,header,content,encode(announcements.blob_image, 'base64') as image FROM announcements WHERE id = %(ann_id)s """
                data = {'ann_id': ann_id}
                cursor.execute(get_ann_statement, data)
                ar = []
                announcement = cursor.fetchone()
                for an in announcement:
                    ar.append(an)
                if announcement:
                    if ar[4] != "" and ar[4]:
                        ar[4] = "data:image/png;base64," + ar[4]
                    return ar  ##bir announcement arrayi belki sonra obje yaparsın
                else:
                    return None
        except (Exception, dbapi2.Error) as error:
            print("Error while getting announcement {}".format(error))

    def get_event(self, event_id):
        try:
            with self.conn.cursor() as cursor:
                get_event_statement = """SELECT id, club_id, header, content,date_, encode(events.blob_image, 'base64') as image FROM events WHERE id = %(event_id)s """
                data = {'event_id': event_id}
                cursor.execute(get_event_statement, data)
                event = cursor.fetchone()
                event_ = []
                for ev in event:
                    event_.append(ev)
                if event:
                    if event_[5] != "" and event_[5]:
                        event_[5] = "data:image/png;base64," + event_[5]

                get_comments_statement = """SELECT comments.id, comments.event_id, comments.user_id, comments.content, comments.created_at, users.name, users.surname
                                        FROM comments LEFT JOIN users ON users.id = comments.user_id WHERE comments.event_id = %(event_id)s;"""
                cursor.execute(get_comments_statement, data)
                comments = cursor.fetchall()
                if comments:
                    return event_, comments
                if event:
                    comments = None
                    return event_, comments  ##bir event arrayi belki sonra obje yaparsın
                else:
                    return None
        except (Exception, dbapi2.Error) as error:
            print("Error while getting announcement {}".format(error))

    def get_event_info(self, event_id):
        try:
            with self.conn.cursor() as cursor:
                get_event_statement = """SELECT id, club_id, header, content,date_, encode(events.blob_image, 'base64') as image FROM events WHERE id = %(event_id)s """
                data = {'event_id': event_id}
                cursor.execute(get_event_statement, data)
                event = cursor.fetchone()
                event_ = []
                for ev in event:
                    event_.append(ev)
                if event:
                    if ev[5] != "" and ev[5]:
                        event_[5] = "data:image/png;base64," + event_[5]
                else:
                    return None
        except (Exception, dbapi2.Error) as error:
            print("Error while getting announcement {}".format(error))

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

    def get_announcements(self, club_id=None, all=True, admin_id=None):
        try:
            with self.conn.cursor() as cursor:
                if club_id:  ##all announcements of the club
                    get_anns_statement = """ SELECT id, club_id,header,content,encode(announcements.blob_image, 'base64') as image FROM announcements WHERE club_id = %(club_id)s;"""
                    data = {'club_id': club_id}
                    cursor.execute(get_anns_statement, data)
                    announcements = cursor.fetchall()
                    if announcements:
                        anns = []
                        for a in announcements:
                            x = list(a)
                            anns.append(x)
                        for ann in anns:
                            if ann[4] != "" and ann[4]:
                                ann[4] = "data:image/png;base64," + ann[4]
                        return anns
                    return None
                elif admin_id:  ##return the announcements to render for adminpage
                    get_anns_statement = """ SELECT id, club_id,header,content,encode(announcements.blob_image, 'base64') as image 
                    FROM announcements WHERE club_id = 
                    (SELECT club_id FROM club_managers WHERE admin_id = %(admin_id)s);"""
                    data = {'admin_id': admin_id}
                    cursor.execute(get_anns_statement, data)
                    announcements = cursor.fetchall()
                    if announcements:
                        anns = []
                        for a in announcements:  ##becaues it returns a list of tuples, convert all tuples to list so it is possible to do changes
                            x = list(a)
                            anns.append(x)
                        for ann in anns:
                            if ann[4] != "" and ann[4]:
                                ann[4] = "data:image/png;base64," + ann[4]
                        return anns
                    return None
                else:
                    if all:  ##for announcements page
                        get_anns_statement = """ SELECT id, club_id,header,content,encode(announcements.blob_image, 'base64') as image FROM announcements"""
                        cursor.execute(get_anns_statement)
                        announcements = cursor.fetchall()
                        if announcements:
                            anns = []
                            for a in announcements:
                                x = list(a)
                                anns.append(x)
                            for ann in anns:
                                if ann[4] != "" and ann[4]:
                                    ann[4] = "data:image/png;base64," + ann[4]
                            return anns
                        return None
                    if not all:  ##for main page sharing latest announcements
                        get_anns_statement = """ SELECT id, club_id,header,content,encode(announcements.blob_image, 'base64') as image FROM announcements LIMIT 5 """  ##orderby created at
                        cursor.execute(get_anns_statement)
                        announcements = cursor.fetchall()
                        if announcements:
                            anns = []
                            for a in announcements:
                                x = list(a)
                                anns.append(x)
                            for ann in anns:
                                if ann[4] != "" and ann[4]:
                                    ann[4] = "data:image/png;base64," + ann[4]
                            return anns
                        return None
        except (Exception, dbapi2.Error) as error:
            print("Error while getting announcements {}".format(error))

    def get_events(
        self,
        club_id=None,
        admin_id=None
    ):  ##only visible if user is member and visits the clubs page
        try:
            with self.conn.cursor() as cursor:
                if club_id:
                    get_events_statement = """ SELECT id, club_id, header, content, date_, encode(events.blob_image, 'base64') as image FROM events WHERE club_id = %(club_id)s;"""
                    data = {'club_id': club_id}
                    cursor.execute(get_events_statement, data)
                    events = cursor.fetchall()
                    if events:
                        evs = []
                        for e in events:
                            x = list(e)
                            evs.append(x)
                        for ev in evs:
                            if ev[5] and ev[5] != "":
                                ev[5] = "data:image/png;base64," + ev[5]
                        return evs
                    return None
                elif admin_id:
                    get_events_statement = """ SELECT id, club_id, header, content, date_, encode(events.blob_image, 'base64') as image 
                    FROM events WHERE club_id = 
                    (SELECT club_id FROM club_managers WHERE admin_id = %(admin_id)s);"""
                    data = {'admin_id': admin_id}
                    cursor.execute(get_events_statement, data)
                    events = cursor.fetchall()
                    if events:
                        evs = []
                        for e in events:
                            x = list(e)
                            evs.append(x)
                        for ev in evs:
                            if ev[5] and ev[5] != "":
                                ev[5] = "data:image/png;base64," + ev[5]
                        return evs
                    return None
                else:
                    abort(404)
        except (Exception, dbapi2.Error) as error:
            print("Error while getting announcements {}".format(error))

    def get_member_clubs(
        self, user_id
    ):  ##member club yoksa farklı bir sayfa yap üye olmaya başla diye ya da clubs_page e redirect
        member_clubs = []
        get_member_clubs_statement = """ SELECT clubs.id, clubs.name, clubs.description, 
                                            clubs.history, clubs.student_count, clubs.source, clubs.mission, clubs.vision, clubs.image_url
                                            FROM clubs, members, users 
                                            WHERE ( (users.id = """ + str(
            user_id) + """)
                                            AND (members.club_id = clubs.id) 
                                            AND (members.user_id = users.id) ) """
        #data = {'x': user_id}
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
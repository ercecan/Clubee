from datetime import datetime


class Club:
    def __init__(self,
                 name,
                 events,
                 announcements,
                 history,
                 vision,
                 mission,
                 student_count,
                 image_url,
                 description=None):
        self.name = name
        self.description = description
        self.events = events
        self.announcements = announcements
        self.history = history
        self.vision = vision
        self.mission = mission
        self.student_count = student_count
        self.image_url = image_url


class Announcement:
    def __init__(self, header, content, image):
        self.header = header
        self.content = content
        self.image = image


class Event:
    def __init__(self, header, content, image, date):
        self.header = header
        self.content = content
        self.image = image
        self.date = date

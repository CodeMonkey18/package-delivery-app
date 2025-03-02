import datetime


class Package:

    # constructor
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, delivery_status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.delivery_status = delivery_status
        self.departure_time = None
        self.delivery_time = None


    # print output as a readable string instead of the default "object at 0x000012352" reference
    def __str__(self):
        return "ID: %s, %s, %s, %s, %s, %s, %s, %s, Status: %s, Departed: %s, Delivered: %s" % (self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.notes, self.delivery_status, self.departure_time, self.delivery_time)

    # change package delivery status based on an inputted time
    # space and time complexity O(1)
    def update_status(self, time):
        if self.delivery_time < time:
            self.delivery_status = "Delivered"
        elif self.departure_time < time:
            self.delivery_status = "En route"
        elif self.delivery_status == 'None':
            self.delivery_status = 'At the hub'

        # the delivery time will always show by default
        # this overwrites the delivery time to 'Not Yet' if the package has not been delivered yet
        if self.delivery_time > time:
            self.delivery_time = 'Not Yet'

        # package 9 must display wrong address before 10:20 and the right address afterward
        if self.id == 9:
            if time > datetime.timedelta(hours=10, minutes=20):
                self.city = "Salt Lake City"
                self.state = "UT"
                self.zip = 84111
                self.address = "410 S. State St."
                self.notes = "Address Corrected!"


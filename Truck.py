class Truck:

    # constructor
    def __init__(self, speed, milage, curr_location, curr_time, packages, max_capacity):
        self.speed = speed
        self.milage = milage
        self.curr_location = curr_location
        self.curr_time = curr_time
        self.packages = packages
        self.max_capacity = max_capacity

    # return the object as a readable string
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.speed, self.milage, self.curr_location, self.curr_time, self.packages, self.max_capacity)

class Package:
    def __init__(self, ID, address, city, state, zip, deadline, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def set_status(self, current_time):
        if self.delivery_time and current_time > self.delivery_time:
            self.status = "Delivered"
        elif self.departure_time and current_time > self.departure_time:
            self.status = "En route"
        else:
            self.status = "At Hub"

    def __str__(self):
        return f"{self.ID}, {self.address}, {self.city}, {self.state}, {self.zip}, {self.deadline}, {self.weight}, {self.delivery_time}, {self.status}"

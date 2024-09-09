
class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline_time, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return f"{self.ID}, {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.deadline_time}, {self.weight}, {self.delivery_time}, {self.status}"

    def update_status(self, current_time):
        if self.delivery_time and self.delivery_time < current_time:
            self.status = "Delivered"
        elif self.departure_time and self.departure_time > current_time:
            self.status = "En route"
        else:
            self.status = "At Hub"
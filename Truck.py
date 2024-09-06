from datetime import datetime, timedelta

class Truck:
    def __init__(self, id, capacity=16, speed=18):
        self.id = id
        self.packages = []
        self.capacity = capacity
        self.speed = speed
        self.mileage = 0
        self.current_location = 0
        self.time = datetime.strptime("8:00 AM", "%I:%M %p")

    def load(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            return True
        return False

    def deliver(self, package, distance):
        travel_time = distance / self.speed
        self.time += timedelta(hours=travel_time)
        self.mileage += distance
        package.status = "Delivered"
        package.delivery_time = self.time
        self.packages.remove(package)


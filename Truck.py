class Truck:
    #Create truck attributes
    def __init__(self, number, load, packages, mileage, address, depart):
        self.number = number
        self.capacity = 16
        self.speed = 18
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart = depart
        self.time = depart

    def __str__(self):
        return f"{self.capacity}, {self.speed}, {self.load}, {self.packages}, {self.mileage}, {self.address}, {self.depart}"

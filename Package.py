# Create class for packages
class DeliveryPackage:
    def __init__(self, id, address, city, state, zip_code, deadline, weight, special_notes="", status="At hub"):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = status
        self.delivery_time = None

    def update_status(self, current_time):
        if self.delivery_time and current_time >= self.delivery_time:
            self.status = f"Delivered at {self.delivery_time.strftime('%I:%M %p')}"
        elif self.status != "At hub":
            self.status = "En route"


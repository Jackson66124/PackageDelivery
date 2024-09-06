from Truck import Truck
from HashTable import HashTable
import csv
from Package import DeliveryPackage
from datetime import datetime, timedelta

def load_packages(filename):
    packages = HashTable()
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            special_notes = row[7] if len(row) > 7 else ""
            package = DeliveryPackage(id, address, city, state, zip_code, deadline, weight, special_notes)
            packages.insert(package)
    return packages

def load_distances(filename):
    distances = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for i, row in enumerate(reader):
            distances[i] = {j: float(dist) if dist else 0 for j, dist in enumerate(row) if dist}
    return distances

def load_addresses(filename):
    addresses = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            addresses[row[1]] = int(row[0])  
    return addresses

def assign_packages_to_trucks(packages, trucks):
    all_packages = packages.all_packages()
    for package in all_packages:
        if "Can only be on truck 2" in package.special_notes:
            trucks[1].load(package)
        elif "Delayed" in package.special_notes:
            trucks[1].load(package)
        elif package.deadline != "EOD":
            trucks[0].load(package)
        else:
            # Assign to the truck with fewer packages
            if len(trucks[0].packages) <= len(trucks[1].packages):
                trucks[0].load(package)
            else:
                trucks[1].load(package)

def optimize_route(truck, distances, addresses):
    undelivered = truck.packages.copy()
    route = []
    current_location = 0  # Assume trucks start at the hub (index 0)

    while undelivered:
        nearest = min(undelivered, key=lambda p: distances[current_location].get(addresses.get(p.address, 0), float('inf')))
        route.append(nearest)
        current_location = addresses.get(nearest.address, 0)
        undelivered.remove(nearest)

    return route

def simulate_delivery(trucks, distances, addresses):
    for truck in trucks:
        optimized_route = optimize_route(truck, distances, addresses)
        current_location = 0  # Assume trucks start at the hub (index 0)
        for package in optimized_route:
            destination = addresses.get(package.address, 0)
            distance = distances[current_location].get(destination, 0)
            truck.deliver(package, distance)
            current_location = destination
        
        # Return to hub
        truck.mileage += distances[current_location].get(0, 0)
        truck.time += timedelta(hours=distances[current_location].get(0, 0) / truck.speed)

def update_package_status(packages, current_time):
    for package in packages.all_packages():
        package.update_status(current_time)

def display_package_status(package, current_time):
    print(f"Package {package.id}:")
    print(f"Address: {package.address}, {package.city}, {package.state} {package.zip_code}")
    print(f"Deadline: {package.deadline}")
    print(f"Weight: {package.weight}")
    package.update_status(current_time)
    print(f"Status: {package.status}")
    if package.special_notes:
        print(f"Special Notes: {package.special_notes}")
    print()

def display_all_packages(packages, trucks, current_time):
    update_package_status(packages, current_time)
    all_packages = packages.all_packages()
    all_packages.sort(key=lambda p: p.id)
    for package in all_packages:
        display_package_status(package, current_time)
    print(f"Packages on Truck 1: {len(trucks[0].packages)}")
    print(f"Packages on Truck 2: {len(trucks[1].packages)}")

def calculate_total_mileage(trucks):
    return sum(truck.mileage for truck in trucks)

def user_interface(packages, trucks):
    while True:
        print("\n1. View status of all packages")
        print("2. View status of a specific package")
        print("3. View total mileage")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            time_str = input("Enter time (HH:MM AM/PM): ")
            try:
                current_time = datetime.strptime(time_str, "%I:%M %p")
                display_all_packages(packages, trucks, current_time)
            except ValueError:
                print("Invalid time format. Please use HH:MM AM/PM.")
        elif choice == '2':
            package_id = int(input("Enter package ID: "))
            time_str = input("Enter time (HH:MM AM/PM): ")
            try:
                current_time = datetime.strptime(time_str, "%I:%M %p")
                package = packages.lookup(package_id)
                if package:
                    display_package_status(package, current_time)
                else:
                    print("Package not found.")
            except ValueError:
                print("Invalid time format. Please use HH:MM AM/PM.")
        elif choice == '3':
            total_mileage = calculate_total_mileage(trucks)
            print(f"Total mileage traveled by all trucks: {total_mileage:.2f} miles")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    packages = load_packages("CSV/WGUPS_Package_File.csv")
    distances = load_distances("CSV/WGUPS_Distance_Table.csv")
    addresses = load_addresses("CSV/Address_File.csv")

    trucks = [Truck(1), Truck(2)]
    
    assign_packages_to_trucks(packages, trucks)
    simulate_delivery(trucks, distances, addresses)
    user_interface(packages, trucks)

if __name__ == "__main__":
    main()
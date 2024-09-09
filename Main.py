import csv
import datetime
from Truck import Truck
from HashTable import HashMap
from Package import Package

def read_csv(filename):
    with open(filename, newline='') as csvfile:
        return list(csv.reader(csvfile))

def load_package_data(filename, package_hash_table):
    with open(filename, newline='') as package_info:
        for package in csv.reader(package_info):
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline_time = package[5]
            pWeight = package[6]
            pStatus = "At Hub"
            package_hash_table.insert(pID, Package(pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pStatus))

def distance_in_between(x_value, y_value, distances):
    distance = distances[x_value][y_value]
    return float(distance) if distance else float(distances[y_value][x_value])

def extract_address(address, address_list):
    for row in address_list:
        if address in row[2]:
            return int(row[0])
    return None

def delivering_packages(truck, package_hash_table, distances, addresses):
    # Retrieve all packages to be delivered
    not_delivered = [package_hash_table.lookup(pid) for pid in truck.packages]
    truck.packages.clear()
    
    # Initialize current location and mileage
    current_address_index = extract_address(truck.address, addresses)
    truck.mileage = 0.0
    truck.time = truck.depart_time
    
    while not_delivered:
        # Calculate distances from current address to all remaining packages
        distances_to_packages = []
        for package in not_delivered:
            package_address_index = extract_address(package.address, addresses)
            distance = distance_in_between(current_address_index, package_address_index, distances)
            distances_to_packages.append((distance, package))
        
        # Choose the nearest package
        next_distance, next_package = min(distances_to_packages, key=lambda x: x[0])
        
        # Update truck state
        truck.packages.append(next_package.ID)
        truck.mileage += next_distance
        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=next_distance / truck.speed)
        
        # Update package status
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time
        
        # Remove the delivered package from the list
        not_delivered.remove(next_package)
        
        # Update current location
        current_address_index = extract_address(next_package.address, addresses)

def parse_time_input(time_str):
    try:
        time_parts = time_str.strip().split()
        hm_parts = time_parts[0].split(':')
        hours = int(hm_parts[0])
        minutes = int(hm_parts[1])
        am_pm = time_parts[1].upper()

        if am_pm not in ['AM', 'PM']:
            raise ValueError("Invalid AM/PM indicator.")
        if hours < 1 or hours > 12 or minutes < 0 or minutes > 59:
            raise ValueError("Invalid hour or minute value.")

        if am_pm == 'PM' and hours != 12:
            hours += 12
        if am_pm == 'AM' and hours == 12:
            hours = 0

        return datetime.timedelta(hours=hours, minutes=minutes)
    except Exception as e:
        print(f"Error parsing time: {e}")
        return None

def main():
    distances = read_csv("CSV/WGUPS_Distance_Table.csv")
    addresses = read_csv("CSV/Address.csv")
    package_hash_table = HashMap()
    load_package_data("CSV/WGUPS_Package_File.csv", package_hash_table)
    
    truck1 = Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
    truck2 = Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
    truck3 = Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))
    
    delivering_packages(truck1, package_hash_table, distances, addresses)
    delivering_packages(truck2, package_hash_table, distances, addresses)
    truck3.depart_time = min(truck1.time, truck2.time)
    delivering_packages(truck3, package_hash_table, distances, addresses)
    
    print("Western Governors University Parcel Service (WGUPS)")
    print(f"The mileage for the route is: {truck1.mileage + truck2.mileage + truck3.mileage}")

    user_input = input("To start please type the word 'time': ").strip().lower()
    if user_input != "time":
        print("Entry invalid. Closing program.")
        return

    try:
        user_time_str = input("Please enter a time to check status of package(s). Use the format HH:MM AM/PM: ")
        current_time = parse_time_input(user_time_str)
        if current_time is None:
            print("Entry invalid. Closing program.")
            return

        second_input = input("To view the status of an individual package type 'solo'. For a rundown of all packages type 'all': ").strip().lower()
        if second_input == "solo":
            package_id = int(input("Enter the numeric package ID: "))
            package = package_hash_table.lookup(package_id)
            if package:
                package.update_status(current_time)
                print(package)
            else:
                print("Package ID not found.")
        elif second_input == "all":
            for package_id in range(1, 41):
                package = package_hash_table.lookup(package_id)
                if package:
                    package.update_status(current_time)
                    print(package)
                else:
                    print(f"Package ID {package_id} not found.")
        else:
            print("Entry invalid. Closing program.")
    except ValueError:
        print("Entry invalid. Closing program.")

if __name__ == "__main__":
    main()

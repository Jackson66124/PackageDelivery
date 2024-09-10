import csv
import datetime
from Truck import Truck
from HashTable import HashMap
from Package import Package

def csv_reader(filename):
    with open(filename, newline='') as csvfile:
        return list(csv.reader(csvfile))


def distance_between(x_value, y_value, distances):
    distance = distances[x_value][y_value]
    return float(distance) if distance else float(distances[y_value][x_value])

def get_address(address, address_list):
    return next((int(row[0]) for row in address_list if address in row[2]), None)

def load_package(filename, hash_table):
    with open(filename, newline='') as package_info:
        for package in csv.reader(package_info):
            ID = int(package[0])
            Address, City, State, Zip, Deadline, Weight = package[1:7]
            Status = "At Hub"
            hash_table.insert(ID, Package(ID, Address, City, State, Zip, Deadline, Weight, Status))

def deliver_packages(truck, package_hash_table, distances, addresses):
    not_delivered = [package_hash_table.lookup(pID) for pID in truck.packages]
    truck.packages.clear()
    
    current_address_index = get_address(truck.address, addresses)
    
    while not_delivered:
        package_distances = [
            (distance_between(current_address_index, get_address(package.address, addresses), distances), package)
            for package in not_delivered
        ]
        
        distance, package = min(package_distances, key=lambda x: x[0])
        
        truck.packages.append(package.ID)
        truck.mileage += distance
        truck.address = package.address
        truck.time += datetime.timedelta(hours=distance / truck.speed)
        
        package.delivery_time = truck.time
        package.departure_time = truck.depart
        package.status = "Delivered"
        
        not_delivered.remove(package)
        current_address_index = get_address(package.address, addresses)

def parse_time(time):
    try:
        hours_mins = time.strip().split()
        hours, minutes = map(int, hours_mins[0].split(':'))
        am_pm = hours_mins[1].upper()
        hours = hours % 12 + (12 if am_pm == 'PM' else 0)
        return datetime.timedelta(hours=hours, minutes=minutes)
    except:
        return None


def main():
    distance = csv_reader("CSV/WGUPS_Distance_Table.csv")
    address = csv_reader("CSV/Address.csv")
    package_hash_table = HashMap()
    load_package("CSV/WGUPS_Package_File.csv", package_hash_table)
    
    #Manually load trucks
    trucks = [
        Truck(None, [30, 13, 37, 16, 40, 1, 15, 34, 20, 31, 29, 14], 0.0, "4001 South 700 East", datetime.timedelta(hours=8)),
        Truck(None, [21, 27, 12, 35, 18, 24, 39, 6, 26, 17, 23, 38, 22, 19, 3, 36], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20)),
        Truck(None, [9, 28, 33, 7, 32, 4, 6, 10, 2, 25, 11, 5, 8], 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))
    ]
    
    for truck in trucks:
        deliver_packages(truck, package_hash_table, distance, address)
    
    total_mileage = sum(truck.mileage for truck in trucks)
    print("WGUPS")
    print(f"The total mileage is: {total_mileage:.2f}")

    time_input = ''
    while time_input != 'quit':
        print('Type "quit" to exit')
        time_input = input("What time do you want to check package status? Format: HH:MM AM/PM ")

        if time_input.lower() == 'quit':
            print('Exiting')
            break
        
        time = parse_time(time_input)
        while time is None:
            time_input = input('Invalid time, try again. What time do you want to check package status? Format: HH:MM AM/PM ')
            time = parse_time(time_input)

        time_input = input("To view a singular package type '1'. To view all packages type '2': ")
        if time_input == "1":
            package_id = int(input("Enter the package ID# (1-40): "))
            package = package_hash_table.lookup(package_id)
            if package:
                package.set_status(time)
                print(package)
            else:
                print("Package ID not found.")
        elif time_input == "2":
            for package_id in range(1, 41):
                package = package_hash_table.lookup(package_id)
                if package:
                    print(package)
                else:
                    print(f"Package ID {package_id} not found.")

if __name__ == "__main__":
    main()

# WGUPS Routing Program
# Christopher Kim
# ID - 011175374

import csv
import datetime

from Package import Package
from HashTable import HashTable
from Truck import Truck


# function that loads the package csv data into the hashtable
# time complexity O(n) - iterating through package_list pkg(n) times
# space complexity O(n) - creates a Package for each row(n) in the csv file
def load_package_data(csv_file):
    # open the csv file
    with open(csv_file) as package_file:
        # return a reader object
        package_list = csv.reader(package_file)

        # loop through the package list
        # for every row: store each value/field in a variable
        for pkg in package_list:
            pkg_id = int(pkg[0])
            pkg_address = pkg[1]
            pkg_city = pkg[2]
            pkg_state = pkg[3]
            pkg_zip = pkg[4]
            pkg_deadline = pkg[5]
            pkg_weight = pkg[6]
            pkg_notes = pkg[7]
            pkg_delivery_status = 'At Hub'

            # create a package object, passing in the newly created variables
            pkg = Package(pkg_id, pkg_address, pkg_city, pkg_state, pkg_zip, pkg_deadline, pkg_weight, pkg_notes,
                          pkg_delivery_status)
            # append the package object to the hashtable
            package_table.insert(pkg_id, pkg)


# create an empty hashtable
package_table = HashTable()

# load the package.csv data
load_package_data("CSV/package_data.csv")

# next process the other csv files
# store the file in a list, so we can retrieve the values via the indices
with open("CSV/addresses.csv") as address_file:
    address_list = list(csv.reader(address_file))

with open("CSV/distance_values.csv") as distance_file:
    distance_list = list(csv.reader(distance_file))


# Source used: C950 WGUPS Project Implementation Steps - Example - Nearest Neighbor
# define a function to extract the index in the address.csv file
# each row in the address csv is a list : [index 0, location name 1, address 2]
# the function will intake an address and spit out the corresponding [index]
# this will be used to map the addresses to the x,y columns in the distance csv file
def get_address(address):
    # time complexity O(n^2) | space complexity O(n)
    for row in address_list:
        if address in row[2]:
            return int(row[0])


# next, define a function to find the distance between 2 addresses
# time and space complexity O(1)
def get_distance(address_one, address_two):
    distance = distance_list[address_one][address_two]

    # in the distance csv matrix, half the fields are empty
    # but the matrix is a 2-D list, bla[6][2] = bla[2][6]
    # so we can substitute the empty fields with its inverse like so
    if distance == '':
        distance = distance_list[address_two][address_one]

    return float(distance)


# create 3 truck objects
# trucks cannot leave before 8:00, some packages will not arrive until 9:05, one package will be corrected at 10:20
# so set 3 separate departure times: 8, 9:05, and 10:20
truck_one = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                  [1, 13, 14, 15, 16, 19, 20, 21, 22, 23, 29, 30, 31, 34, 37, 40], 16)

# some packages can only be on truck 2
# these packages all have a deadline of 'EOD' so it's best for truck 2 to be the last to depart
truck_two = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20),
                  [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 17, 18, 35, 36, 38], 16)
truck_three = Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
                    [6, 24, 25, 26, 27, 28, 32, 33, 39], 16)

# variable to check if a truck has finished their deliveries
finished = False

# create function to deliver the packages
# time complexity O(n^2) - outer loop iterates through deliveries while > 0, inner loop iterate through it for closest package
# space complexity O(n) - creating a deliveries list with n packages
def deliver_packages(truck):

    # store the to-be-delivered packages in a new list
    deliveries = []
    for pkg_id in truck.packages:
        # add the packages in the truck to the deliveries list
        package = package_table.lookup(pkg_id)
        deliveries.append(package)
    # empty the truck's package list, so the packages can be re-added later in the correct delivery order
    truck.packages.clear()

    # set the departure time of all packages in the truck's deliveries list
    for package in deliveries:
        package.departure_time = truck.curr_time

    while len(deliveries) > 0:
        target_address = 1000
        target_package = None
        # nearest neighbor algorithm
        # find the distance between the truck's current location and every package in the deliveries list
        # the closest package becomes the target_package to be dropped off next
        for package in deliveries:
            if get_distance(get_address(truck.curr_location), get_address(package.address)) <= target_address:
                target_address = get_distance(get_address(truck.curr_location), get_address(package.address))
                target_package = package

        # the target package is re-added to the truck's package list
        truck.packages.append(target_package.id)
        # it is "dropped off" and removed from the to-be-delivered list
        deliveries.remove(target_package)
        # add the distance traveled to the truck's milage; set the truck's new location to where the package was dropped off
        truck.milage += target_address
        truck.curr_location = target_package.address
        # the truck travels at 18mph
        # advance the current time by the (distance traveled / 18)
        truck.curr_time += datetime.timedelta(hours=target_address / 18)
        target_package.delivery_time = truck.curr_time

    # once the delivery list is empty, the driver is freed up
    if not deliveries:
        global finished
        finished = True

# call the function to start each truck and begin deliveries
deliver_packages(truck_one)
deliver_packages(truck_three)
# there are 2 drivers, so truck_two must wait at hub until either truck 1 or 3 finishes their deliveries
if finished:
    deliver_packages(truck_two)

###   #   ###
# Interface #
###   #   ###

print("WGUPS Package Tracker")
print("The total milage for today's deliveries is: ", (truck_one.milage + truck_two.milage + truck_three.milage), "miles.")

while True:
    try:
        user_time = input("Please enter a time that you would like to view the status of one or more packages at (HH:MM)")
        (hh, mm) = user_time.split(':')
        convert_time = datetime.timedelta(hours=int(hh), minutes=int(mm))
    except ValueError:
        print("Sorry, that is not a valid time. Please enter a different value.")
    else:
        break

user_choice = input("Press 1 to check the status of one package. Or press 2 to check the status of all packages.")
if user_choice == '1':
    try:
        user_package = input("Which package would you like to check? Please enter the package's ID number (1-40).")
        convert_package = package_table.lookup(int(user_package))
        convert_package.update_status(convert_time)
        print(str(convert_package))
    except ValueError:
        print("Sorry, that is not a valid entry. Exiting program.")
elif user_choice == '2':
    all_packages = range(1,41)
    for package in all_packages:
        pkg = package_table.lookup(package)
        pkg.update_status(convert_time)
        print(str(pkg))
else:
    print("Sorry, that is not a valid entry. Exiting program.")
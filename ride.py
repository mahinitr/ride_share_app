from threading import Lock
import json
lock = Lock()


from models.in_memory_data import MemoryData

memory_data = MemoryData.instance()

class Ride:
    def __init__(self, src, dest, user, price): 
        self.src = src
        self.dest = dest
        self.status = None
        self.user = user
        self.travellers = []
        self.availability = user.vehicle.capacity
        self.ride_price = price

    def __str__(self):
        return self.src + " - " + self.dest + " - "  + self.user.name + " - " + str(self.availability) + " - " + str(self.ride_price)

    def assignRide(self, user, seats):
        # use thread locking here..
        try:
            lock.acquire()
            if self.status == 0:
                print "Ride is inctive"
            if self.availability <= 0 or \
                self.availability < seats:
                print "Unable to assign"
                return False
            self.availability =  self.availability - seats
            self.user.rides_offered = self.user.rides_offered + 1
            user.rides_taken = user.rides_taken + 1
            self.travellers.append(user)
            return True
        finally:
            lock.release()
        
        

class Map: 
    def __init__(self): 
        self.locations = {}
        self.rides = {}
  
    def add_ride(self, src, dest, user, price):
        if src not in self.locations:
            self.locations[src] = []
        if dest not in self.locations[src]:
            self.locations[src].append(dest)

        SRC_DEST = src + "_" + dest
        if SRC_DEST not in self.rides:
            self.rides[SRC_DEST] = []
        ride = Ride(src, dest, user, price)
        self.rides[SRC_DEST].append(ride)
        ride.status = 1
        return ride


    def fetch_ride(self, src, dest, seats):
        if src not in self.locations:
            print "No ride found"
            return None
        adj_loc = self.locations[src]
        if dest not in adj_loc:
            print "No ride found"
            return None
        SRC_DEST = src + "_" + dest
        rides = self.rides[SRC_DEST]
        avl_rides = []
        for ride in rides:
            if ride.status == 1 and ride.availability > 0 and \
                ride.availability >= seats:
                avl_rides.append(ride)
        if len(avl_rides) == 0:
            print "No ride found"
            return None
        # 1-selection strategy
        best_ride = avl_rides[0]
        for i in range(1, len(avl_rides)):
            if avl_rides[i].ride_price < best_ride.ride_price:
                best_ride = avl_rides[i]

        return best_ride

            

class RideManager:

    _instance = None

    def __init__(self):
        self.map = Map()
        self.users_rides = {}
        
    def start_ride(self, data):
        if "user_id" not in data or \
            "price" not in data or \
            "destination" not in data:
            print "Required data not given(user_id, destination, price)"
            return False
        u_id = data["user_id"]
        if u_id not in memory_data.users:
            print "User does not exist"
            return False
        user = memory_data.users[u_id]
        if not user.vehicle:
            print "User does not have vehicle"
            return False
        src = user.location.location
        dest = data["destination"]
        price = data["price"]
        ride = self.map.add_ride(src, dest, user, price)
        print str(ride), user.name
        self.users_rides[u_id] = ride
        return True

    def stopRide(self, data):
        if "user_id" not in data or \
            "destination" not in data:
            print "Required data not given(user_id, destination)"
            return False
        u_id = data["user_id"]
        if u_id not in memory_data.users:
            print "User does not exist"
            return False
        if u_id not in self.users_rides:
            print "No rides found with this user"
            return False
        ride = self.users_rides[u_id]
        ride.status = 0
        return True
        

    def requestRide(self, data):
        if "user_id" not in data or \
            "destination" not in data or \
            "seats" not in data:
            print "Required data not given(user_id, destination, seats)"
            return False
        u_id = data["user_id"]
        if u_id not in memory_data.users:
            print "User does not exist"
            return False
        user = memory_data.users[u_id]
        src = user.location.location
        dest = data["destination"]
        seats = data["seats"]
        ride = self.map.fetch_ride(src, dest, seats)
        print str(ride)
        if not ride:
            print "Unabe to assign ride"
            return False
        if ride.assignRide(user, seats):
            print "Assigned ride"
            return True
        return False

    def reports(self, u_id):
        reports = {}
        if u_id not in memory_data.users:
            print "User does not exist"
            return {}
        user = memory_data.users[u_id]
        reports["rides_offered"] = user.rides_offered
        reports["rides_taken"] = user.rides_taken
        return reports


    @staticmethod
    def instance():
        if RideManager._instance == None:
            RideManager._instance = RideManager()
        return RideManager._instance





from location import Location
from vehicle import Vehicle
from in_memory_data import MemoryData

memory_data = MemoryData.instance()

NEXT_USER_ID = 0

class User:

    def __init__(self):
        self.id = ""
        self.name = ""
        self.phone = ""
        self.location = None
        self.source_loc = None
        self.dest_loc = None
        self.vehicle = None
        self.rides_offered = 0
        self.total_earnings = 0
        self.rides_taken = 0

    @staticmethod
    def register_user(data):
        if "phone" not in data or \
            "name" not in data or \
            "location" not in data:
            print "Required data is not provided(phone, name, location)"
            return False
        global NEXT_USER_ID
        NEXT_USER_ID = NEXT_USER_ID + 1
        user = User()
        user.id = str(NEXT_USER_ID)
        user.name = data["name"]
        user.phone = data["phone"]
        loc = data["location"]
        user.location = Location(loc)
        memory_data.addUser(user)
        memory_data.addLocation(user.location)
        return True

    @staticmethod
    def addVehicle(data):
        if "user_id" not in data or \
            "vehicle_no" not in data or \
            "capacity" not in data:
            print "Required data not given(user_id, vehicle_no, capacity)"
            return False
        u_id = data["user_id"]
        if u_id not in memory_data.users:
            print "User does not exist"
            return False
        v_id = data["vehicle_no"]
        if v_id in memory_data.vehicles:
            print "Vehcile is already added"
            return False
        user = memory_data.users[u_id]
        v = Vehicle(v_id, v_id, int(data["capacity"]))
        memory_data.addVehicle(v)
        user.vehicle = v
        return True

    @staticmethod
    def start_ride(data):
        pass

    @staticmethod
    def get_ride(data):
        pass




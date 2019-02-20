
class MemoryData:

    _instance = None

    def __init__(self):
        self.users = {}
        self.locations = {}
        self.vehicles = {}

    def addUser(self, user):
        if user.id not in self.users:
            self.users[user.id] = user

    def addLocation(self, loc):
        if loc.id not in self.locations:
            self.locations[loc.id] = loc

    def addVehicle(self, vehicle):
        if vehicle.id not in self.vehicles:
            self.vehicles[vehicle.id] = vehicle

    @staticmethod
    def instance():
        if MemoryData._instance == None:
            MemoryData._instance = MemoryData()
        return MemoryData._instance


import unittest
from ride import RideManager
from models.user import User

class TestRideApp(unittest.TestCase):

    def setUp(self):
        user_1 = {"name":"M", "phone":"1", "location":"A"}
        user_2 = {"name":"N", "phone":"1", "location":"A"}
        vehicle_1 = {"user_id":"1", "vehicle_no":"1_1", "capacity":"3"}
        User.register_user(user_1)
        User.register_user(user_2)
        User.addVehicle(vehicle_1)

    def test_start_ride(self):
        ride_mgr = RideManager.instance()
        ride_1 = {"user_id":"1", "destination":"B", "price" : 100}
        self.assertTrue(ride_mgr.start_ride(ride_1))
        ride_1 = {"user_id":"2", "destination":"B", "price" : 100}
        self.assertFalse(ride_mgr.start_ride(ride_1))

    def test_stop_ride(self):
        ride_mgr = RideManager.instance()
        ride_1 = {"user_id":"1", "destination":"B"}
        self.assertTrue(ride_mgr.stopRide(ride_1))
        ride_1 = {"user_id":"2", "destination":"B"}
        self.assertFalse(ride_mgr.stopRide(ride_1))

    def test_request_ride(self):
        ride_mgr = RideManager.instance()
        ride_1 = {"user_id":"1", "destination":"B", "price" : 100}
        self.assertTrue(ride_mgr.start_ride(ride_1))
        ride_1 = {"user_id":"2", "destination":"B", "price":"100", "seats":1}
        self.assertTrue(ride_mgr.requestRide(ride_1))
        ride_1 = {"user_id":"2", "destination":"C", "price":"100", "seats":1}
        self.assertFalse(ride_mgr.requestRide(ride_1))

    def test_reports(self):
        ride_mgr = RideManager.instance()
        ride_1 = {"user_id":"1", "destination":"B", "price" : 100}
        self.assertTrue(ride_mgr.start_ride(ride_1))
        ride_1 = {"user_id":"2", "destination":"B", "price":"100", "seats":1}
        self.assertTrue(ride_mgr.requestRide(ride_1))
        ride_1 = {"user_id":"2", "destination":"C", "price":"100", "seats":1}
        self.assertFalse(ride_mgr.requestRide(ride_1))

        reports = ride_mgr.reports("1")
        self.assertEquals(reports, {'rides_taken': 0, 'rides_offered': 1})

        reports = ride_mgr.reports("2")
        self.assertEquals(reports, {'rides_taken': 1, 'rides_offered': 0})



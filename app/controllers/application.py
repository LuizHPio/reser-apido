from bottle import template, LocalRequest, LocalResponse
from .db.RoomController import RoomController
from .db.EquipmentController import EquipmentController
from .auth import Auth


class Application():

    def __init__(self):
        self.pages = {
            "landing": self.landing,
            "login": self.login,
            "register": self.register,
        }

    @staticmethod
    def show_reserves(request: LocalRequest):
        user_id = Auth.get_userid(request)
        reserved_rooms = RoomController.get_rooms(user_id)
        reserved_equipment = EquipmentController.get_equipments(user_id)
        access_token, _ = Auth.get_token_pair(request)

        return template('reserves', reserved_rooms=reserved_rooms, reserved_equipment=reserved_equipment, role=access_token.role)

    @staticmethod
    def show_admin(request: LocalRequest):
        rooms = RoomController.get_rooms()
        equipments = EquipmentController.get_equipments()
        access_token, _ = Auth.get_token_pair(request)

        return template('admin', equipments=equipments, rooms=rooms, role=access_token.role)

    def render(self, page):
        content = self.pages.get(page, self.helper)
        return content()

    def helper(self):
        return template('helper')

    def landing(self):
        return template('landing')

    def login(self):
        return template('login')

    def register(self):
        return template('register')

    @staticmethod
    def show_home(request: LocalRequest):
        room_list = RoomController.get_rooms()
        equipment_list = EquipmentController.get_equipments()
        access_token, _ = Auth.get_token_pair(request)

        return template('home', salas=room_list, equipment_list=equipment_list, role=access_token.role)

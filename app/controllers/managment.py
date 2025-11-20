from .db.RoomController import RoomController
from .db.EquipmentController import EquipmentController
from .auth import Auth
from bottle import LocalRequest


class Managment:

    @staticmethod
    def reserve_room(id, session_id):
        status = RoomController.reserve_room(id, session_id)

        if status:
            return '<script>alert("Sala reservada com sucesso"); window.location.replace("/home");</script>'
        else:
            return '<script>alert("Um erro foi encontrado ao tentar reservar a sala"); window.location.replace("/home");</script>'

    @staticmethod
    def unreserve_room(id, request: LocalRequest):
        user_id = Auth.get_userid(request)
        status = RoomController.unreserve_room(id, user_id)

        if status:
            return '<script>alert("Sala liberada com sucesso"); window.location.replace("/home");</script>'
        else:
            return '<script>alert("Um erro foi encontrado ao tentar liberar a sala"); window.location.replace("/home");</script>'

    @staticmethod
    def reserve_equipment(id, request: LocalRequest):
        session_id = Auth.get_userid(request)
        status = EquipmentController.reserve_equipment(id, session_id)

        if status:
            return '<script>alert("Equipamento reservado com sucesso"); window.location.replace("/home");</script>'
        else:
            return '<script>alert("Um erro foi encontrado ao tentar reservar o equipamento"); window.location.replace("/home");</script>'

    @staticmethod
    def unreserve_equipment(id, request: LocalRequest):
        user_id = Auth.get_userid(request)
        status = EquipmentController.unreserve_equipment(id, user_id)

        if status:
            return '<script>alert("Equipamento liberado com sucesso"); window.location.replace("/home");</script>'
        else:
            return '<script>alert("Um erro foi encontrado ao tentar liberar o equipamento"); window.location.replace("/home");</script>'

    @staticmethod
    def create_room(request: LocalRequest):
        name = request.forms.get("name")
        description = request.forms.get("description")
        is_available = request.forms.get("available")

        status = RoomController.create_room(name, description, is_available)

        if status:
            return '<script>alert("Sala criada com sucesso"); window.location.replace("/admin");</script>'
        else:
            return '<script>alert("Um erro foi encontrado ao tentar criar a sala"); window.location.replace("/admin");</script>'

    @staticmethod
    def delete_room(id: int):

        status = RoomController.delete_room(id)

        if status:
            return '<script>alert("Sala deletada com sucesso"); window.location.replace("/admin");</script>'
        else:
            return '<script>alert("Um erro foi encontrado ao tentar deletar a sala"); window.location.replace("/admin");</script>'

    @staticmethod
    def create_equipment(request: LocalRequest):
        name = request.forms.get("name")
        description = request.forms.get("description")
        is_available = request.forms.get("available")

        status = EquipmentController.create_equipment(
            name, description, is_available)

        if status:
            return '<script>alert("Equipamento criado com sucesso"); window.location.replace("/admin");</script>'
        else:
            return '<script>alert("Um erro foi encontrado ao tentar criar o equipamento"); window.location.replace("/admin");</script>'

    @staticmethod
    def delete_equipment(id: int):

        status = EquipmentController.delete_equipment(id)

        if status:
            return '<script>alert("Equipamento deletada com sucesso"); window.location.replace("/admin");</script>'
        else:
            return '<script>alert("Um erro foi encontrado ao tentar deletar o equipamento"); window.location.replace("/admin");</script>'

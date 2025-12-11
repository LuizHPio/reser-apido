from .db.RoomController import RoomController
from .db.EquipmentController import EquipmentController
from .auth import Auth
from bottle import LocalRequest
from typing import Literal
import socketio


class Managment:
    sio: socketio.Server
    user_socket_map: dict[str, int] = {}

    @classmethod
    def configure(cls, sio: socketio.Server, user_sessions: dict[str, int]):
        cls.sio = sio
        cls.user_socket_map = user_sessions

    @classmethod
    def emit_request_status(cls, event_name: str, user_id: str, object_id: int, resource_type: Literal["room", "equipment"], status: bool, fail_message: str = "Um erro foi encontrado ao executar a sua solicitação."):
        if status:
            cls.sio.emit(event_name, (object_id, resource_type))
        else:
            cls.sio.emit("warning", fail_message,
                         to=cls.user_socket_map[user_id])

    @classmethod
    def reserve_room(cls, id, user_id):
        status = RoomController.reserve_room(id, user_id)

        cls.emit_request_status(
            "successful-reserve",
            user_id,
            id,
            "room",
            status,
            "Um erro foi encontrado ao tentar reservar a sala"
        )

        return

    @classmethod
    def unreserve_room(cls, id: int, request: LocalRequest, sio: socketio.Server):
        user_id = Auth.get_userid(request)
        status = RoomController.unreserve_room(id, user_id)

        if user_id == None:
            return

        cls.emit_request_status(
            "successful-unreserve",
            user_id,
            id,
            "room",
            status,
            "Um erro foi encontrado ao tentar liberar a sala"
        )

    @classmethod
    def reserve_equipment(cls, id, request: LocalRequest):
        user_id = Auth.get_userid(request)
        status = EquipmentController.reserve_equipment(id, user_id)

        if user_id == None:
            return

        cls.emit_request_status(
            "successful-reserve",
            user_id,
            id,
            "equipment",
            status,
            "Um erro foi encontrado ao tentar reservar o equipamento"
        )

    @classmethod
    def unreserve_equipment(cls, id, request: LocalRequest):
        user_id = Auth.get_userid(request)
        status = EquipmentController.unreserve_equipment(id, user_id)

        if user_id == None:
            return

        cls.emit_request_status(
            "successful-unreserve",
            user_id,
            id,
            "equipment",
            status,
            "Um erro foi encontrado ao tentar liberar o equipamento"
        )

    @staticmethod
    def create_room(request: LocalRequest):
        # Bottle magic
        name = request.forms.get("name")  # type: ignore
        description = request.forms.get("description")  # type: ignore
        is_available = request.forms.get("available")  # type: ignore

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
        # Bottle magic
        name = request.forms.get("name")  # type: ignore
        description = request.forms.get("description")  # type: ignore
        is_available = request.forms.get("available")  # type: ignore

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

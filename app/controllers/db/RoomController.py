from .database import db
from .models.Room import Room
from .models.Equipment import Equipment
from peewee import DoesNotExist, IntegrityError, ModelSelect
from dataclasses import dataclass


@dataclass
class IRoom:
    id: int
    name: str
    description: str
    available: str


class RoomController:
    @db.atomic()
    @staticmethod
    def delete_room(id) -> bool:
        try:
            Room.delete_by_id(id)
        except Exception as e:
            print("Request failed, try again.", e)
            return False

        return True

    @db.atomic()
    @staticmethod
    def create_room(name, description, is_available) -> bool:
        try:
            Room.create(name=name, description=description,
                        is_available=is_available, owner=None)
        except Exception as e:
            print("Request failed, try again.", e)
            return False

        return True

    @db.atomic()
    @staticmethod
    def get_rooms(user_id=None) -> list[IRoom]:
        if user_id == None:
            rooms = Room.select()
        else:
            rooms = Room.select().where(Room.owner == user_id)

        room_list: list[IRoom] = []

        for room in rooms:
            room: Room
            room_list.append(
                IRoom(room.id, room.name, room.description, room.available))

        return room_list

    @db.atomic()
    @staticmethod
    def reserve_room(id, user_id) -> bool:
        try:
            room: Room = Room.get_by_id(id)
        except:
            print("Room not found")
            return False

        if not room.available:
            print("Room not available")
            return False

        room.owner = user_id
        room.available = False
        room.save()

        return True

    @db.atomic()
    @staticmethod
    def unreserve_room(room_id, user_id) -> bool:
        try:
            room: Room = Room.get_by_id(room_id)
        except:
            print("Room not found")
            return False

        if room.available:
            print("Room available")
            return False

        if str(room.owner) != user_id:
            print("You're not the owner of the room")
            return True

        room.owner = None
        room.available = True
        room.save()

        return True

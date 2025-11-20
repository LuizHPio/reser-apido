from .database import db
from .models.Equipment import Equipment
from dataclasses import dataclass


@dataclass
class IEquipment:
    id: int
    name: str
    description: str
    available: str


class EquipmentController:

    @db.atomic()
    @staticmethod
    def delete_equipment(id) -> bool:
        try:
            Equipment.delete_by_id(id)
        except Exception as e:
            print("Request failed, try again.", e)
            return False

        return True

    @db.atomic()
    @staticmethod
    def create_equipment(name, description, is_available) -> bool:
        try:
            Equipment.create(name=name, description=description,
                             is_available=is_available, owner=None)
        except Exception as e:
            print("Request failed, try again.", e)
            return False

        return True

    @db.atomic()
    @staticmethod
    def reserve_equipment(id, user_id) -> bool:
        try:
            equipment: Equipment = Equipment.get_by_id(id)
        except:
            print("Equipment not found")
            return False

        if not equipment.available:
            print("Equipment not available")
            return False

        equipment.owner = user_id
        equipment.available = False
        equipment.save()

        return True

    @db.atomic()
    @staticmethod
    def unreserve_equipment(equipment_id, user_id) -> bool:
        try:
            equipment: Equipment = Equipment.get_by_id(equipment_id)
        except:
            print("equipment not found")
            return False

        if equipment.available:
            print("equipment available")
            return False

        if str(equipment.owner) != user_id:
            print("You're not the owner of the equipment")
            return True

        equipment.owner = None
        equipment.available = True
        equipment.save()

        return True

    @db.atomic()
    @staticmethod
    def get_equipments(user_id=None) -> list[IEquipment]:
        if user_id == None:
            equipments = Equipment.select()
        else:
            equipments = Equipment.select().where(Equipment.owner == user_id)

        equipment_list: list[IEquipment] = []

        for equipment in equipments:
            equipment: Equipment
            equipment_list.append(
                IEquipment(equipment.id, equipment.name, equipment.description, equipment.available))

        return equipment_list

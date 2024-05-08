# poetry run python -m unittest

from abc import ABC, abstractmethod
from typing import Any, Callable, List, Dict
from dataclasses import dataclass

import unittest


@dataclass
class Item:
    name: str


class IInventory(ABC):
    @abstractmethod
    def add(self, item: Item): ...

    @abstractmethod
    def remove(self, item: Item): ...

    @abstractmethod
    def get(self, name: str) -> Item: ...

    @abstractmethod
    def amount(self, name) -> bool: ...


class Inventory(IInventory):
    def __init__(self) -> None:
        self.items: List[Item] = []

    def add(self, item: Item):
        self.items.append(item)

    def remove(self, item: Item):
        self.items.remove(item)

    def get(self, name: str) -> Item:
        try:
            return list(filter(lambda item: item.name == name, self.items))[0]
        except IndexError:
            raise Exception("Not found")

    def amount(self, name: str) -> int:
        return len(list(filter(lambda item: item.name == name, self.items)))

class ICraft(ABC):
    @abstractmethod
    def craft(self, name: str, inventory: IInventory) -> Item:
        ...

    @abstractmethod
    def can_craft(self) -> bool:
        ...

class OnTheKneeCrafter(ICraft):
    def __init__(self):
        self.recipe = {
            'BasicTorpedo': {
                'Steel': 1,
                'Chip': 1,
                'Fuel': 1
            },
            'PhotonTorpedo': {
                'Steel': 1,
                'Chip': 1,
                'Photon': 2
            }
        }

    def craft(self, name: str, inventory: IInventory) -> Item:
        recipe = self.recipe[name]
        for ingr in recipe:
            for i in range(recipe[ingr]):
                inventory.remove(Item(ingr))
        inventory.add(Item(name))

    def can_craft(self) -> bool:
        raise NotImplementedError()


class Icommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...


class CraftCommand(Icommand):
    def __init__(self, inventory: IInventory, name: str, crafter: ICraft, recipe: Dict[str, int] = None):
        self.inventory = inventory
        self.name = name
        self.recipe = recipe
        self.crafter = crafter

    def execute(self) -> None:
        if not self.recipe:
            if not self.crafter:
                self.crafter = OnTheKneeCrafter()
            self.crafter.craft(self.name, self.inventory)
        elif self.recipe:
            for ingr in self.recipe:
                for i in range(self.recipe[ingr]):
                    self.inventory.remove(Item(ingr))
            self.inventory.add(Item(self.name))


class TestOTUSRefactoring(unittest.TestCase):
    # @unittest.skip
    def test_craft_basic_torpedo1(self):
        # Arrange
        inventory = Inventory()
        inventory.add(Item("Steel"))
        inventory.add(Item("Chip"))
        inventory.add(Item("Fuel"))

        # Act
        inventory.remove(Item("Steel"))
        inventory.remove(Item("Chip"))
        inventory.remove(Item("Fuel"))
        inventory.add(Item("BasicTorpedo"))
        # Assert
        self.assertEquals(inventory.amount("Steel"), 0)
        self.assertEquals(inventory.amount("Chip"), 0)
        self.assertEquals(inventory.amount("Fuel"), 0)
        self.assertEquals(inventory.amount("BasicTorpedo"), 1)

    def test_craft_basic_torpedo2(self):
        # Arrange
        inventory = Inventory()
        inventory.add(Item("Steel"))
        inventory.add(Item("Chip"))
        inventory.add(Item("Fuel"))

        # Act
        CraftCommand(inventory, 'BasicTorpedo').execute()
        # Assert
        self.assertEquals(inventory.amount("Steel"), 0)
        self.assertEquals(inventory.amount("Chip"), 0)
        self.assertEquals(inventory.amount("Fuel"), 0)
        self.assertEquals(inventory.amount("BasicTorpedo"), 1)

    def test_craft_photon_torpedo1(self):
        # Arrange
        inventory = Inventory()
        inventory.add(Item("Steel"))
        inventory.add(Item("Chip"))
        inventory.add(Item("Photon"))
        inventory.add(Item("Photon"))

        # Act
        CraftCommand(inventory, 'PhotonTorpedo').execute()
        # Assert
        self.assertEquals(inventory.amount("Steel"), 0)
        self.assertEquals(inventory.amount("Chip"), 0)
        self.assertEquals(inventory.amount("Photon"), 0)
        self.assertEquals(inventory.amount("PhotonTorpedo"), 1)

    def test_craft_photon_torpedo2(self):
        # Arrange
        inventory = Inventory()
        inventory.add(Item("Steel"))
        inventory.add(Item("Chip"))
        inventory.add(Item("Photon"))
        inventory.add(Item("Photon"))

        recipe = {
            'Steel': 1,
            'Chip': 1,
            'Photon': 2
        }

        # Act
        CraftCommand(inventory, 'PhotonTorpedo', recipe).execute()
        # Assert
        self.assertEquals(inventory.amount("Steel"), 0)
        self.assertEquals(inventory.amount("Chip"), 0)
        self.assertEquals(inventory.amount("Photon"), 0)
        self.assertEquals(inventory.amount("PhotonTorpedo"), 1)

    def test_craft_photon_torpedo3(self):
        # Arrange
        inventory = Inventory()
        inventory.add(Item("Steel"))
        inventory.add(Item("Chip"))
        inventory.add(Item("Photon"))
        inventory.add(Item("Photon"))

        crafter = OnTheKneeCrafter()

        # Act
        CraftCommand(inventory, 'PhotonTorpedo', crafter=crafter).execute()
        # Assert
        self.assertEquals(inventory.amount("Steel"), 0)
        self.assertEquals(inventory.amount("Chip"), 0)
        self.assertEquals(inventory.amount("Photon"), 0)
        self.assertEquals(inventory.amount("PhotonTorpedo"), 1)
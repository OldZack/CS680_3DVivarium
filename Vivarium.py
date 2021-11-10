"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Created on 20181028

:author: micou(Zezhou Sun), Zack (Wanzhi Wang)
:version: 2021.11.09
"""
import random

import ColorType
from Point import Point
from Component import Component
from Animation import Animation
from ModelTank import Tank
from ModelLinkage import Predator, Prey, Food
from EnvironmentObject import EnvironmentObject


class Vivarium(Component, Animation):
    """
    The Vivarium for our animation
    """
    components = None  # List
    parent = None  # class that have current context
    tank = None
    tank_dimensions = None
    creatures = None  # Keep track of the creatures in Tank

    ##### BONUS 5(TODO 5 for CS680 Students): Feed your creature
    # Requirements:
    #   Add chunks of food to the vivarium which can be eaten by your creatures.
    #     * When ‘f’ is pressed, have a food particle be generated at random within the vivarium.
    #     * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of
    #     the vivarium and remain there within the tank until eaten.
    #     * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.

    def __init__(self, parent):
        self.parent = parent

        self.tank_dimensions = [4, 4, 4]
        tank = Tank(parent, self.tank_dimensions)
        super(Vivarium, self).__init__(Point((0, 0, 0)))

        # Build relationship
        self.addChild(tank)
        self.tank = tank

        # Store all components in one list, for us to access them later
        self.components = [tank]
        self.creatures = []
        # Add five preys and  one predator
        self.addNewObjInTank(Prey(parent, Point(
            (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.BLUE))
        self.addNewObjInTank(Prey(parent, Point(
            (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.GREEN))
        self.addNewObjInTank(Prey(parent, Point(
            (-1.7+random.random()*3.4, -1.7+random.random()*3.4, -1.7+random.random()*3.4)), ColorType.PINK))
        self.addNewObjInTank(Predator(parent, Point((-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4))))

    # This function resets the vivarium
    def reset(self):
        for c in self.creatures:
            self.delObj(c)
        self.creatures = []
        self.addNewObjInTank(Prey(self.parent, Point(
            (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
                                  ColorType.BLUE))
        self.addNewObjInTank(Prey(self.parent, Point(
            (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
                                  ColorType.GREEN))
        self.addNewObjInTank(Prey(self.parent, Point(
            (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4)),
                                  ColorType.PINK))
        self.addNewObjInTank(Predator(self.parent, Point(
            (-1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4, -1.7 + random.random() * 3.4))))
        self.update()

    # This function adds a food to the vivarium
    def add_food(self):
        self.addNewObjInTank(Food(self.parent, Point((-1.8+random.random()*3.8, 1.8, -1.8+random.random()*3.8))))
        self.update()

    def animationUpdate(self):
        """
        Update all creatures in vivarium
        """
        for c in self.components[::-1]:
            if isinstance(c, EnvironmentObject):
                if c.species_id == 1 or c.species_id == 0:
                    if (c.vanish_flag):
                        self.delObjInTank(c)
                        self.update()
            if isinstance(c, Animation):
                c.animationUpdate()

    def delObjInTank(self, obj):
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            self.creatures.remove(obj)
            del obj

    # A delete function specifically called in reset()
    def delObj(self, obj):
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            del obj

    def addNewObjInTank(self, newComponent):
        if isinstance(newComponent, Component):
            self.tank.addChild(newComponent)
            self.components.append(newComponent)
        if isinstance(newComponent, EnvironmentObject):
            if newComponent.species_id >= 0:
                self.creatures.append(newComponent)
            # add environment components list reference to this new object's
            newComponent.env_obj_list = self.components

"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""
import random


from Component import Component
from Point import Point
import ColorType as Ct
from Displayable import Displayable
from Animation import Animation
from EnvironmentObject import EnvironmentObject
from Vivarium import Tank
from DisplayableSphere import DisplayableSphere
from DisplayableHalfRoundCylinder import DisplayableHalfRoundCylinder
from DisplayableCylinder import DisplayableCylinder
from DisplayableRoundCylinder import DisplayableRoundCylinder

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, linkageLength=0.5, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        link1 = Component(Point((0, 0, 0)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link1.setDefaultColor(Ct.DARKORANGE1)
        link2 = Component(Point((0, 0, linkageLength)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link2.setDefaultColor(Ct.DARKORANGE2)
        link3 = Component(Point((0, 0, linkageLength)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link3.setDefaultColor(Ct.DARKORANGE3)
        link4 = Component(Point((0, 0, linkageLength)),
                          DisplayableCube(self.contextParent, 1, [linkageLength / 4, linkageLength / 4, linkageLength]))
        link4.setDefaultColor(Ct.DARKORANGE4)

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)

        self.components = [link1, link2, link3, link4]

class BodyLinkage(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, LinkageLength = 0.1, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        topBody = Component(Point((0, 0, 0)), DisplayableHalfRoundCylinder(self.contextParent, 1*LinkageLength, 0.5*LinkageLength))
        topBody.setDefaultColor(Ct.DARKORANGE2)
        topBody.vRange = [-90, 90]

        head = Component(Point((0, 1*LinkageLength, 0.6*LinkageLength)), DisplayableSphere(self.contextParent, 0.8*LinkageLength))
        head.setDefaultColor(Ct.DARKORANGE1)
        head.uRange = [-65, 45]
        head.vRange = [-73, 73]
        head.wRange = [-20, 20]

        botBody = Component(Point((0, 0, 0)), DisplayableCylinder(self.contextParent, 1*LinkageLength, 1*LinkageLength))
        botBody.setDefaultColor(Ct.DARKORANGE3)


        leftEye = Component(Point((-0.35*LinkageLength, 0.2*LinkageLength, 0.66*LinkageLength)), DisplayableSphere(self.contextParent, 0.1*LinkageLength))
        leftEye.setDefaultColor(Ct.RED)
        leftEye.uRange = [-45, 45]
        leftEye.vRange = [-45, 45]

        rightEye = Component(Point((0.35*LinkageLength, 0.2*LinkageLength, 0.66*LinkageLength)), DisplayableSphere(self.contextParent, 0.1*LinkageLength))
        rightEye.setDefaultColor(Ct.RED)
        rightEye.uRange = [-45, 45]
        rightEye.vRange = [-45, 45]

        self.addChild(topBody)
        self.addChild(botBody)
        topBody.addChild(head)
        head.addChild(leftEye)
        head.addChild(rightEye)

        self.components = [topBody, head]


class ArmLinkage(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, LinkageLength = 0.1, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent
        self.chained_rotate = 1

        humeri = Component(Point((0, 0, 0)), DisplayableCylinder(self.contextParent, 0.1*LinkageLength, 0.5*LinkageLength))
        humeri.setDefaultColor(Ct.DARKORANGE1)
        humeri.setDefaultAngle(humeri.wAxis, 90)
        humeri.uRange = [-225, 45]
        humeri.wRange = [90, 90]

        shoulder = Component(Point((0, 0, -0.25*LinkageLength)), DisplayableCube(self.contextParent, 1, [0.4*LinkageLength, 0.25*LinkageLength, 0.8*LinkageLength]))
        shoulder.setDefaultColor(Ct.DARKORANGE2)
        shoulder.uRange = [-20, 5]
        # Since the children of shoulder does not contain any joint,
        # we chain shoulder and its children so they can be colored together when selected.
        shoulder.chained_child = 1

        upperArm = Component(Point((0, 0, 0.8*LinkageLength)), DisplayableHalfRoundCylinder(self.contextParent, 0.1*LinkageLength, 0.4*LinkageLength))
        upperArm.setDefaultColor(Ct.DARKORANGE1)
        upperArm.setDefaultAngle(upperArm.uAxis, 90)

        foreArm = Component(Point((0, 0.4*LinkageLength, 0)), DisplayableRoundCylinder(self.contextParent, 0.1*LinkageLength, 0.3*LinkageLength))
        foreArm.setDefaultColor(Ct.DARKORANGE1)
        foreArm.uRange = [0, 20]
        foreArm.vRange = [-45, 45]
        foreArm.wRange = [-110, 0]

        hand = Component(Point((0, 0.3*LinkageLength, 0)), DisplayableCube(self.contextParent, 1, [0.4*LinkageLength, 0.25*LinkageLength, 0.8*LinkageLength]))
        hand.setDefaultAngle(hand.uAxis, -90)
        hand.setDefaultColor(Ct.DARKORANGE2)
        hand.uRange = [-120, -60]
        hand.vRange = [-20, 20]
        hand.wRange = [-90, 90]

        self.setDefaultAngle(self.uAxis, 90)

        self.addChild(humeri)
        humeri.addChild(shoulder)
        shoulder.addChild(upperArm)
        upperArm.addChild(foreArm)
        foreArm.addChild(hand)

        self.components = [humeri, shoulder, foreArm, hand]


class LegLinkage(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, LinkageLength = 0.1, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent
        self.chained_rotate = 1

        thigh = Component(Point((0, 0, 0)), DisplayableCylinder(self.contextParent, 0.2*LinkageLength, 0.2*LinkageLength))
        thigh.setDefaultColor(Ct.DARKORANGE1)
        thigh.setDefaultAngle(thigh.wAxis, 90)
        thigh.uRange = [-30, 30]
        thigh.wRange = [90, 90]
        # Since the children of thigh does not contain any joint,
        # we chain thigh and its children so they can be colored together when selected.
        thigh.chained_child = 1

        leg = Component(Point((0, -0.1*LinkageLength, -0.5*LinkageLength)), DisplayableCube(self.contextParent, 1, [0.4*LinkageLength, 0.2*LinkageLength, 0.5*LinkageLength]))
        leg.setDefaultColor(Ct.DARKORANGE1)
        # Since the children of leg does not contain any joint,
        # we chain leg and its children so they can be colored together when selected.
        leg.chained_child = 1

        foot = Component(Point((0, 0, -0.1*LinkageLength)), DisplayableCube(self.contextParent, 1, [1.6*LinkageLength, 0.7*LinkageLength, 0.1*LinkageLength]))
        foot.setDefaultColor(Ct.DARKORANGE2)

        self.setDefaultAngle(self.uAxis, -90)

        self.addChild(thigh)
        thigh.addChild(leg)
        leg.addChild(foot)

        self.components = [thigh]


class DisplayableCube(Displayable):
    """
    Create a enclosed cylinder whose one end is at z=0 and it grows along z coordinates
    """

    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    scale = None
    edgeLength = 1
    _bufferData = None

    def __init__(self, parent, edgeLength, scale=None):
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.edgeLength = edgeLength
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale

    def draw(self):
        gl.glCallList(self.callListHandle)

    def initialize(self):
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()

        v_l = [
            [-self.edgeLength / 2, -self.edgeLength / 2, -self.edgeLength / 2],
            [self.edgeLength / 2, -self.edgeLength / 2, -self.edgeLength / 2],
            [self.edgeLength / 2, self.edgeLength / 2, -self.edgeLength / 2],
            [- self.edgeLength / 2, self.edgeLength / 2, -self.edgeLength / 2],
            [- self.edgeLength / 2, -self.edgeLength / 2, self.edgeLength / 2],
            [self.edgeLength / 2, -self.edgeLength / 2, self.edgeLength / 2],
            [self.edgeLength / 2, self.edgeLength / 2, self.edgeLength / 2],
            [- self.edgeLength / 2, self.edgeLength / 2, self.edgeLength / 2],
        ]

        gl.glNewList(self.callListHandle, gl.GL_COMPILE)
        gl.glPushMatrix()

        gl.glScale(*self.scale)
        gl.glTranslate(0, 0, self.edgeLength / 2)

        # a primitive cube
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex3f(*v_l[1])
        gl.glVertex3f(*v_l[0])
        gl.glVertex3f(*v_l[3])
        gl.glVertex3f(*v_l[2])

        gl.glVertex3f(*v_l[4])
        gl.glVertex3f(*v_l[5])
        gl.glVertex3f(*v_l[6])
        gl.glVertex3f(*v_l[7])

        gl.glVertex3f(*v_l[0])
        gl.glVertex3f(*v_l[4])
        gl.glVertex3f(*v_l[7])
        gl.glVertex3f(*v_l[3])

        gl.glVertex3f(*v_l[7])
        gl.glVertex3f(*v_l[6])
        gl.glVertex3f(*v_l[2])
        gl.glVertex3f(*v_l[3])

        gl.glVertex3f(*v_l[5])
        gl.glVertex3f(*v_l[1])
        gl.glVertex3f(*v_l[2])
        gl.glVertex3f(*v_l[6])

        gl.glVertex3f(*v_l[0])
        gl.glVertex3f(*v_l[1])
        gl.glVertex3f(*v_l[5])
        gl.glVertex3f(*v_l[4])

        gl.glEnd()

        gl.glPopMatrix()
        gl.glEndList()


##### TODO 1: Construct your two different creatures
# Requirements:
#   1. For the basic parts of your creatures, feel free to use routines provided with the previous assignment.
#   You are also free to create your own basic parts, but they must be polyhedral (solid).
#   2. The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae,
#   fins, tentacles, etc.
#   3. Model requirements:
#         1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
#         2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at
#         least one moving part.
#         3. The predator and prey should have distinguishable different colors.
#         4. You are welcome to reuse your PA2 creature in this assignment.


class Predator(Component, Animation, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None
    rotation_speed = None
    translation_speed = None
    up_vector = Point((0, 1, 0))
    local_n_vector = None
    local_v_vector = None
    local_u_vector = None

    def __init__(self, parent, position):
        super(Predator, self).__init__(position)
        arm1 = ModelLinkage(parent, Point((0, 0, 0)), 0.1)
        arm2 = ModelLinkage(parent, Point((0, 0, 0)), 0.1)
        arm2.setDefaultAngle(arm2.vAxis, 120)
        arm3 = ModelLinkage(parent, Point((0, 0, 0)), 0.1)
        arm3.setDefaultAngle(arm3.vAxis, 240)

        self.components = arm1.components + arm2.components + arm3.components
        self.addChild(arm1)
        self.addChild(arm2)
        self.addChild(arm3)

        self.rotation_speed = []
        for comp in self.components:
            comp.setRotateExtent(comp.uAxis, 0, 35)
            comp.setRotateExtent(comp.vAxis, -45, 45)
            comp.setRotateExtent(comp.wAxis, -45, 45)
            self.rotation_speed.append([1, 0, 0])

        self.translation_speed = Point([0,0,0])
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.1 * 4
        self.species_id = 1

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create period animation for creature joints
        for i, comp in enumerate(self.components):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            comp.rotate(self.rotation_speed[i][1], comp.vAxis)
            comp.rotate(self.rotation_speed[i][2], comp.wAxis)
            if comp.uAngle in comp.uRange:  # rotation reached the limit
                self.rotation_speed[i][0] *= -1
            if comp.vAngle in comp.vRange:
                self.rotation_speed[i][1] *= -1
            if comp.wAngle in comp.wRange:
                self.rotation_speed[i][2] *= -1
        #self.vAngle = (self.vAngle + 5) % 360

        for item in self.env_obj_list:
            if isinstance(item, Tank):
                if not (item.tank_dimensions[0] / 2 - self.bound_radius) > (
                        self.current_position[0] + self.translation_speed[0]) > (
                               -item.tank_dimensions[0] / 2 + self.bound_radius):
                    self.translation_speed.coords[0] *= -1
                if not (item.tank_dimensions[1] / 2 - self.bound_radius > self.current_position[1] +
                        self.translation_speed[1] > -item.tank_dimensions[1] / 2 + self.bound_radius):
                    self.translation_speed.coords[1] *= -1
                if not (item.tank_dimensions[2] / 2 - self.bound_radius > self.current_position[2] +
                        self.translation_speed[2] > -item.tank_dimensions[2] / 2 + self.bound_radius):
                    self.translation_speed.coords[2] *= -1

            elif isinstance(item, EnvironmentObject):
                # If item is a predator.
                if item.species_id == 2:
                    print((item.bound_center - self.bound_center).norm(), (item.bound_radius + self.bound_radius))
                    if (item.bound_center - self.bound_center).norm() <= (item.bound_radius + self.bound_radius):
                        self.translation_speed.reflect(item.bound_center - self.bound_center)
                # If item is a prey.
                elif item.species_id == 1:
                    self.translation_speed += (item.current_position - self.current_position)
                    print((item.bound_center - self.bound_center).norm(), (item.bound_radius + self.bound_radius))
                    if (item.bound_center - self.bound_center).norm() <= (item.bound_radius + self.bound_radius):
                        print("here")

        self.translation_speed = self.translation_speed.normalize()*0.01

        self.local_n_vector = self.translation_speed.normalize()
        self.local_v_vector = self.local_n_vector.cross3d(self.up_vector).normalize()
        self.local_u_vector = self.local_n_vector.cross3d(self.local_v_vector).normalize()

        self.pre_rotation_matrix = [
            [self.local_n_vector.coords[0], self.local_n_vector.coords[1], self.local_n_vector[2], 0],
            [self.local_v_vector.coords[0], self.local_v_vector.coords[1], self.local_v_vector[2], 0],
            [self.local_u_vector.coords[0], self.local_u_vector.coords[1], self.local_u_vector[2], 0],
            [0, 0, 0, 1]
        ]

        self.current_position = self.current_position + self.translation_speed
        self.update()


class Prey(Component, Animation, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None
    rotation_speed = None
    translation_speed = None
    up_vector = Point((0, 1, 0))
    local_n_vector = None
    local_v_vector = None
    local_u_vector = None

    def __init__(self, parent, position):
        super(Prey, self).__init__(position)
        body = BodyLinkage(parent, Point((0, 0, 0)))
        body.setDefaultAngle(body.vAxis, 90)

        rightArm = ArmLinkage(parent, Point((-0.13, 0.05, -0.005)))
        leftArm = ArmLinkage(parent, Point((0.13, 0.05, -0.005)))
        for i in range(4):
            # Mirror two arms by flipping the wAxis direction of five joints.
            leftArm.components[i].wAxis = [0, 0, -1]

        rightLeg = LegLinkage(parent, Point((-0.05, -0.1, 0)))
        leftLeg = LegLinkage(parent, Point((0.03, -0.1, 0)))
        body.components[0].addChild(rightArm)
        body.components[0].addChild(leftArm)
        body.addChild(rightLeg)
        body.addChild(leftLeg)

        self.components = body.components + rightArm.components + leftArm.components + leftLeg.components + rightLeg.components
        self.addChild(body)
        self.rotation_speed = []
        # for comp in self.components:
        #     comp.setRotateExtent(comp.uAxis, 0, 35)
        #     comp.setRotateExtent(comp.vAxis, -45, 45)
        #     comp.setRotateExtent(comp.wAxis, -45, 45)
        #     self.rotation_speed.append([1, 0, 0])

        self.translation_speed = Point([random.random() - 0.5 for _ in range(3)]).normalize() * 0.01

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.1 * 4
        self.species_id = 1

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create period animation for creature joints

        for item in self.env_obj_list:
            if isinstance(item, Tank):
                if not (item.tank_dimensions[0] / 2 - self.bound_radius) > (
                        self.current_position[0] + self.translation_speed[0]) > (
                               -item.tank_dimensions[0] / 2 + self.bound_radius):
                    self.translation_speed.coords[0] *= -1
                if not (item.tank_dimensions[1] / 2 - self.bound_radius > self.current_position[1] +
                        self.translation_speed[1] > -item.tank_dimensions[1] / 2 + self.bound_radius):
                    self.translation_speed.coords[1] *= -1
                if not (item.tank_dimensions[2] / 2 - self.bound_radius > self.current_position[2] +
                        self.translation_speed[2] > -item.tank_dimensions[2] / 2 + self.bound_radius):
                    self.translation_speed.coords[2] *= -1

        self.local_n_vector = self.translation_speed.normalize()
        self.local_v_vector = self.local_n_vector.cross3d(self.up_vector).normalize()
        self.local_u_vector = self.local_n_vector.cross3d(self.local_v_vector).normalize()

        self.pre_rotation_matrix = [
            [self.local_n_vector.coords[0], self.local_n_vector.coords[1], self.local_n_vector[2], 0],
            [self.local_v_vector.coords[0], self.local_v_vector.coords[1], self.local_v_vector[2], 0],
            [self.local_u_vector.coords[0], self.local_u_vector.coords[1], self.local_u_vector[2], 0],
            [0, 0, 0, 1]
        ]

        self.current_position = self.current_position + self.translation_speed
        print(self.current_position)
        self.update()

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between it and tank walls. When it hits with tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.

        ##### TODO 4: Eyes on the road!
        # Requirements:
        #   1. CCreatures should face in the direction they are moving. For instance, a fish should be facing the
        #   direction in which it swims. Remember that we require your creatures to be movable in 3 dimensions,
        #   so they should be able to face any direction in 3D space.

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

import math
import numpy as np
from numpy.linalg import norm

mass_sun = 1.989 * 10 ** 30
G = 6.674e-11


class Planet(object):
    def __init__(self, name, color, mass, pos):
        self.name = name
        self.color = color
        self.mass = mass
        self.pos = np.array(pos)
        radius = norm(pos)

        if radius > 0:
            self.vel = (np.sqrt(G * mass_sun / radius) *
                        np.array([-pos[1] / radius, pos[0] / radius]))
        else:
            self.vel = np.zeros(2)

        # All the planets have to be initialised in order to calculate
        # accelerations, therefore they will be initialized as None and
        # calculated later.
        self.acc = None
        # The old acceleration is needed because it will have to be used
        # in the algorithm to obtain the new positions and velocities.
        self.old_acc = self.acc

    def update_acc(self, planets, first=False):
        """Calculating the acceleration due to the other planets.
        """
        acc = np.zeros(2)
        for planet in planets:
            if planet is not self:
                dist = self.pos - planet.pos  # Distance between planets
                # Using Newton's gravitational formula.
                acc = acc + (-G * planet.mass * dist) / math.pow(norm(dist), 3)
        if first:
            self.acc = acc
            self.old_acc = acc
        return acc

    def update_pos(self, t):
        """Obtaining the new position using the Beeman's algorithm.
        """
        self.pos = (self.pos + self.vel * t + (math.pow(t, 2) / 6.0) *
                    (4.0 * self.acc - self.old_acc))

    def update_vel(self, t, new_acc):
        """Obtaining the new velocity using the Beeman's algorithm.
        """
        self.vel = (self.vel + ((t / 6.0) *
                    (2.0 * new_acc + 5.0 * self.acc - self.old_acc)))

    def update_vel_acc(self, t, planets):
        new_acc = self.update_acc(planets)
        self.update_vel(t, new_acc)
        self.old_acc = self.acc
        self.acc = new_acc

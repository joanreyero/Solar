import math
import numpy as np
from numpy.linalg import norm

mass_sun = 1.989 * 10 ** 30
G = 6.674e-11


class Satelite(object):
    def __init__(self, origin, target, color, size, mass, given_speed, angle,
                 radius_planet, planets):
        self.color = color
        self.size = size
        self.mass = mass
        self.time = 0
        self.vel = (origin.vel + given_speed *
                     np.array([np.cos(angle), np.sin(angle)]))

        self.pos = np.array([origin.pos[0] + radius_planet * np.cos(angle),
                             origin.pos[1] + radius_planet * np.sin(angle)])

        self.acc = self.update_acc(planets)
        self.origin = origin
        self.target = target
        self.min_dist = None


        self.old_acc = self.acc

    def update_acc(self, planets):
        """Calculating the acceleration due to the other planets.
        """
        acc = np.zeros(2)
        for planet in planets:
            if planet is not self:
                dist = self.pos - planet.pos  # Distance between planets
                # Using Newton's gravitational formula.
                acc = acc + (-G * planet.mass * dist) / math.pow(norm(dist), 3)
        return acc

    def update_pos(self, t):
        """Obtaining the new position using the Beeman's algorithm.
        """
        #xprint self.pos
        self.pos = (self.pos + self.vel * t + (math.pow(t, 2) / 6.0) *
                        (4.0 * self.acc - self.old_acc))

    def get_distance_target(self):
        return norm(self.pos-self.target.pos)

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

import math
import numpy as np
from numpy.linalg import norm

mass_sun = 1.989 * 10 ** 30
G = 6.675e-11


class Planet(object):
    def __init__(self, mass, radius, angle, time_interval):
        self.mass = mass
        # Creates a vector position from polar form
        self.pos = radius * np.array([np.cos(angle), np.sin(angle)])

        # Creates a vector velocity perpendicular to position
        # using v = sqrt(GM/r)
        self.vel = (np.sqrt(G * mass_sun / radius) *
                    np.array([-np.sin(angle), np.cos(angle)]))
        print self.vel

        # All the planets have to be initialised in order to calculate
        # accelerations, therefore they will be initialized as None and
        # calculated later in the function move()
        self.acc = None
        # The old acceleration is needed because it will have to be used
        # in the algorithm to obtain the new positions and velocities.
        self.old_acc = 0

        # A small time interval for numerical integration
        self.t = time_interval

    def acc_sun(self):
        """Calculating the acceleration due to the Sun.
        """
        return (-G * mass_sun * self.pos / (norm(self.pos))**3)

    def update_acc(self, planets):
        """Calculating the acceleration due to the other planets.
        """
        acc = self.acc_sun()
        for planet in planets:
            if planet is not self:
                dist = self.pos - planet.pos  # Distance between planets
                # Using Newton's gravitational formula.
                acc += (-G * planet.mass * dist / norm(dist)**3)
        self.acc = acc
        return acc

    def update_pos(self):
        """Obtaining the new position using the Beeman's algorithm.
        """
        self.pos += (self.vel * self.t + (math.pow(self.t, 2) / 6.0) *
                     (4.0 * self.acc - self.old_acc))

    def update_vel(self, new_acc):
        """Obtaining the new velocity using the Beeman's algorithm.
        """
        self.vel += ((self.t / 6.0) * (2.0 * new_acc +
                                     5.0 * self.acc - self.old_acc))

    def update_vel_acc(self, planets):
        new_acc = self.update_acc(planets)
        print self.pos
        print self.vel
        print self.acc
        print '\n'
        self.update_vel(new_acc)
        #print self.vel
        self.old_acc, self.acc = self.acc, new_acc

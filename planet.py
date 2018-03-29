import math
import numpy as np
from numpy.linalg import norm

mass_sun = 1.989 * 10 ** 30
G = 6.674e-11


class Planet(object):
    def __init__(self, mass, pos, initial_velocity, color, time_interval):
        self.mass = mass
        self.color = color
        self.pos = np.array(pos)
        radius = norm(pos)

        # Creates a vector velocity perpendicular to position
        # using v = sqrt(GM/r) if the initial velocity was not
        # specified.
        if not initial_velocity:
            radius = norm(pos)
            self.vel = (np.sqrt(G * mass_sun / radius) *
                        np.array([-pos[1] / radius, pos[0] / radius]))
        else:
            vel, angle = initial_velocity[0], initial_velocity[1]
            self.vel = (vel * np.array([np.cos(angle), np.sin(angle)]))
        #print self.vel

        # All the planets have to be initialised in order to calculate
        # accelerations, therefore they will be initialized as None and
        # calculated later.
        self.acc = None
        # The old acceleration is needed because it will have to be used
        # in the algorithm to obtain the new positions and velocities.
        self.old_acc = self.acc

        # A small time interval for numerical integration
        self.t = time_interval

    def update_acc(self, planets, first=False):
        """Calculating the acceleration due to the other planets.
        """
        acc = np.array([0.0, 0.0])
        for planet in planets:
            if planet is not self:
                dist = self.pos - planet.pos  # Distance between planets
                # Using Newton's gravitational formula.
                acc = acc + (-G * planet.mass * dist) / (norm(dist)**3)
        if first:
            self.old_acc = acc
        self.acc = acc
        return acc

    def update_pos(self):
        """Obtaining the new position using the Beeman's algorithm.
        """
        self.pos = (self.pos + self.vel * self.t + (math.pow(self.t, 2) / 6.0) *
                    (4.0 * self.acc - self.old_acc))

    def update_vel(self, new_acc):
        """Obtaining the new velocity using the Beeman's algorithm.
        """
        self.vel = (self.vel + (self.t / 6.0) *
                    (2.0 * new_acc + 5.0 * self.acc - self.old_acc))

    def update_vel_acc(self, planets):
        new_acc = self.update_acc(planets)
        print self.pos
        #print self.vel
        #print self.acc
        #print '\n'
        self.update_vel(new_acc)
        #print self.vel
        self.old_acc, self.acc = self.acc, new_acc

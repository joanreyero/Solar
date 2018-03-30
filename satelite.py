import math
import numpy as np
from numpy.linalg import norm

mass_sun = 1.989 * 10 ** 30
G = 6.674e-11


class Satelite(object):
    def __init__(self, color, mass, given_speed, engine_time, angle,
                 pos, mass_planet, vel_planet, radius_planet,
                 planets):
        self.color = color
        self.mass = mass
        self.engine_time = engine_time
        self.time = 0

        self.vel = (vel_planet + given_speed *
                     np.array([np.cos(angle), np.sin(angle)]))

        print angle
        self.pos = np.array([pos[0] + radius_planet * np.cos(angle),
                             pos[1] + radius_planet * np.sin(angle)])

        print "position " + str(self.pos)
        print "velocity " + str(self.vel)

        self.acc = self.update_acc(planets)

        print "acceleration " + str(self.acc)
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
        #print acc
        return acc

    def update_pos(self, t):
        """Obtaining the new position using the Beeman's algorithm.
        """
        if self.time < self.engine_time:
            self.pos += t * self.vel
        else:
            self.pos = (self.pos + self.vel * t + (math.pow(t, 2) / 6.0) *
                        (4.0 * self.acc - self.old_acc))

    def update_vel(self, t, new_acc):
        """Obtaining the new velocity using the Beeman's algorithm.
        """
        self.vel = (self.vel + ((t / 6.0) *
                                (2.0 * new_acc + 5.0 * self.acc - self.old_acc)))

    def update_vel_acc(self, t, planets):
        new_acc = self.update_acc(planets)
        if self.time >= self.engine_time:
            self.update_vel(t, new_acc)
        print self.vel
        print self.acc
        print '\n'
        self.old_acc = self.acc
        self.acc = new_acc
        self.time += t

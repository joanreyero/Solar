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

        # The velocity of the planet of origin plus the given velocity
        # at the given angle.
        self.vel = (origin.vel + given_speed *
                     np.array([np.cos(angle), np.sin(angle)]))

        # The position of the planet of origin plus the vector in the direction
        # of the given angle and length radius.
        self.pos = np.array([origin.pos[0] + radius_planet * np.cos(angle),
                             origin.pos[1] + radius_planet * np.sin(angle)])

        self.acc = self.update_acc(planets)
        self.origin = origin
        self.target = target

        self.min_distance = None
        self.old_acc = self.acc

    def update_pos(self, t):
        """Obtaining the new position using the Beeman's algorithm.
        Args:
            param1 (float): a small time step.
        """
        self.pos = (self.pos + self.vel * t + (math.pow(t, 2) / 6.0) *
                        (4.0 * self.acc - self.old_acc))

    def update_minimal_distance(self):
        """Updates the minimal distance to the target if the Satelite has moved
        any closer. Writes the minimal distance in a text file named
        'minimum-distance.txt.'
        """
        dist = norm(self.pos-self.target.pos) # Distance to the target

        if self.min_distance:  # If it's not the first iteration
            if self.min_distance > dist:
                # Update and overwrite
                self.min_distance = dist
                wr = open('minimum-distance.txt', 'w')
                wr.write("Minimal distance to " + self.target.name + ": " +
                         str(round(self.min_distance / 1000, 2)) +" km.")

        else:
            self.min_distance = dist

    def update_vel(self, t, new_acc):
        """Obtaining the new velocity using the Beeman's algorithm.
        Args:
            param1 (float): a small time step needed for numerical integration.
            param2 (float): the acceleration at the next time step.
        """
        self.vel = (self.vel + ((t / 6.0) *
                                (2.0 * new_acc + 5.0 * self.acc - self.old_acc)))

    def update_acc(self, planets):
        """Calculating the acceleration due to the planets.
        The sum of all the Gm/r, where m is the mass of the planet and r
        is the radius separating them.
        Args:
            param1 (list): a list of all the planets.
        """
        acc = np.zeros(2)
        for planet in planets:
            if planet is not self:
                dist = self.pos - planet.pos  # Distance between planets
                # Using Newton's gravitational formula.
                acc = acc + (-G * planet.mass * dist) / math.pow(norm(dist), 3)
        return acc

    def update_vel_acc(self, t, planets):
        """Updates the velocity and the acceleration of the satelite.
        Args:
            param1 (float): a small time step needed for numerical integration.
            param2 (list): a list of all the planets.
        """
        # First calculate the new acceleration.
        new_acc = self.update_acc(planets)
        # Calculate the velocity with it
        self.update_vel(t, new_acc)
        # Lastly, update the accelerations.
        self.old_acc, self.acc = self.acc, new_acc

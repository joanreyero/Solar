import math
import numpy as np
from numpy.linalg import norm

mass_sun = 1.989 * 10 ** 30
G = 6.674e-11


class Planet(object):
    def __init__(self, name, color, size, mass, pos, radius_planet,
                 vel=None, angle=None):
        self.name = name
        self.color = color
        self.size = size
        self.laps = (0, 0)
        self.mass = mass
        self.pos = np.array(pos)
        radius = norm(pos)

        if vel is None:  # If it is a planet and has no given initial velocity.
            if radius > 0:  # If its not the Sun
                # Calculate the velocity using the square root of G times the
                # mass of the Sun over the distance to it.
                self.vel = (np.sqrt(G * mass_sun / radius) *
                            np.array([-pos[1] / radius, pos[0] / radius]))
            else:
                self.vel = np.zeros(2)  # Set Sun's initial velocity to zero.
        else:
            # If it's an asteroid set the initial velocity to the given speed
            # at the given angle.
            self.vel = vel * np.array([np.cos(angle), np.sin(angle)])

        # All the planets have to be initialised in order to calculate
        # accelerations, therefore they will be initialized as None and
        # calculated later.
        self.acc = None
        # The old acceleration is needed because it will have to be used
        # in the algorithm to obtain the new positions and velocities.
        self.old_acc = self.acc

    def update_pos_laps(self, t, time):
        """Obtaining the new position using the Beeman's algorithm.
        If an orbit is completed, increase the number of laps by one and save
        the time.
        Args:
            param1 (float): a small time step.
            param2 (float): the current time since the start of the simulation.
        """
        new_pos = (self.pos + self.vel * t + (math.pow(t, 2) / 6.0) *
                   (4.0 * self.acc - self.old_acc))

        # If the planet is going from 4th to 1st quadrant
        if self.pos[1] < 0 and new_pos[1] >= 0:
            self.laps = (self.laps[0]+1, time)  # Increase laps by one

        self.pos = new_pos  # Update the position

    def update_vel(self, t, new_acc):
        """Obtaining the new velocity using the Beeman's algorithm.
        Args:
            param1 (float): a small time step needed for numerical integration.
            param2 (float): the acceleration at the next time step.
        """
        self.vel = (self.vel + ((t / 6.0) *
                    (2.0 * new_acc + 5.0 * self.acc - self.old_acc)))

    def update_acc(self, planets, first=False):
        """Calculating the acceleration due to the other planets.
        The sum of all the Gm/r, where m is the mass of the other planet and r
        is the radius separating them.
        Args:
            param1 (list): a list of all the planets.
            param2 (bool) (opt): whether it is the first iteration or not
        """
        acc = np.zeros(2)
        for planet in planets:
            if planet is not self:
                dist = self.pos - planet.pos  # Distance between planets
                # Using Newton's gravitational formula.
                acc = acc + (-G * planet.mass * dist) / math.pow(norm(dist), 3)

        if first:  # If it is the first iteration
            self.acc = acc
            # Set the previous acceleration equal to the current acceleration
            self.old_acc = acc
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

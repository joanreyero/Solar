import numpy as np
from numpy.linalg import norm

mass_sun = 1.989 * 10 ** 30
G = 6.675E(-11)


class Planet(object):
    def __init__(self, mass, radius, angle, time_interval):
        self.mass = mass
        # Creates a vector position from polar form
        self.pos = radius * np.array([np.cos(angle), np.sin(angle)])

        # Creates a vector velocity perpendicular to position
        # using v = sqrt(GM/r)
        self.vel = (np.sqrt(G * mass_sun / radius) *
                    np.array([-np.sin(angle), np.cos(angle)]))

        # All the planets have to be initialised in order to calculate
        # accelerations, therefore they will be initialized as None and
        # calculated later in the function move()
        self.acceleration = None
        # The old acceleration is needed because it will have to be used
        # in the algorithm to obtain the new positions and velocities.
        self.old_acceleration = 0

        # A small time interval for numerical integration
        self.t = time_interval

    def acceleration_sun(self):
        """Calculating the acceleration due to the Sun.
        """
        return (-1 * (G * mass_sun / (norm(self.pos))**2) *
                (self.pos / norm(self.pos)))

    def get_acceleration(self, planets):
        """Calculating the acceleration due to the other planets.
        """
        a = self.acceleration_sun()
        for planet in planets:
            dist = self.pos - planet.pos  # Distance between planets
            # Using Newton's gravitational formula.
            a += -1 * (G * planet.mass / norm(dist)**2) * (dist / norm(dist))
        return a

    def position(self):
        """Obtaining the new position using the Beeman's algorithm.
        """
        self.pos += (self.vel * self.t + self.t ** 2.0 / 6.0 *
                     (4.0 * self.acceleration - self.old_acceleration))

    def velocity(self, new_acceleration):
        """Obtaining the new velocity using the Beeman's algorithm.
        """
        self.vel += (self.t / 6.0 * (2.0 * new_acceleration +
                              5.0 * self.acceleration - self.old_acceleration))

#    def mmove(self, all_planets):
#        """Moving the planet updating the position, velocity and acceleration.
#        """
#        # If it's the first time called, calculate the initial acceleration and
#        # initialize the instance variable.
#
#        # Removing self from planets
#        planets = [planet for planet in all_planets if planet != self]
#
#        if not self.acceleration:
#            self.acceleration = self.get_acceleration(planets)
#            self.old_acceleration = self.acceleration
#
#        self.position()  # Calculate and update the new position
#        # Calculate the acceleration in the next step, needed for the new velocity.
#        new_acceleration = self.get_acceleration(planets)
#        self.velocity(new_acceleration)  # Calculate the new velocity
#        # Update the accelerations.
#        self.old_acceleration = self.acceleration
#        self.acceleration = new_acceleration

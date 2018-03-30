import json
import math
import numpy as np
from planet import Planet
from satelite import Satelite
from numpy.linalg import norm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Solar(object):

    def __init__(self, data_name, time_step, satelite=False):
        with open(data_name + '.json') as json_data:
            data = json.load(json_data)

        self.planets = [Planet(*[planet] + data[planet][0:4])
                        for planet in data]

        for planet in self.planets:
            planet.update_acc(self.planets, first=True)

        if satelite:
            self.distances = []
            with open(satelite + '.json') as json_data:
                sat_data = json.load(json_data)['Satelite']

            for p in self.planets:
                if p.name == sat_data[0]:
                    origin = p
                if p.name == sat_data[1]:
                    target = p

            self.planets.append(Satelite(*[origin, target] + sat_data[2:] +
                                         [data[planet.name][4], self.planets]))
        self.t = time_step


    def init(self):
       return self.patches

    def animate(self, i):
        self.move()
        for n, planet in enumerate(self.planets):
            self.patches[n].center = (planet.pos[0], planet.pos[1])
        return self.patches

    def get_time_step(self):
        for body in self.planets:
            if type(body).__name__ == "Satelite":
                sat = body
        t = 0.01*norm(sat.vel)/norm(sat.acc)
        if t > 20000:
            return 20000
        return t

    def move(self):
        t = self.get_time_step()
        for planet in self.planets:
            if type(planet).__name__ == "Satelite":
                planet.update_pos(t




                )
                self.distances.append(planet.get_distance_target())
            else:
                planet.update_pos(t)
        for planet in self.planets:
            planet.update_vel_acc(t, self.planets)

    def run(self):
        fig = plt.figure()
        ax = plt.axes()
        axes = 3E11
        self.patches = [plt.Circle((planet.pos[0], planet.pos[1]),
                                   planet.size, color = planet.color)
                        for planet in self.planets]
        for patch in self.patches:
            ax.add_patch(patch)
        ax.set_axis_bgcolor('black')
        ax.axis('scaled')
        ax.set_xlim(-axes, axes)
        ax.set_ylim(-axes, axes)

        anim = FuncAnimation(fig, self.animate, init_func = self.init, interval = 1)
        plt.show()
        try:
            return ("""Simulation complete. Minimal distance to target was """
                    + str(min(self.distances)))
        except:
            return 'Simulation complete'


solar = Solar('solar-system-data', 20000, satelite='earth-satelite-data')
print solar.run()

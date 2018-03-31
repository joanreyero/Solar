import json
import math
import numpy as np
import itertools as it
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
        self.energies = ([], [])
        self.t = time_step
        self.time = 0

    def init(self):
       return self.patches

    def animate(self, i):
        self.move()
        for n, planet in enumerate(self.planets):
            self.patches[n].center = (planet.pos[0], planet.pos[1])
        return self.patches

    def get_energies(self):
        energy = sum([planet.get_energy(self.planets) for planet in self.planets
                      if planet.name is not 'Sun'])
        self.energies[0].append(self.time)
        self.energies[1].append(energy)

        if self.time == 0:
            mode = "w"
        else:
            mode = "a"

        text = ("Time: " + str(self.time) + "s. Energy: "
                + str(round(energy, 2)) + "J.\n")
        energies_file = open("energies.txt", mode)
        energies_file.write(text)

    def plot_energies(self):
        plt.plot(self.energies[0], self.energies[1])
        plt.xlabel('Time (s)')
        plt.ylabel('Energy (J)')
        plt.show()


    def get_time_step(self):
        for body in self.planets:
            if type(body).__name__ == "Satelite":
                sat = body
                t = 0.01*norm(sat.vel)/norm(sat.acc)
                if t < self.t:
                    return t
        return self.t

    def move(self):
        t = self.get_time_step()
        for planet in self.planets:
            if type(planet).__name__ == "Satelite":
                planet.update_pos(t)
                self.distances.append(planet.get_distance_target())
            else:
                planet.update_pos_laps(t, self.time)
        for planet in self.planets:
            planet.update_vel_acc(t, self.planets)

        self.get_energies()
        self.time += t

    def get_obital_periods(self):
        text = ""
        for planet in self.planets:
            if type(planet).__name__ == "Planet" and planet.name is not 'Sun':
                try:
                    mean_time = planet.laps[1] / planet.laps[0]
                    period = round(mean_time / (3600 * 24), 2)
                    fraction = round(period / 365, 2)
                    text += (planet.name + ": " + str(period) + " days (" +
                             str(fraction) + " times the real Earth's period.\n")
                except: pass
        wr = open('orbital-periods.txt', 'w')
        wr.write(text)

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

        self.get_obital_periods()
        self.plot_energies()

        try:
            return ("""Simulation complete. Minimal distance to target was """
                    + str(min(self.distances)))
        except:
            return 'Simulation complete'


solar = Solar('solar-system-data', 20000)
print solar.run()

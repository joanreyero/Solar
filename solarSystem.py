import json
from planet import Planet
from numpy.linalg import norm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Solar(object):

    def __init__(self, data_name, time_step):
        with open(data_name + '.json') as json_data:
            data = json.load(json_data)

        self.planets = [Planet(*data[planet]+[time_step])
                        for planet in data]

        for planet in self.planets:
            planet.update_acc(self.planets)

    def init(self):
       return self.patches

    def animate(self, i):
        self.move()
        for n, planet in enumerate(self.planets):
            #print planet.pos
            self.patches[n].center = (planet.pos[0], planet.pos[1])
            #print self.patches[n].center
            #print '\n'
        return self.patches

    def move(self):
        for planet in self.planets:
            planet.update_pos()
        for planet in self.planets:
            planet.update_vel_acc(self.planets)

    def run(self):
        fig = plt.figure()
        ax = plt.axes()
        axes = 4e11
        self.patches = [plt.Circle((planet.pos[0], planet.pos[1]),
                                   5*10**9, color = planet.color)
                        for planet in self.planets]
        for patch in self.patches:
            ax.add_patch(patch)
        ax.axis('scaled')
        ax.set_xlim(-axes, axes)
        ax.set_ylim(-axes, axes)

        anim = FuncAnimation(fig, self.animate, init_func = self.init, interval = 1)
        plt.show()


solar = Solar('solar-system-data', 2000)

solar.run()



#print '\n'*2

#for planet in solar.planets:
 #   print planet.pos

#print solar.move()

#print '\n'

#for planet in solar.planets:
 #   print planet.pos

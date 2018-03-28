import json
from planet import Planet
from numpy.linalg import norm

with open('data3.json') as json_data:
    data = json.load(json_data)

time = 1000

def get_planet(planet):
    return map(float, [planet['mass'],
                       planet['radius'],
                       planet['start_angle'],
                       time])

planet_list = [Planet(*get_planet(data[planet])) for planet in data]

def get_other_planets(planet):
    return [p for p in planet_list if p != planet]

print 'accelerations:'
for planet in planet_list:
    other_planets = get_other_planets(planet)
    planet.acceleration = planet.get_acceleration(other_planets)
    print planet.acceleration
print '\n'

def move(planet_list):
    """Moving the planet updating the position, velocity and acceleration.
    """

    for planet in planet_list:
        # Removing self from planets
        other_planets = get_other_planets(planet)
        print other_planets

        print 'acceleration ' + str(planet.acceleration)
        print 'velocity ' + str(planet.vel)
        planet.position()  # Calculate and update the new position
        print 'new position' + str(planet.pos)

    for planet in planet_list:
        # Removing self from planets
        other_planets = get_other_planets(planet)

        # Calculate the acceleration in the next step,
        #needed for the new velocity.
        new_acceleration = planet.get_acceleration(other_planets)
        planet.velocity(new_acceleration)  # Calculate the new velocity
        # Update the accelerations.
        planet.old_acceleration = planet.acceleration
        planet.acceleration = new_acceleration


for _ in range(10):
    for planet in planet_list:
        print planet.pos, norm(planet.pos)

    move(planet_list)
    print '\n\n'



#print planet_list[0].pos
#planet_list[0].position()
#print planet_list[0].pos

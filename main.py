import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import animation
# this will come in handy later


def distance(coord_1, coord_2):
    return np.sqrt((coord_1[0]-coord_2[0])**2 + (coord_1[1]-coord_2[1])**2)


class individual:
    # each individual is instatiated with a location,
    # a status and a set of boundaries
    def __init__(self, coords, status, bounds, speed):
        self.coord = coords
        self.status = status
        self.bounds = bounds
        self.speed = speed
        self.time = 0
        self.removed = 0

    # in this example I imagine each indivual moving in a given direction
    # which we can change at any point in time
    def set_direction(self):
        angle = np.random.uniform(0, 2*np.pi)
        x_direction = np.cos(angle)
        y_direction = np.sin(angle)

        self.x_direction = x_direction
        self.y_direction = y_direction

    # Every turn, the individual will updat their location
    def update_location(self):
        speed = self.speed
        bounds = self.bounds
        distance = speed*np.random.random()
        # What to do if they run up against the boundary of the region?
        if self.coord[0] + distance*self.x_direction < 0:
            new_x = -distance*self.x_direction-self.coord[0]
            self.x_direction = -self.x_direction
        elif self.coord[0] + distance*self.x_direction > bounds[0]:
            new_x = 2*bounds[0]-distance*self.x_direction - self.coord[0]
            self.x_direction = -self.x_direction
        else:
            new_x = self.coord[0] + distance*self.x_direction

        if self.coord[1] + distance*self.y_direction < 0:
            new_y = -distance*self.y_direction-self.coord[1]
            self.y_direction = -self.y_direction
        elif self.coord[1] + distance*self.y_direction > bounds[1]:
            new_y = 2*bounds[1]-distance*self.y_direction - self.coord[1]
            self.y_direction = -self.y_direction
        else:
            new_y = self.coord[1] + distance*self.y_direction

        self.coord = (new_x, new_y)

    # each individual has a certain chance to be infected by others
    # within a certain radius
    def transmission(self, others, radius, probability):
        # of course if they're already recoved it's moot
        if self.removed == 1:
            pass
        # and if they're already infected, they won't get infected again
        elif self.status == 1:
            # but we can track how long they've been infected
            self.time += 1
            # And put them into the 'removed' category
            if self.time == 175:
                self.status = 2
                self.removed = 1
        else:
            # but if they're susceptible
            neighbor_count = 0
            for other in others:
                # then every infected person nearby increases the probability of transmission
                if other.status == 1:
                    if distance(self.coord, other.coord) < radius:
                        neighbor_count += 1
            if sum([1 for x in np.random.random(neighbor_count) if x > probability]) > 0:
                self.status = 1


#reduced radius and probability numbers
bounds = (5,5)
radius = .05
probability = .1

#I'm only going to model 200 people this time
everyone = []
for n in range(5):
    everyone.append(individual((10*np.random.random(),10*np.random.random()),
                               1,bounds,np.random.random()/25))

for n in range(195):
    everyone.append(individual((10*np.random.random(),10*np.random.random()),
                               0,bounds,np.random.random()/25))

for n in range(0,len(everyone)):
    everyone[n].set_direction()

fig = plt.figure(figsize=(5,5))
plt.xlim(0,5)
plt.ylim(0,5)
ax=plt.axes()

ims=[]

for n in range(300):
  #No we need to track everyone's coordinates
    coords = []
    status = []
    for person in everyone:
        coords.append(person.coord)
        status.append(person.status)
    #preferably as numpy arrays
    status = np.array(status)
    coords = np.array(coords)
    #Which we can easily index for a scatter plot on one line
    im=[ax.scatter(coords[:,0],coords[:,1],c=status,cmap='winter', norm=mpl.colors.Normalize(vmin=-1, vmax=1))]
    #Add this artis object to our list
    ims.append(im)
    #And then check for transmission and update everyone's location
    for i in range(0,len(everyone)):
        everyone[i].transmission(everyone[:i]+everyone[i+1:],radius,probability)
    for i in range(0,len(everyone)):
        everyone[i].update_location()
#create the animation
ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,repeat_delay=1000)
plt.show()
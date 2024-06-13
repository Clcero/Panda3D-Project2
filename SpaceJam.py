# Luke Classen, 6/12/2024

from direct.showbase.ShowBase import ShowBase
import math, sys, random

import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses

class MyApp(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        # Create world
        self.SetupScene()

        # Start setting key bindings.
        self.accept('escape', self.quit)

    def SetupScene(self):
        '''Load universe, space station, player, then randomly place the planets.'''

        # Path dictionary
        planets = [
            {"texture_path": "./Assets/Planets/Mars.jpg"},
            {"texture_path": "./Assets/Planets/Purple.png"},
            {"texture_path": "./Assets/Planets/Sand.png"},
            {"texture_path": "./Assets/Planets/Tiled.jpg"},
            {"texture_path": "./Assets/Planets/Wicker.jpg"},
            {"texture_path": "./Assets/Planets/Rock.jpg"}
        ]

        # Spawn planets at "random" positions within the player's view
        self.minDistance = 500
        self.existing_positions = []

        for i, planet_spec in enumerate(planets):
            position = self._generate_position(self.existing_positions, self.minDistance)
            planet = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, f"Planet{i+1}", planet_spec["texture_path"], position, random.randint(150, 275))
            setattr(self, f"Planet{i+1}", planet)
            self.existing_positions.append(position)

        self.Universe = spaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, 'Universe', "Assets/Universe/Universe.jpg", (0, 0, 0), 15000)
        self.SpaceStation1 = spaceJamClasses.SpaceStation(self.loader, "./Assets/Space Station/station.glb", self.render, 'Space Station', "./Assets/Space Station/Metal.jpg", (75, 500, 100), 1)
        self.Hero = spaceJamClasses.Spaceship(self.loader, "./Assets/Spaceships/spaceship.obj", self.render, 'Hero', "./Assets/Spaceships/spaceship.jpg", (1000, 1200, -50), 2, (0, 0, 90))

        fullCycle = 60

        for j in range(fullCycle):
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.Planet2, nickName, j, fullCycle, 2)

    def distance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)
    
    def _generate_position(self, existing_positions, min_distance):
        while True:
            new_position = (random.randint(-2000, 8000), random.randint(3000, 6000), random.randint(350, 2550))
            if all(self.distance(new_position, pos) >= min_distance for pos in existing_positions):
                return new_position

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 10)

    # Prepare message if server wants to quit.
    def quit(self):
        '''Exit game.'''
        sys.exit()
        
# Instances, then runs program
app = MyApp()
app.run()
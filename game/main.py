from game_engine import init, Layer, Sprite, Text
from asteroid import (Bullet, SpaceShip, Asteroid, GUI, AsteroidGame, GameLayer, Title, Life)
from random import randint
import pyglet

#Add victory condition ? And Level ?

resolution = (800,600)  #Adaptable Size
init(resolution, "Nexus VI : The Asteroid Game")

game = AsteroidGame()
background_layer = Layer()
game_layer = GameLayer()
title = Title()
life = Life(position=(randint(0,800),randint(0,600))) #Adaptable position

speed= randint(-100,100), randint(-100,100) #Adaptable position

spaceship = SpaceShip((400,300)) #Adaptable position
game_layer.add(spaceship)

for i in range(randint(2, 5)):
    position = (400,300) #Adaptable position
    while (position[0] >320 and position [0] < 480) and (position[1] > 220 and position [1] < 380): #Adaptable position
        position = randint(0,800),randint(0,600) #Adaptable position
    asteroid = Asteroid(position, speed)
    game_layer.add(asteroid)

gui = GUI(spaceship)

background = Sprite("assets/background.png", (0,0), anchor=(0,0))
background_layer.add(background)
game.add(background_layer)
game.add(game_layer)
game.add(gui)
game.add(title)
# game.debug = True

music = pyglet.media.load("assets/music.wav", streaming=False)
music_loop = pyglet.media.SourceGroup(music.audio_format, None)
music_player = pyglet.media.Player()
music_player.queue(music)
music_loop.loop = True
music_player.queue(music_loop)
music_player.play()

game.run()


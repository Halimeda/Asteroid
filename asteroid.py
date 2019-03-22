from game_engine import init, Game, Layer, Sprite, Text
from random import randint
from pyglet.window.key import symbol_string
from math import cos, sin, radians, sqrt
import pyglet

class AsteroidGame(Game):

    def __init__(self):
        super().__init__()
        self.started = False

    def add(self, layer):
        super().add(layer)
        layer.game = self

    def update(self, dt):
        if self.started:
            super().update(dt)

class Title(Layer):
    def __init__(self):
        super().__init__()
    #self.start_music =Sound("") #Create and ad start music
        self.text = Sprite("assets/title.png")
        self.add(self.text)

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)
        self.game.started = True
        self.text.destroy()

class GUI(Layer):

    #Spaceship live count and draw

    def __init__(self, spaceship):
        super().__init__()
        self.spaceship = spaceship
        self.lives = []

    def draw_life(self):

        position_initial = (795, 565)

        for i in range(self.spaceship.lives):
            image_path = "assets/life.png"
            position = (position_initial[0] - (i * (16 + 5)), position_initial[1])
            life = Sprite(image_path, position, anchor = (16, 16))
            self.lives.append(life)
            self.add(life)
    
    #add live during the game

    def update(self, dt):
        super().update(dt)

        if (len(self.lives) > self.spaceship.lives) and (len(self.lives) > 0):
            life = self.lives.pop()
            life.destroy()

        elif (len(self.lives) < self.spaceship.lives): 
            self.lives = []          
            self.draw_life()

class GameLayer(Layer):

    # Score

    def __init__(self):
        super().__init__()
        self.game = None

        self.score_points = 0
        self.score= Text("", (10, 570), font_size=20)
        self.add(self.score)

    def update(self, dt):
        super().update(dt)
        self.score.element.text = "Score : " + str(self.score_points)

    def change_score(self, amount):
        self.score_points = max(self.score_points + amount, 0)

class SpaceObject(Sprite):

    def __init__(self,image_path, position, speed = (0,0), anchor = (0,0), rotation_speed = (0)):
        super().__init__(image_path, position, anchor=anchor)
        self.speed = speed
        self.rotation_speed = rotation_speed

    def update(self, dt):

        move_x = self.speed[0] * dt
        move_y = self.speed[1] * dt
        self.position = (self.position[0] + move_x, self.position[1] + move_y)

        if (self.position[0] > 800):
            self.position = (0, (self.position[1]))
        elif (self.position[0] < 0):
            self.position = (800, (self.position[1]))

        if (self.position[1] > 600):
            self.position = ((self.position[0]), 0)
        elif (self.position[1] < 0):
            self.position = ((self.position[0]), 600)

        self.rotation += self.rotation_speed * dt
        

        super().update(dt)

class Bullet(SpaceObject):
    def __init__(self, position, speed = (0,0)):
        image_path = "assets/bullet.png"
        self.lifetime = 3
        super().__init__(image_path, position, speed, anchor = (8,8))

    def update(self, dt):

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()
        super().update(dt)
    
    def on_collision(self, other):
        if isinstance(other, Asteroid):
            other.destroy()
            self.destroy()

class Life(SpaceObject):

    def __init__(self, position, speed = (randint(-100, 100), randint(-100, 100))):
        image_path = "assets/life.png"
        self.timer_life = 0
        self.lifetime = 10
        super().__init__(image_path, position, speed, anchor = (16,16))


    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()
        super().update(dt)

#class Flame(SpaceObject):
    #Add flame when spaceship accelerate
    #def __init__(self, ship_position, ship_speed, ship_rotation):
        #image_path = "assets/flame.png"
        #super().__init__(image_path, position=ship_position, speed=ship_speed, rotation=ship_rotation, anchor=(2.5, 6))

class SpaceShip(SpaceObject):
    def __init__(self, position):
        image_path = "assets/Nexus.png"
        self.engine_on = False
        self.lives = 5
        self.invincibility_time = 3
        self.invincible = 0
        self.timer_asteroid = 0
        self.timer_life = 0
        self.engine_back = False
        self.shoot_sound = pyglet.media.load("assets/Laser_Shoot5.wav", streaming=False)
        self.hit_sound = pyglet.media.load("assets/Explosion2.wav", streaming=False)
        self.dead_sound = pyglet.media.load("assets/Explosion3.wav", streaming=False)

        super().__init__(image_path, position, speed = (0, 0), anchor = (24,40))

    def add_life(self):
        self.lives += 1
    

    def add_asteroid(self):
        if self.timer_asteroid > 15:
            self.timer_asteroid = 0
            speed = (randint(-100, 100), randint(-100, 100))
            position = randint(0,800),randint(0,600)
            new_asteroid = Asteroid(position, speed)
            self.layer.add(new_asteroid)

    def update(self, dt):

        angle = -radians(self.rotation - 90)
        dspeedx = 0
        dspeedy = 0

        if self.timer_life > 20:
            bonus_life = Life(position = (randint(0,800),randint(0,600)), speed = (randint(-100, 100), randint(-100, 100)))
            self.layer.add(bonus_life)
            self.timer_life = 0

        if self.engine_on and self.engine_back == False:

            dspeedx = cos(angle) * dt * 100
            dspeedy = sin(angle) * dt * 100
        
        if self.engine_on and self.engine_back == True:

            dspeedx = cos(angle) * dt * -100
            dspeedy = sin(angle) * dt * -100
        
        self.speed = ((self.speed[0] + dspeedx), (self.speed[1] + dspeedy))

        speed_vector = sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)

        if speed_vector > 1000:
            self.speed = ((self.speed[0] / speed_vector * 1000), (self.speed[1] / speed_vector * 1000))

        if self.invincible > 0:
            self.invincible -= dt
            self.opacity = 80
        
        else:
            self.opacity = 255

        self.timer_asteroid += dt
        self.timer_life += dt
        self.add_asteroid()
        super().update(dt)

    def shoot(self):
        angle = -radians(self.rotation - 90)

        bullet_speed = (cos(angle) * 300, sin(angle) * 300)
        bullet = Bullet(self.position, bullet_speed)
        self.shoot_sound.play()
        self.layer.change_score(-50)
        self.layer.add(bullet)
    
    def on_collision(self, other):
        if isinstance(other, Life):
            other.destroy()
            self.lives += 1
    
    def destroy(self):
        if self.invincible <= 0:
            self.layer.change_score(-500)
            self.hit_sound.play()
            self.lives -= 1
            if self.lives > 0:
                for n in range(10):
                    speed = randint(-100, 100), randint(-100, 100)
                    bullet = Bullet(self.position, speed)
                    self.layer.add(bullet)
                self.invincible = self.invincibility_time
            else:
                self.dead_sound.play()
                super().destroy()

                gameover =  Layer()
                bg = Sprite("assets/gameover.png")
                gameover.add(bg)
                self.layer.game.add(gameover) 

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "UP" or symbol_string(key) == "Z":
            self.engine_on = True
            self.engine_back = False
            #self.flame = Flame(self.position, self.speed, self.rotation)
            #self.layer.add(self.flame)


        elif symbol_string(key) == "DOWN" or symbol_string(key) == "S": 
            self.engine_on = True
            self.engine_back = True   
        
        if symbol_string(key) == "RIGHT" or symbol_string(key) == "D":
            self.rotation_speed = 100
            
        elif symbol_string(key) == "LEFT" or symbol_string(key) == "Q":
            self.rotation_speed = -100
        
        if symbol_string(key) == "SPACE":
            self.shoot()

    def on_key_release(self, key, modifiers):
        if symbol_string(key) == "UP" or symbol_string(key) == "Z":
            self.engine_on = False
            self.engine_back = False
            #self.flame.destroy()

        elif symbol_string(key) == "DOWN" or symbol_string(key) == "S":
            self.engine_on = False
            self.engine_back = False
        
        if symbol_string(key) == "RIGHT" or symbol_string(key) == "D":
            self.rotation_speed = 0
        elif symbol_string(key) == "LEFT" or symbol_string(key) == "Q":
            self.rotation_speed = 0

class Asteroid(SpaceObject):

    def __init__(self, position=(randint(0,800),randint(0,600)), speed = (randint(-100,100), randint(-100,100)), category = 3):

        self.explosion_sound = pyglet.media.load("assets/Explosion.wav", streaming=False)
        self.time_count = 0

        if category == 3:
            image_path = "assets/asteroid128.png"
            anchor = (64, 64)
        elif category == 2:
            image_path = "assets/asteroid64.png"
            anchor = (32, 32)
        else:
            image_path = "assets/asteroid32.png"
            anchor = (16, 16)

        super().__init__(image_path, position, speed, anchor = anchor, rotation_speed=randint(-50, 50))
        self.category = category

    def on_collision(self, other):
        if isinstance(other, SpaceShip):
            other.destroy()

    def destroy(self):
        super().destroy()
        self.layer.change_score(int(300 / self.category))
        self.explosion_sound.play()
        if self.category == 3:
            self.asteroid_count =-1
        if self.category > 1:
            self.category -= 1
            for i in range(3):
                speed = (randint(-100, 100), randint(-100, 100))
                asteroid = Asteroid(self.position, speed, self.category)
                self.layer.add(asteroid)

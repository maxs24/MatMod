import random
import math
import pygame


class Particle():

    def __init__(self, radius, mass, position, velocity):
        self.radius = radius
        self.mass = mass
        self.position = position
        self.velocity = velocity

    def move(self):

        force = [0, 0]
        force[0] = g[0] * self.mass + (-k) * self.velocity[0]
        force[1] = g[1] * self.mass + (-k) * self.velocity[1]

        self.velocity[0] += 1 / self.mass * force[0] * dt
        self.velocity[1] += 1 / self.mass * force[1] * dt

        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

        # проверка столкновения с нижней стенкой
        D = height - self.position[1]
        if D < self.radius:
            self.position[1] -= (self.radius - D)
            self.velocity[1] *= -1
        # проверка столкновения с верхней стенкой
        D = self.position[1]
        if D < self.radius:
            self.position[1] += (self.radius - D)
            self.velocity[1] *= -1
        # проверка столкновения с правой стенкой
        D = width - self.position[0]
        if D < self.radius:
            self.position[0] -= (self.radius - D)
            self.velocity[0] *= -1
        # проверка столкновения с левой стенкой
        D = self.position[0]
        if D < self.radius:
            self.position[0] += (self.radius - D)
            self.velocity[0] *= -1

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), tuple(self.position),
                           self.radius, 2)

    def velosity(self):  # модуль скоростей шаров
        v = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        return v


class Gist():
    def __init__(self, ax, ay, h):
        self.ax = ax
        self.ay = ay
        self.h = h

    def draw(self, y1):
        # pygame.draw.rect(screen,(0,0,0),(self.ax, self.ay, self.bx, y1))
        pygame.draw.polygon(
            screen,
            (0, 0, 0),
            [
                [self.ax, self.ay - y1],
                [self.ax, self.ay],
                [self.ax + self.h, self.ay],
                [self.ax + self.h, self.ay - y1],
            ]
        )


def collide(p1, p2):
    R = [(i - j) for i, j in zip(p2.position, p1.position)]
    R_abs = math.sqrt(sum([i ** 2 for i in R]))
    R_unit = [i / R_abs for i in R]
    Delta = p1.radius + p2.radius - R_abs

    if Delta > 0:
        v1x = p1.velocity[0]
        v1y = p1.velocity[1]
        v2x = p2.velocity[0]
        v2y = p2.velocity[1]
        m1 = p1.mass
        m2 = p2.mass

        n = R_unit
        t = [-n[1], n[0]]

        v1n = n[0] * v1x + n[1] * v1y
        v1t = -n[1] * v1x + n[0] * v1y
        v2n = n[0] * v2x + n[1] * v2y
        v2t = -n[1] * v2x + n[0] * v2y

        v1n_ = (2 * m2 * v2n + (m1 - m2) * v1n) / (m1 + m2)
        v2n_ = (2 * m1 * v1n + (m2 - m1) * v2n) / (m2 + m1)

        p1.velocity[0] = n[0] * v1n_ - n[1] * v1t
        p1.velocity[1] = n[1] * v1n_ + n[0] * v1t
        p2.velocity[0] = n[0] * v2n_ - n[1] * v2t
        p2.velocity[1] = n[1] * v2n_ + n[0] * v2t

        p1.position[0] += -(Delta / 2) * R_unit[0]
        p1.position[1] += -(Delta / 2) * R_unit[1]
        p2.position[0] += (Delta / 2) * R_unit[0]
        p2.position[1] += (Delta / 2) * R_unit[1]


#######################################################

dt = .05
my_particles = []
my_gist = []
num = 100
numG = 10
g = [0, 0]
k = 0

for i in range(numG):
    # p = Gist(800 - (i+1)*10, 100, 7)
    p = Gist(50 + (i + 1) * 10, 450, 10)
    my_gist.append(p)

X_MIN = 100
Y_MIN = 100
for i in range(15):
    Y_MIN = 100
    for j in range(15):
        p = Particle(5, 1, [X_MIN, Y_MIN],
                     [40, 40])
        Y_MIN += 15
        my_particles.append(p)
    X_MIN += 15

#######################################################

background_color = (255, 255, 0)
(width, height) = (840, 480)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Гистограмма')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)

    velocity_list = []
    for particle in my_particles:
        particle.move()
        particle.draw()
        velocity_list.append(particle.velosity())

    vmax = max(velocity_list)
    vmin = min(velocity_list)
    dn = (vmax - 0) / numG

    for i, gist in enumerate(my_gist):
        res = [item for item in velocity_list if vmin + dn * i <= item < vmin + dn * (i + 1)]
        gist.draw(len(res) * 2)
        res = []

    for i in range(len(my_particles) - 1):
        for j in range(i + 1, len(my_particles)):
            collide(my_particles[i], my_particles[j])

    pygame.display.flip()

pygame.quit()

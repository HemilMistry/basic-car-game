import pygame
import sys
import random

pygame.init()

width, height = 800, 600  
red = (215, 50, 50)
green = (50, 170, 80)
white = (255, 255, 255)
grey = (120, 120, 120)
carX = 400
carY = 400

gameDisplay = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 128)


# Car Class
class Car:
    def __init__(self, x, y, cooldown):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 40  
        self.cooldown = cooldown
        self.last_move_time = 0
        self.target_x = self.x
        self.speed = 5

    def move(self, keys):
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_a] and self.x > 255 and current_time - self.last_move_time > self.cooldown:
            self.target_x -= 255
            self.last_move_time = current_time

        if keys[pygame.K_d] and self.x < 625 and current_time - self.last_move_time > self.cooldown:
            self.target_x += 255
            self.last_move_time = current_time

        if self.x < self.target_x:
            self.x += self.speed
            if self.x > self.target_x:
                self.x = self.target_x
        elif self.x > self.target_x:
            self.x -= self.speed
            if self.x < self.target_x:
                self.x = self.target_x
        

    def load(self):
        try:
            pygame.draw.rect(gameDisplay, white, (self.x, self.y, self.width, self.height)) 
        except pygame.error as e:
            print(f"Error drawing rectangle: {e}")

# Road Markings Class
class RoadMarkings:
    def __init__(self, x, width, height, speed, count):
        self.x = x
        self.width = width
        self.height = height
        self.speed = speed
        self.count = count
        self.spacing = 140  
        self.y_values = [i * self.spacing for i in range(self.count)]

    def move(self):
        for i in range(len(self.y_values)):
            self.y_values[i] += self.speed
            if self.y_values[i] > 600:
                self.y_values[i] = -self.height

    def draw(self):
        for y in self.y_values:
            pygame.draw.rect(gameDisplay, white, (self.x, y, self.width, self.height))

car = Car(carX, carY, 200)
markings1 = RoadMarkings(266, 10, 70, 7, 5)
markings2 = RoadMarkings(533, 10, 70, 7, 5)

# Enemy Car Class
enemyXValues = [carX, carX - 255, carX + 255]
score = 1
highscoreValue = 0

def highscore():
    global highscoreValue
    highscore_font = pygame.font.Font(None, 36)
    highscore_text = highscore_font.render(f"Highscore: {highscoreValue}", True, white)
    highscore_rect = highscore_text.get_rect(topright=(width - 10, 10))
    gameDisplay.blit(highscore_text, highscore_rect)

    if gameOver and highscoreValue < score:
        highscoreValue = score  

        new_highscore_text = highscore_font.render(f"NEW Highscore: {highscoreValue}", True, white)
        highscore_rect = new_highscore_text.get_rect(center=(width // 2, height // 2 + 200))

        gameDisplay.blit(new_highscore_text, highscore_rect)


class Enemy():
    def __init__(self):
        self.x = random.choice(enemyXValues)
        self.y = 0
        self.speed = 5 + score

    def load(self):
        try:
            pygame.draw.rect(gameDisplay, red, (self.x, self.y, 20, 40))
        except pygame.error as e:
            print(f"Error drawing rectangle: {e}")

    def move(self):
        global score
        self.y += self.speed
        if self.y > 600:
            self.y = 0
            self.x = random.choice(enemyXValues) 
            score += 1 
            if self.speed < 12:
                self.speed += 0.5
            elif score > 20:
                self.speed += 0.25
                if self.speed > 15:
                    self.speed = 15

        
    def check_collision(self, player):
        enemy_rect = pygame.Rect(self.x, self.y, 20, 40)
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height) 

        return enemy_rect.colliderect(player_rect)

enemy = Enemy()

# Game Over Screen
retry_button = pygame.Rect(width // 2 - 50, height // 2 + 50, 100, 50)
def game_over():
    game_over_font = pygame.font.Font(None, 64)
    game_over_text = game_over_font.render("Game Over", True, white)
    text_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 50))

    pygame.draw.rect(gameDisplay, green, retry_button) 

    retry_font = pygame.font.Font(None, 36)
    retry_text = retry_font.render("Retry", True, white)
    retry_rect = retry_text.get_rect(center=(width // 2, height // 2 + 75))

    gameDisplay.blit(game_over_text, text_rect)
    gameDisplay.blit(retry_text, retry_rect)

    pygame.display.update()

speed_font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
gameOver = False

while True:
    if not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()

        gameDisplay.fill(green)

        pygame.draw.rect(gameDisplay, grey, (20, 0, 760, 680))

        markings1.move()
        markings1.draw()

        markings2.move()
        markings2.draw()

        car.move(keys)
        car.load()

        enemy.move()
        enemy.load()

        # Score Text
        Scoretext = font.render(str(score), True, (0, 0, 0,))
        Scoretext.set_alpha(50)
        text_rect = Scoretext.get_rect(center=(width // 2, height // 2))
        gameDisplay.blit(Scoretext, text_rect)

        # FPS Text
        fps_text = speed_font.render(f"FPS: {round(clock.get_fps(), 0)}", True, white)
        fps_rect = fps_text.get_rect(topleft=(10, 10))
        gameDisplay.blit(fps_text, fps_rect)

        highscore()

        if enemy.check_collision(car):
            gameOver = True
            game_over()

    else:
        game_over()
        highscore()

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if retry_button.collidepoint(mouse_x, mouse_y):
                    gameOver = False
                    score = 1
                    car = Car(carX, carY, 200)
                    enemy = Enemy()

    pygame.display.update()
    clock.tick(60)
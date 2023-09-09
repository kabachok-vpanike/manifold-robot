import os
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

WIDTH, HEIGHT = 1076, 800
MAP_SIZE = int(input("Enter map size (e.g. 6): "))
CELL_SIZE = int(input("Enter cell size (e.g. 10): "))
OBSTACLE_SIZE = HEIGHT // MAP_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot with obstacles")
WHITE = (255, 255, 255)
OBSTACLE_IMAGE = pygame.image.load(os.path.join('pictures/obstacle.jpg'))
OBSTACLE_IMAGE = pygame.transform.scale(OBSTACLE_IMAGE, (OBSTACLE_SIZE, OBSTACLE_SIZE))
GENERATE_BUTTON_IMAGE = pygame.image.load(os.path.join('pictures/button1.png'))
REPLACE_ROBOT_BUTTON_IMAGE = pygame.image.load(os.path.join('pictures/button2.png'))
ROBOT_IMAGE = pygame.image.load(os.path.join('pictures/robot.png'))
ROBOT_IMAGE = pygame.transform.scale(ROBOT_IMAGE, (OBSTACLE_SIZE, OBSTACLE_SIZE))
FPS = 60
FREE_CELLS = []
GAMEMAP = []
ROBOT_POS = [-1, -1]

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False 
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        return action

generate_button = Button(1076 - 260 - 8, 0 + 8, GENERATE_BUTTON_IMAGE)

replace_robot_button = Button(1076 - 260 - 8, 0 + 80 + 8, REPLACE_ROBOT_BUTTON_IMAGE)

def calculate_distance():
    
    if len(GAMEMAP) == 0:
        return
    i = ROBOT_POS[0]
    j = ROBOT_POS[1]
    while i >= 0 and GAMEMAP[i][j] != 1:
        i -= 1
    obstacle_ahead = [(j + 0.5) * CELL_SIZE, (i + 1) * CELL_SIZE]
    
    i = ROBOT_POS[0]
    j = ROBOT_POS[1]
    while j < MAP_SIZE and GAMEMAP[i][j] != 1:
        j += 1
    obstacle_right = [j * CELL_SIZE, (i + 0.5) * CELL_SIZE]

    i = ROBOT_POS[0]
    j = ROBOT_POS[1]
    while i < MAP_SIZE and GAMEMAP[i][j] != 1:
        i += 1
    obstacle_back = [(j + 0.5) * CELL_SIZE, i * CELL_SIZE]

    i = ROBOT_POS[0]
    j = ROBOT_POS[1]
    while j >= 0 and GAMEMAP[i][j] != 1:
        j -= 1
    obstacle_left = [(j + 1) * CELL_SIZE, (i + 0.5) * CELL_SIZE]

    return [obstacle_ahead, obstacle_right, obstacle_back, obstacle_left]
    
def map_generation(size, regenerate=True):
    global FREE_CELLS
    global GAMEMAP
    global ROBOT_POS
    obstacle_ahead = 0
    obstacle_right = 0
    obstacle_back = 0
    obstacle_left = 0
    if regenerate:
        GAMEMAP = []
        FREE_CELLS = []
        GAMEMAP = [[random.randint(0, 1) for i in range(size)] for j in range(size)]
        for i in range(len(GAMEMAP)):
            for j in range(len(GAMEMAP[i])):
                if not(GAMEMAP[i][j]):
                    FREE_CELLS.append([i, j])
    if len(ROBOT_POS):
        GAMEMAP[ROBOT_POS[0]][ROBOT_POS[1]] = 0
    old_x, old_y = ROBOT_POS
    ROBOT_POS = random.choice(FREE_CELLS)
    GAMEMAP[ROBOT_POS[0]][ROBOT_POS[1]] = 2
    FREE_CELLS.append([old_x, old_y])
    FREE_CELLS.remove(ROBOT_POS)
    return GAMEMAP

def obstacles_generation(arr):
    obstacles = []
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == 1:
                obstacles.append([0, pygame.Rect(j * OBSTACLE_SIZE, i * OBSTACLE_SIZE, OBSTACLE_SIZE, OBSTACLE_SIZE)])
            if arr[i][j] == 2:
                obstacles.append([1, pygame.Rect(j * OBSTACLE_SIZE, i * OBSTACLE_SIZE, OBSTACLE_SIZE, OBSTACLE_SIZE)])
    return obstacles

def draw_window(obstacles_array):
    global obstacles
    WIN.fill(WHITE)
    for obstacle in obstacles_array:
        if obstacle[0] == 0:
            WIN.blit(OBSTACLE_IMAGE, (obstacle[1].x, obstacle[1].y))
        if obstacle[0] == 1:
            WIN.blit(ROBOT_IMAGE, (obstacle[1].x, obstacle[1].y))
    if generate_button.draw():
        obstacles = obstacles_generation(map_generation(MAP_SIZE))
    if replace_robot_button.draw():
        obstacles = obstacles_generation(map_generation(MAP_SIZE, False))
        
    pygame.draw.line(WIN, (0, 0, 0), (0, 0), (0, 800), 4)
    pygame.draw.line(WIN, (0, 0, 0), (0, 0), (800, 0), 4)
    
    pygame.font.init()
    my_font = pygame.font.SysFont('Noto Sans', 30)
    for shift in range(1, MAP_SIZE):
        text_surface = my_font.render(str(CELL_SIZE * shift), False, (0, 0, 0))
        WIN.blit(text_surface, (OBSTACLE_SIZE * shift + 4, 10))
        pygame.draw.line(WIN, (0, 0, 0), (OBSTACLE_SIZE * shift, 0), (OBSTACLE_SIZE * shift, 20), 4)

        WIN.blit(text_surface, (10, OBSTACLE_SIZE * shift + 4))
        pygame.draw.line(WIN, (0, 0, 0), (0, OBSTACLE_SIZE * shift), (20, OBSTACLE_SIZE * shift), 4)

    distances = calculate_distance()
    pos = ["0° obstacle:", "90° obstacle:", "180° obstacle:", "270° obstacle:"]
    my_font = pygame.font.SysFont('Noto Sans', 35)
    for ind in range(len(distances)):
        obstacles_coordinates = distances[ind]
        text_surface =  my_font.render(pos[ind], False, (0, 0, 0))
        WIN.blit(text_surface, (800 + 16, 200 + ind * 70))
        text_surface = my_font.render(str("(" + str(obstacles_coordinates[0]) + ", " + str(obstacles_coordinates[1]) + ")"), False, (0, 0, 0))
        WIN.blit(text_surface, (800 + 16, 200 + ind * 70 + 25))
        
    #WIN.blit(text_surface, (10, OBSTACLE_SIZE / 2))
    pygame.display.update()
    
game_map = map_generation(MAP_SIZE)
obstacles = obstacles_generation(game_map)
    
def main():
    clock = pygame.time.Clock();
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(obstacles)
    pygame.quit()
    
if __name__ == "__main__":
    main()
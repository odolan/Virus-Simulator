import pygame
import random
import graph as graph

"""
s = susceptible 
s-I susceptible - but in isolation
i = infected 
i-a = infected but asymptomatic 
r = recovered 
c = community wall 
"""

#controls simulation
class Grid:

    #default setup when object created
    def __init__(self):
        self.width = 400
        self.height = 400

        #possible grid row/column amounts
        self.possible_grid_amounts = [4,5,8,10,16,20,25,40,50]
        self.size = 8

        pygame.init()
        self.screen = pygame.display.set_mode([self.width+500, self.height+80])
        pygame.display.set_caption("Virus Simulation - by: Owen Dolan")
        self.done = False
        self.clock = pygame.time.Clock()
        self.margin = 2

        self.time = 0

        self.contage_factor = 10
        self.completely_isolated_factor = 4

        #button setup
        self.start_button = False
        self.reset_button = False
        self.random_button = False

        #hold run history to graph
        self.previously_infected = []
        self.previously_susceptible = []
        self.previously_recovered = []

        self.grid = [[] for i in range(self.possible_grid_amounts[self.size])]
        for i in range(self.possible_grid_amounts[self.size]):
            for i in range(self.possible_grid_amounts[self.size]):
                self.grid[i].append('s')

        self.completely_isolate_people(self.completely_isolated_factor)

    def display(self):
        while not self.done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN: # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos() # Change the x/y screen coordinates to grid coordinates
                    if pos[0] < self.width and pos[0] > 0 and pos[1] < self.height and pos[1] > 0:

                        #determine which grid tile pressed
                        column = int(pos[0] // (self.width/self.possible_grid_amounts[self.size]))
                        row = int(pos[1] // (self.height/self.possible_grid_amounts[self.size]))
                        if self.grid[row][column] != 'c':
                            self.grid[row][column] = 'i' #sets the person to be infected

                    # Determine if start button is pressed
                    if pos[0] > self.width + 20 and pos[0] < self.width + 90 and pos[1] > 20 and pos[1] < 50:
                        if self.start_button == False:
                            self.start_button = True
                        else:
                            self.start_button = False

                    # Determine if reset button is pressed
                    if pos[0] > self.width + 20 and pos[0] < self.width + 90 and pos[1] > 50 and pos[1] < 80:
                        if self.reset_button == False:
                            self.reset_button = True
                        else:
                            self.reset_button = False

                    # Determine if random button is pressed
                    if pos[0] > self.width + 10 and pos[0] < self.width + 100 and pos[1] > 90 and pos[1] < 110:
                        if self.random_button == False:
                            self.random_button = True
                        else:
                            self.random_button = False

                    # if plus or minus grid size changed
                    if pos[0] > self.width + 20 and pos[0] < self.width + 50 and pos[1] > 145 and pos[1] < 175:
                        if self.size < len(self.possible_grid_amounts)-1:
                            self.reset_grid()
                            self.size += 1
                            self.grid = [[] for i in range(self.possible_grid_amounts[self.size])]
                            for i in range(self.possible_grid_amounts[self.size]):
                                for i in range(self.possible_grid_amounts[self.size]):
                                    self.grid[i].append('s')
                    if pos[0] > self.width + 55 and pos[0] < self.width + 85 and pos[1] > 145 and pos[1] < 175:
                        if self.size > 0:
                            self.reset_grid()
                            self.size -= 1
                            self.grid = [[] for i in range(self.possible_grid_amounts[self.size])]
                            for i in range(self.possible_grid_amounts[self.size]):
                                for i in range(self.possible_grid_amounts[self.size]):
                                    self.grid[i].append('s')

                    #contageious factor control buttons (+ annd -)
                    if pos[0] > 45 and pos[0] < 75 and pos[1] > self.height+35 and pos[1] < self.height+65:
                        if self.contage_factor >= 4:
                            self.contage_factor -= 1
                    if pos[0] > 80 and pos[0] < 110 and pos[1] > self.height + 35 and pos[1] < self.height + 65:
                        if self.contage_factor < 20:
                            self.contage_factor += 1

                    #complete isolation factor increase/decrease
                    if pos[0] > 235 and pos[0] < 265 and pos[1] > self.height + 35 and pos[1] < self.height + 65:
                        if self.completely_isolated_factor <= 40:
                            factor = self.completely_isolated_factor + 2
                            self.reset_grid()
                            self.completely_isolated_factor = factor
                            self.completely_isolate_people(self.completely_isolated_factor)
                    if pos[0] > 272 and pos[0] < 302 and pos[1] > self.height + 35 and pos[1] < self.height + 65:
                        if self.completely_isolated_factor >= 1:
                            factor = self.completely_isolated_factor - 2
                            self.reset_grid()
                            self.completely_isolated_factor = factor
                            self.completely_isolate_people(self.completely_isolated_factor)

                    # if community button pressed
                    if pos[0] > self.width+5 and pos[0] < self.width+115 and pos[1] > 180 and pos[1] < 210:
                        if self.size >= 5:
                            self.reset_grid()
                            self.add_counties()



            self.draw_grid_and_controls()

            self.clock.tick(10)
            pygame.display.flip()

            # if the run/start button is pressed -> values start updating
            if self.start_button == True:
                self.apply_next()
                self.time += 1
            else:
                graph.plot(self.screen, self.grid, self.time / 10, self.previously_infected, self.previously_susceptible, self.previously_recovered)

            # if reset button is pressed
            if self.reset_button == True:
                self.reset_grid()

            # if random button is pressed
            if self.random_button == True:
                self.reset_grid()
                self.random_start()
                self.random_button = False


        pygame.quit()


    # adds four community walls
    def add_counties(self):
        main_row = int(self.possible_grid_amounts[self.size]/2)

        for row in range(self.possible_grid_amounts[self.size]):
            for column in range(self.possible_grid_amounts[self.size]):
                if column == main_row and (row < int((main_row)-(.4*main_row)) or row > int((main_row)+(.4*main_row))):
                    self.grid[row][column] = 'c'
                if row == main_row and (column < int((main_row)-(.4*main_row)) or column > int((main_row)+(.4*main_row))):
                    self.grid[row][column] = 'c'


    #returns how much of the population is SIR
    def return_SIR(self):
        _s = 0
        _i = 0
        _r = 0


        total_population = 0

        for row in range(len(self.grid)):
            for column in range(len(self.grid)):
                if self.grid[row][column] == 'i' or self.grid[row][column] == 'i-a':
                    _i += 1
                if self.grid[row][column] == 's' or self.grid[row][column] == 's-I':
                    _s += 1
                if self.grid[row][column] == 'r':
                    _r += 1
                if self.grid[row][column] != 'c':
                    total_population += 1

        s = (_s/total_population) * 100
        i = (_i /total_population) * 100
        r = (_r /total_population) * 100
        return s,i,r


    #completely isolates a given percent of the population
    def completely_isolate_people(self, percent_of_pop):
        totalPop = self.possible_grid_amounts[self.size] ** 2
        number_isolating = totalPop * (percent_of_pop/100)
        infectedCount = 0

        while infectedCount < number_isolating:
            for row in range(len(self.grid)):
                for column in range(len(self.grid)):
                    chance = random.randint(0, 3*percent_of_pop)
                    if chance == 1:
                        self.grid[row][column] = 's-I'
                        infectedCount += 1

    #resets grid and variables back to their regular states
    def reset_grid(self):
        self.time = 0
        self.start_button = False

        self.previously_infected = []
        self.previously_susceptible = []
        self.previously_recovered = []

        for row in range(len(self.grid)):
            for column in range(len(self.grid)):
                self.grid[row][column] = 's'

        self.completely_isolate_people(self.completely_isolated_factor)
        self.reset_button = False

    #starts the grid in a random setup
    def random_start(self):
        for row in range(self.possible_grid_amounts[self.size]):
            for column in range(self.possible_grid_amounts[self.size]):
                if self.grid[row][column] != 's-I':
                    ran = random.randint(1,15)
                    if ran == 1:
                        self.grid[row][column] = 'i'
                    else:
                        self.grid[row][column] = 's'

    #looks at current state of the grid and updates the statuses
    def apply_next(self):

        #callls function to graph with matplotlib
        self.previously_infected, self.previously_susceptible, self.previously_recovered = graph.plot(self.screen, self.grid, self.time/10, self.previously_infected, self.previously_susceptible, self.previously_recovered) #update the graph as everything else gets updated

        time = self.time/10 # converts frames to seconds
        #updates the grid every half second
        if time % .5 == 0:
            for row in range(len(self.grid)):
                for column in range(len(self.grid)):
                    normal_neighbors = [[row, column+1], [row, column-1], [row-1, column], [row+1, column]] #possible 4 neighbor face locations
                    neighbors_contage_count = 0 #number of infected nambers for every cell

                    #looks at all of the cells neighbors (left, right, top, bottom) and counts the number of infected people touching them
                    for i in normal_neighbors:
                        if 0 <= i[0] < len(self.grid) and 0 <= i[1] < len(self.grid):
                            if self.grid[i[0]][i[1]] == 'i' or self.grid[i[0]][i[1]] == 'i-a':
                                neighbors_contage_count += 1
                    # random chance of making someone sick if neighbor is sick
                    if self.grid[row][column] == 's' and neighbors_contage_count >= 1:
                        chances_of_catching = int(self.contage_factor/neighbors_contage_count) #change the number 10 in this case to change how easy it is to catch
                        spread = random.randint(0,chances_of_catching)
                        if spread == 1:
                            symptoms = random.randint(1,4) # there is a one in 4 chance that the person does not show symptoms
                            if symptoms == 2:
                                self.grid[row][column] = 'i-a'
                            else:
                                self.grid[row][column] = 'i'

                    # if cell is sick, there is a random chance of recovery
                    if self.grid[row][column] == 'i' or self.grid[row][column] == 'i-a':
                        chances_of_recovering = random.randint(0,10)
                        if chances_of_recovering == 1:
                            self.grid[row][column] = 'r'


    #displays boxs buttons graphs and charts
    def draw_grid_and_controls(self):
        # Set the screen background
        self.screen.fill((255, 255, 255))

        # draw start/stop button
        if self.start_button == True:
            color = (255, 50, 50)
            text = 'Stop'
        else:
            color = (50, 255, 50)
            text = 'Run'
        pygame.draw.rect(self.screen, color, (self.width + 20, 10, 70, 30))  # draw start/stop
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(text, False, (0, 0, 0))
        self.screen.blit(textsurface, (self.width + 26, 15))

        # draw reset button
        pygame.draw.rect(self.screen, (200, 200, 200), (self.width + 20, 50, 70, 30))  # draw reset
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render("Reset", False, (0, 0, 0))
        self.screen.blit(textsurface, (self.width + 26, 55))

        # draw random start
        pygame.draw.rect(self.screen, (200, 200, 200), (self.width + 10, 90, 90, 30))  # draw random
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render("Random", False, (0, 0, 0))
        self.screen.blit(textsurface, (self.width + 16, 95))

        # change grid size buttons and text
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = myfont.render("Grid Size", False, (0, 0, 0))
        self.screen.blit(textsurface, (self.width + 20, 125))

        myfont = pygame.font.SysFont('Comic Sans MS', 35)
        pygame.draw.rect(self.screen, (200, 200, 200), (self.width + 20, 145, 30, 30))  # draw + box
        textsurface = myfont.render("+", False, (0, 0, 0))
        self.screen.blit(textsurface, (self.width + 28, 145))
        myfont = pygame.font.SysFont('Comic Sans MS', 40)
        pygame.draw.rect(self.screen, (200, 200, 200), (self.width + 55, 145, 30, 30))  # draw - box
        textsurface = myfont.render("-", False, (0, 0, 0))
        self.screen.blit(textsurface, (self.width + 67, 145))

        # draw community button
        pygame.draw.rect(self.screen, (200, 200, 200), (self.width + 5, 180, 110, 30))  # draw reset
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 27)
        textsurface = myfont.render("Community", False, (0, 0, 0))
        self.screen.blit(textsurface, (self.width + 10, 185))

        # contagious factor buttons
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = myfont.render(str(round((1/self.contage_factor)*100, 2)) +"% spread factor", False, (0, 0, 0))
        self.screen.blit(textsurface, (5, self.height + 10))

        myfont = pygame.font.SysFont('Comic Sans MS', 35)
        pygame.draw.rect(self.screen, (200, 200, 200), (45, self.height + 35, 30, 30))  # draw + box
        textsurface = myfont.render("+", False, (0, 0, 0))
        self.screen.blit(textsurface, (53, self.height + 34))
        myfont = pygame.font.SysFont('Comic Sans MS', 43)
        pygame.draw.rect(self.screen, (200, 200, 200), (80, self.height + 35, 30, 30))  # draw - box
        textsurface = myfont.render("-", False, (0, 0, 0))
        self.screen.blit(textsurface, (90, self.height + 32))

        # complete isolation factor buttons
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = myfont.render(str(self.completely_isolated_factor) + "% in complete isolation", False, (0, 0, 0))
        self.screen.blit(textsurface, (200, self.height + 10))

        myfont = pygame.font.SysFont('Comic Sans MS', 35)
        pygame.draw.rect(self.screen, (200, 200, 200), (235, self.height + 35, 30, 30))  # draw + box
        textsurface = myfont.render("+", False, (0, 0, 0))
        self.screen.blit(textsurface, (242, self.height + 34))
        myfont = pygame.font.SysFont('Comic Sans MS', 43)
        pygame.draw.rect(self.screen, (200, 200, 200), (272, self.height + 35, 30, 30))  # draw - box
        textsurface = myfont.render("-", False, (0, 0, 0))
        self.screen.blit(textsurface, (282, self.height + 32))

        #key
        s,i,r = self.return_SIR()

        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = myfont.render("suscepible: " + str(int(s)) + "%", False, (0,0,0))
        self.screen.blit(textsurface, (415, self.height + 10))
        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = myfont.render("infected: " + str(int(i)) + "%", False, (255,0,0))
        self.screen.blit(textsurface, (415, self.height + 30))
        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = myfont.render("recovered: " + str(int(r)) + "%", False, (200,200,200))
        self.screen.blit(textsurface, (415, self.height + 50))


        # Draw the grid
        for row in range(self.possible_grid_amounts[self.size]):
            for column in range(self.possible_grid_amounts[self.size]):

                #if cell is susceptible
                if self.grid[row][column] == 's' or self.grid[row][column] == 's-I':
                    pygame.draw.rect(self.screen, (255, 255, 255), (
                    column * (self.width / self.possible_grid_amounts[self.size]),
                    row * (self.width / self.possible_grid_amounts[self.size]),
                    (self.width / self.possible_grid_amounts[self.size]),
                    (self.width / self.possible_grid_amounts[self.size])))

                #if cell is infected but asymptomatic
                if self.grid[row][column] == 'i-a':
                    pygame.draw.rect(self.screen, (252, 204, 208), (
                    column * (self.width / self.possible_grid_amounts[self.size]),
                    row * (self.width / self.possible_grid_amounts[self.size]),
                    (self.width / self.possible_grid_amounts[self.size]),
                    (self.width / self.possible_grid_amounts[self.size])))

                #if cell is infected
                if self.grid[row][column] == 'i':
                    pygame.draw.rect(self.screen, (255, 0, 0), (
                    column * (self.width / self.possible_grid_amounts[self.size]),
                    row * (self.width / self.possible_grid_amounts[self.size]),
                    (self.width / self.possible_grid_amounts[self.size]),
                    (self.width / self.possible_grid_amounts[self.size])))

                #if cell has recovered
                if self.grid[row][column] == 'r':
                    pygame.draw.rect(self.screen, (200, 200, 200), (
                    column * (self.width / self.possible_grid_amounts[self.size]),
                    row * (self.width / self.possible_grid_amounts[self.size]),
                    (self.width / self.possible_grid_amounts[self.size]),
                    (self.width / self.possible_grid_amounts[self.size])))

                #if cell is community wall
                if self.grid[row][column] == 'c':
                    pygame.draw.rect(self.screen, (0, 0, 0), (
                    column * (self.width / self.possible_grid_amounts[self.size]),
                    row * (self.width / self.possible_grid_amounts[self.size]),
                    (self.width / self.possible_grid_amounts[self.size]),
                    (self.width / self.possible_grid_amounts[self.size])))

                pygame.draw.line(self.screen, (0, 0, 0), (column * (self.width / self.possible_grid_amounts[self.size]),
                                                          row * (self.width / self.possible_grid_amounts[self.size])), (
                                 column * (self.width / self.possible_grid_amounts[self.size]),
                                 self.height))  # draws grid lines x axis
                pygame.draw.line(self.screen, (0, 0, 0),
                                 (0, row * (self.width / self.possible_grid_amounts[self.size])), (self.width, row * (
                                self.width / self.possible_grid_amounts[self.size])))  # draws grid lines y axis

        # adds two additional lines that make the graph look better
        pygame.draw.line(self.screen, (0, 0, 0), (self.width, 0), (self.width, self.height))
        pygame.draw.line(self.screen, (0, 0, 0), (0, self.height - 1), (self.width, self.height - 1))


game = Grid()
game.display()

"""This file handles the graphing of the data live"""
import pygame
import matplotlib as mpl
from matplotlib import style
mpl.use("Agg")
style.use('seaborn-whitegrid')

import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt

# draws the graph when the data is not being updated -> this is used for when the user has not hit run yet or has paused the graphing so the graph
# does not disapear
def plot_dead(screen, data, time, previously_infected, previously_susceptible, previously_recovered):
    infected_cases = previously_infected
    susceptible_cases = previously_susceptible
    recovered_cases = previously_recovered

    fig = plt.figure(figsize=[4, 4], dpi=100)
    ax = fig.add_subplot(111)

    fig.suptitle('Infection Data')
    plt.ylabel('Cases (cells)',labelpad=0)
    plt.xlabel('Time (seconds)',labelpad=3)

    canvas = agg.FigureCanvasAgg(fig)

    sick = []
    time_sick = []
    for i in infected_cases:
        time_sick.append(i[0])
        sick.append(i[1])

    could_get_sick = []
    time_could_get_sick = []
    for i in susceptible_cases:
        time_could_get_sick.append(i[0])
        could_get_sick.append(i[1])

    better = []
    time_better = []
    for i in recovered_cases:
        time_better.append(i[0])
        better.append(i[1])

    # plots data
    ax.plot(time_sick, sick, '-', label='Infected Cases', color='#FF0000')  # infected cases
    ax.plot(time_could_get_sick, could_get_sick, '-', label='Susceptible Cases', color='#c8c8c8')  # susceptible cases
    ax.plot(time_better, better, '-', label='Recovered Cases', color='#000000')  # recovered cases

    # a bunch of drawing commands to display data
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    graph = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(graph, (520, 0))
    pygame.display.flip()

    plt.close('all')


#draws the graph on to the screeen and returns updated total cases data
def plot(screen, data, time, previously_infected, previously_susceptible, previously_recovered):
    infected = 0
    susceptible = 0
    recovered = 0

    #instantiate some plotting commands

    infected_cases = previously_infected
    susceptible_cases = previously_susceptible
    recovered_cases = previously_recovered

    fig = plt.figure(figsize=[4, 4], dpi=100)
    ax = fig.add_subplot(111)
    canvas = agg.FigureCanvasAgg(fig)

    fig.suptitle('Infection Data')
    plt.ylabel('Cases (cells)',labelpad=0)
    plt.xlabel('Time (days)',labelpad=3)

    #updates the data
    for row in range(len(data)):
        for column in range(len(data)):
            if data[row][column] == 'i':
                infected += 1
            if data[row][column] == 's':
                susceptible += 1
            if data[row][column] == 'r':
                recovered += 1

    infected_cases.append([time, infected])
    susceptible_cases.append([time, susceptible])
    recovered_cases.append([time, recovered])

    #prepare data to graph
    sick = []
    time_sick = []
    for i in infected_cases:
        time_sick.append(i[0])
        sick.append(i[1])

    could_get_sick = []
    time_could_get_sick = []
    for i in susceptible_cases:
        time_could_get_sick.append(i[0])
        could_get_sick.append(i[1])

    better = []
    time_better = []
    for i in recovered_cases:
        time_better.append(i[0])
        better.append(i[1])

    # plots data
    ax.plot(time_sick, sick, '-', label='Infected Cases', color='#FF0000')  # infected cases
    ax.plot(time_could_get_sick, could_get_sick, '-', label='Susceptible Cases', color='#c8c8c8')  # susceptible cases
    ax.plot(time_better, better, '-', label='Recovered Cases', color='#000000')  # recovered cases

    # a bunch of drawing commands to display data
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    graph = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(graph, (520, 0))
    pygame.display.flip()

    plt.close('all')

    return infected_cases, susceptible_cases, recovered_cases #returns data back to the main function

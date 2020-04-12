# Virus-Simulator

## Epidemiology: SIR Modeling
---
[Article detailing SIR -> Epidemiology pg. 85](http://greenteapress.com/modsimpy/ModSimPy3.pdf)
#### Methodology: 
* S: People who are “susceptible”, that is, capable of contracting the dis- ease if they come into contact with someone who is infected.
* I: People who are “infectious”, that is, capable of passing along the disease if they come into contact with someone susceptible.
* R: People who are “recovered”. In the basic version of the model, people who have recovered are considered to be immune to reinfection. That is a reasonable model for some diseases, but not for others, so it should be on the list of assumptions to reconsider later.

> This model assumes that the population is closed; that is, no one arrives or departs, so the size of the population, N, is constant.

* the total population = n
* total number of infected people = i 
* the recovery rate Y: if for example 100 people are infectious at a particular point in time, maybe we could expect about 1 out of 4 to recover on any particular day. Therefore the recovery rate is 0.25 per day. 
* recoveries we expect per day is γiN: the total poulation times the number infected time the recovery rate.*
*the contact rate β: if for example each susceptible person comes into contact with 1 person every 3 days (making them infected). 
* population that’s susceptible sN: the fraction of the population thats susceptible 
* number of contacts per day:  βsN
number of those in contact with infected people: βsiN 

SIR models are examples of compartment models, so-called because they divide the world into discrete categories, or compartments, and describe transi- tions from one compartment to another. 

## Code 
---
[Article Detailing Making Grid in Pygame](http://programarcadegames.com/python_examples/f.php?file=array_backed_grid.py)

#### python packages needed:
```python
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib as mpl
import pygame
import random
```
pygame is the base of the gui that handles the button presess, the window, and the chart

matplotlib is used to draw a graph on a canvas and overlay it onto the pygame screen

Within the main Grid() object there is a grid variable that stores a 2-D array with row and column data that represent each cell (person) in the grid (society)

### Each cell can store one of 6 values:
1. s = susceptible -> represented on the grid with any white cell and on the graphed with the black line
2. s-I susceptible in isolation (comes in contact with no one) -> represented by a white cell and graphed with the black line
3. i = infected -> represented as a red cell and on the graph with the red line 
4. i-a = infected but asymptomatic -> represented by pink cell and graphed with the red line
5. r = recovered -> represented by a gray cell and graphed with the gray line
6. c = community wall -> represented by a black cell and not graphed

### Rules:
1. Each generation (one day) is represented by the full iteration of the main while loop 
2. Any indivdual has at most 4 neighbors(if not in corner or against wall or side): Left, Right, Top, Bottom
3. If a cell has a neighbor that is infected there is a certain chance they will be infected controled by the spread factor
4. The more infected neighbors a cell has the more likely it will be to become infected

### Grid Size:
Changing grid size smaller or larger reduces or increases the amount of cells displayed. 

### Reset: 
Reset removes all the cells from the grid, resets several variables including the matplotlib graph.

### Random:
Fills the grid with a random number of infected cases randomly scattared. 

### Add Counties
Adds four quadrants that represent the natural distancing between towns, cities, and communities. This might more accuratly show how the spread is slowed in reality. (this button is only effective in the larger grid sizes)

### Spread Factor
Replicates the effect of how much sick people stay home and how much people social distance. The percentage represends the chances that an infected person infects another person per generation (day). The larger the percent the faster the virus spreads. 

### Complete Isolation
Replicates the barrier formed by complete distancing in society. This is equivelent to a person staying home and not putting themselves at all in contact with anyone or anything contaminated. This acts as a natural barrier to slow the spread and overall damage of the virus. 

#### Data inputed into pygame graph (example):
| Time  | Susceptible  |  
| ----- |:------------:|  
| 0     | 2500         |  
| 1     | 2490         |  
| 2     | 2430         |  

| Time  | Infected     | 
| ----- |:------------:| 
| 0     | 0            | 
| 1     | 10           |  
| 2     | 60           | 

| Time  | Recovered    | 
| ----- |:------------:| 
| 0     | 0            | 
| 1     | 0            |  
| 2     | 10           | 

#### This data was used to plot three lines on the matplotlib graph canvas:
```python
ax.plot(time_sick, sick, '-', label='Infected Cases', color='#FF0000')  # infected cases
ax.plot(time_could_get_sick, could_get_sick, '-', label='Susceptible Cases', color='#c8c8c8')  # susceptible cases
ax.plot(time_better, better, '-', label='Recovered Cases', color='#000000')  # recovered cases
```

### Notes: 
* One drawback of my code was that it did not represent a true mixed society where random social interactions take place every day. My simulation accounts for one person only coming into contact with four people a day (their neighbors) and no one else. For that reason it really only spreads outwards. This could be solved if each person were represented as a moving agent and not a grid locked cell. 

---
 
## Example of GUI when loaded:
![Image Failed to Load](Example_Images/ExampleTwo.png)
## Example with smaller grid and communities turned on:
![Image Failed to Load](Example_Images/ExampleOne.png)
## Example of full sized grid running: 
![Image Failed to Load](Example_Images/ExampleThree.png)

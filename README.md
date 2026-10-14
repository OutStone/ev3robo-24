
Welcome to our code repo for a CVUT robo competiton, here's the link to the task for better accesibility: 
<p align="center">
  <a href='https://robosoutez.fel.cvut.cz/zadani-soutezni-ulohy'>CVUT-FEL robosoutez</a>
</p>

# Our Approach

As the forever changing main topic of this competition has now been chosen a game of domino with the objective being creating the longest line with connecting domino pieces.

our idea is as crazy as always - create a robot with a giant spinning arm which will bring the pieces towards the middle of the map. There, around the centre of a robot, will stand a form designed to stack the pieces into the needed shape.    

# Coding Intro
This whole project is made using micropython and its EV3 micropython library.

<p align="center">
  <a href='https://pybricks.com/ev3-micropython/startinstall.html'>Oficial documentation</a>
</p>

NEVER DELETE FIRST LINE IN MAIN - it loads the micropython
```python
#!/usr/bin/env pybricks-micropython
```

# Code snippets to use later



# Code structure
The movement of the robot is devided into two main parts each of which consists of another 4 sections.  

```python

# part I
sect_i = 1

while sect_i < 5:

  if sect_i % 2:
      # pieces needs to be turned 90deg

  if sect_i == 4:
      # one piece has to be turned 180deg

# part II
sect_i = 1

while sect_i < 5:

  if sect_i % 2==0:
      # pieces needs to be turned 90deg
    

```

a function to move the arm to the next piece
```python

def arm_moving(angle):
    pass

```


# 2025
Third year in a row we are taking up for a robotic competiton with lego Ev3 robots. It may seem, that after previus two attemps we should have a knowledge about everything possible with this robot but thats still a long way to go. The task - which unsuprisingly changed again - was now focused on tetris tiles, which should be assembled in a corner of the map into a compact shape.

In the begging, there was light and an attempt to seriously build a robot which would collect the pieces one by one using lines on the game plan for navigation, which I wasn't able to turn into reality due to technical limitations of our robo-set. Then we gave it a bit of thought and came up with a concept of a CNC maschine going from one end of the game plan to the other while collecting the pieces.

This concept turned out to be not only doable but even quite fast and simple, so it suprised us when we ruin into a problem on the day of the competition - there was a bit more grippy surface (and we were lazy at home and we have forgotten to 3d print the tiles with full fill-in so no the bricks were heavier) which resulted in more drag and a magnificient failure.

<a href='https://robosoutez.fel.cvut.cz/robosoutez-2025-pro-stredoskolske-tymy'> task & results 2025 </a>

# 2024
Another year's here and so is its robo task. The rules for this autumn introduce a grid of collored balls, which we have to sort and then drop to two baskets and the oponents field. Seemingly a simple task, so if you know us then you must come to a conclusion that we will no matter what want to have a 100% score. However, how do we start?
Firstly, we will drive the robot in a spiral to colect all the ping pong balls that we get points for. Secondly, we're gonna collect the rest of the balls and imediatly dump them at the oppents half of the game map.

<p align="center">
  <image src='.\src\map24.jpg' align='center' width='400'/>
</p>
<p align="center">
  here is a quick sketch of the idea
</p>

How do we force the robot to drive in a spiral?
It's simple - you divide the spiral into multiple straight lines, each having a specific way how to drive throught it. The two down-facing green arrows are sections where the robot navigates using a ultrasonic sensor and for the rest he's equiped with a sensor (button) to hug the wall and mechanically follow it.

Out of nowhere, on the day of the competition, we ecountred a courious problem - the color sensor, which we were using to sort the balls, stopped giving any kind of sensible data. As a result, the robot messed up two consecutive runs while we desperately tried to find the cause (in the corridor where we were debugging the error simply wasn't happening). As a last hope, we disconnected the sesor and got rid of sorting the balls, which partly worked (the drop of the balls intp the final basket was too high so a large part of the balls jumped out).

It was a dissapointment but what can one do - we tried our best, had fun and that's what counts.

<a href='https://robosoutez.fel.cvut.cz/robosoutez-2024-pro-stredoskolske-tymy'> task & results 2024 </a>

# 2023
Here lies the absulute begging o our robo-building carrier. My friend randomly stumbled upon a robo-competition organised by the CVUT, which seem fun, so we joined and tried our best. The task was quite simple - __stack the most cubes__ in a colum to get points (also there were some extra points based on the colors of the cubes and such).

Our concept was based on a large robot capable of carrying all 16 cubes (in a tube angled 45degs to the game plane) and then colect the cubes in such order, so that we would have the most points. How have we planned to than drop the collum off in the centre of the map? by slamming into the map border and using this stable point for moving the cube containing tube into upright position.

And the __result__? Night before the competition we discovered that the robot is so large, that it simply cannot turn in the map corners. The *simple fix* cost us about half the eveing and we just prayed that it would work. Sadly, the mechanism using the map border failed and the robot nearly broke to to some miss-happ, so no points this year :( 

<a href='https://robosoutez.fel.cvut.cz/robosoutez-2023-pro-stredoskolske-tymy'> task & results 2023 </a>

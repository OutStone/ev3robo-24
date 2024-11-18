# Intro

This year we, again, signed up for a robotic competiton with lego Ev3 robots. It's already the second time when we take part in this event, so we have some experience and know-how.
Speaking about the competiton, maybe it would be nice to include its name and link there: 
<p align="center">
  <a href='https://robosoutez.fel.cvut.cz/zadani-soutezni-ulohy'>CVUT-FEL robosoutez</a>
</p>

# Main Idea

If you read the rules and you know us then you must come to a conclusion that we will no matter what want to have a 100% rating. So how do we start?
Firstly, we will drive the robot in a spiral to colect all the ping pong balls that we get point for. Secondly, we're gonna collect the rest of the balls and then dump them at the oppents half of the game map.
<p align="center">
  <image src='mapa1.jpg' align='center' width='400'/>
</p>

How do we force the robot to drive in a spiral?
It's simple - you divide the spiral into multiple straight lines, each with it's specific way how to drive throught it.
For the rest of this project I will refer to the spiral segments as game stages. In total tehe will be more than 10 of them, most of which will the robot drive throught by mechanicaly following a wall with kind of a arm. Some other game stages will be passed via keeping a constant distance from a wall with a ultrasonic sensor.

# Coding Intro

This whole project is being made and will be made in micropython whith the use of a EV3 micropython library

<p align="center">
  <a href='https://pybricks.com/ev3-micropython/startinstall.html'>Oficial documentation</a>
</p>

NEVER DELETE FISRT LINE IN MAIN - it loads the micropython
```python
#!/usr/bin/env pybricks-micropython
```

# Code snippets to use later

```python
speaker.say(text)
# how about we use this to get some info trought out the program test runs?
```
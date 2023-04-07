I made this simple pygame demonstration in order to teach myself an intuitive understanding of how PID control systems work. 

The ball will always attempt to move towards your mouse when the mouse button is held down, but its motion is determined by the proportional, integral and derivative components of the error (as defined by the distance between the pointer and the ball).

The proportional term is directly proportional to the error, more error more force. 

The derivative term accounts for the rate at which the ball is approaching the pointer, in order to slow down before arrival. 

The integral term applies force proportional to the accumulated error over time, in case the other two terms can get it "close but not quite there". 

The three forces are then summed together and applied to the ball (plus a bit of gravity to provide some natural movement). They are also displayed as X and Y component vectors coming out from the ball to visually illustrate the forces.

![Screenshot](https://i.imgur.com/4OuDTnK.png)

##How to "Play"

By default, the ball is tuned with arbitrary values to get in the right neighborhood of controllable motion. The numbers I picked are overtuned on P (and/or) undertuned on D, which will result in a very long oscillation around the desired point. 

The goal of the "Game" is to adjust the values using the first 6 function keys to change this lazy, oscillating motion into a motion that "snaps" into place in a satisfying manner. By decreasing P and increasing D, you will achieve a slow, accurate, methodical motion such as desired for applications like robot arms and heating systems. Conversely, by increasing both P and D, you will achieve a very rapid and twitchy motion, such as you'd see in UAV flight controllers or 3d printers. 

You may also notice that the ball snaps into place, but a little bit out of place. This can be remedied by increasing the I term, which will gradually push it into place as the error accumulates.  
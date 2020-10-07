# curtains
Automated curtains

Written in CircuitPython for an ItsyBitsy MO from Adafruit

Overview: 
Non-motorized curtains were bought and I wanted to motorize them. Given their placement, the hand drawn method wasn't applicable. A mechanism was designed to allow a brushless DC motor, driven by a hobby ESC (electronic speed control), to raise the curtains up or down given an input from a pushbutton. 

To control the motor, servo-drive protocol was used: a variable width pulse (1.0ms to 2.0ms) on a 50 Hz frequency. 1.5ms is the mid-point, 1.0ms is full down, 2.0ms is full up.

To control the curtain's position, a hall effect sensor and proximity sensor was used. The hall effect sensor shorted to ground when the magnet was in proximity. The proximity sensor output a low signal when the curtain was in front of it. I used the hall effect sensor to count revolutions (4 mags = 1 rev), which works well for going down. For coming back up, I used the proximity sensor to indicate when to stop and also to reset the hall effect sensor count. 

To initiate movement and direction, two push button switches were used. They were wired to connect to ground when pressed. Pressing down would make the curtain go down, pressing up would make the curtain go up. Pressing either button while the motor was in motion would cause the motor to stop. 

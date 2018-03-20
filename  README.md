# Project: Search and Sample Return
---


**Steps of this project are the following:**  

## Data Analysis In Notebook

* Download the simulator and take data in "Training Mode"
* Take some Pictures to do some experiments on them (example for a View containing rock or an empty View just to determine the color Threshold that should be done for each of them
* Example Pictures :


![alt text][image2]
![alt text][image3]

**Do the Precpetion Step**
First of all we identify four Points from the Rover.Camera (img) to do the ***Perspective Transform***
([[14, 140], [301 ,140],[200, 96], [118, 96]]) and 
![alt text][image4]
Then we Apply Color-Thresholding to identify  ***Navigable Terrains, Rocks And Obstacles***
Here i used 3 Functions that take Binary Image and return an Array has selected Area (x,y) as 1 and not as 0 

![alt text][image5]

****Coordinate Transformations:****
as they predefined the ***Functions*** `rover_coords(), pix_to_world() and to_polar_coords()`
convert Binary Images Which contain Coordinates of (Terrain , Rocks , Obstacles) from Center Image to the ***Robot Coordinates, World Coordinates and polar Coordinates***
then we make new 3-Channel Visi Image for (Terrain , Rocks , Obstacles) Coordinates in respecting World Map Coordinates and after that we add this image to world Map to updae it 


* Fill in the `perception_step()` function within the `perception.py` script with the 

[//]: # (Image References)


[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 
[image4]: ./misc/wrap.png
[image5]: ./misc/color.png 

## Autonomous Mode :
#### Drive.py:
To identify Rocks while Rover is driving we add new Attributes to Rover Object in Drive.py
`self.rocks_angles` `self.rocks_angles`
#### Perception Step:
in Perception Step we use the Functions from The notebook changeing the source of data which was Data in the notebook to Rover Object in this step
we update `Rover.rocks_angles` and `Rover.rocks_angles` with the Coordinates of the rock in Rover Coordinates after converting thim with the function `rover_coords()`
#### Decision:
First of all the Rover should check if the Vision Image contains some rocks which stored in chanell 1 if so the it should direct himself to the rock and go forword (still doesn't work by me i have tried but still doesn't work )
if no then he should drive noramlly 
therefor i have added for Rover Object the Attribute Heading (heading to rocks)
all other Functions are well described in the Code and exist by default
##### Getting Stucked :
i have added the follwing Attributes :
```
Rover.stuck_counter = 0
Rover.stuck_wait_frames = 104
Rover.is_stuck = False
```
The Stuck_counter starts counting when the speed is below < 0.2 if it reachs 104 (whichs means almost 4 seconds ) in the same speed then that means the Rover is Stucked 



#### Vedio:

attached
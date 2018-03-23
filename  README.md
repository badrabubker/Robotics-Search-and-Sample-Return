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
***Perspective Transform*** :
The `perspect_transform` function turns a Rover perspective image to a top-down view.
```python
def perspect_transform(img, src, dst):  
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
    return warped 
```
 we identify four Points from the Rover.Camera (img) to do the ***Perspective Transform***
 from this :  
 
![alt text][image2]  
 
 to this :  
 
![alt text][image4]  

which are :
([[14, 140], [301 ,140],[200, 96], [118, 96]]) and Then we Apply Color-Thresholding to identify  ***Navigable Terrains, Rocks And Obstacles***
***Color-Thresholding***
The `color_thresh` function will return a binary image where it is 1 when that pixel color value in the img is above the given RGB threshold, if above parameter is set to True.
Here i used 3 Functions that take Binary Image and return an Array has selected Area (x,y) as 1 and not as 0 
```python
def color_thresh(img, rgb_thresh=(160, 160, 160)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] > rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select
```
![alt text][image5]

****Coordinate Transformations:****
as they predefined the ***Functions*** `rover_coords(), pix_to_world() and to_polar_coords()`
convert Binary Images Which contain Coordinates of (Terrain , Rocks , Obstacles) from Center Image to the ***Robot Coordinates, World Coordinates and polar Coordinates***
```python
def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    x_pixel = -(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[1]/2 ).astype(np.float)
    return x_pixel, y_pixel


# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# Define a function to map rover space pixels to world space
def rotate_pix(xpix, ypix, yaw):
    # Convert yaw to radians
    yaw_rad = yaw * np.pi / 180
    xpix_rotated = (xpix * np.cos(yaw_rad)) - (ypix * np.sin(yaw_rad))
                            
    ypix_rotated = (xpix * np.sin(yaw_rad)) + (ypix * np.cos(yaw_rad))
    # Return the result  
    return xpix_rotated, ypix_rotated

def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale): 
    # Apply a scaling and a translation
    xpix_translated = (xpix_rot / scale) + xpos
    ypix_translated = (ypix_rot / scale) + ypos
    # Return the result  
    return xpix_translated, ypix_translated


# Define a function to apply rotation and translation (and clipping)
# Once you define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    # Apply rotation
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # Apply translation
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # Perform rotation, translation and clipping all at once
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    # Return the result
    return x_pix_world, y_pix_world
```
then we make new 3-Channel Visi Image for (Terrain , Rocks , Obstacles) Coordinates in respecting World Map Coordinates and after that we add this image to world Map to updae it 


[//]: # (Image References)


[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 
[image4]: ./misc/wrap.png
[image5]: ./misc/color.png 
[image6]: ./screen_shot.png 

## Autonomous Mode :
#### Drive.py:
To identify Rocks while Rover is driving we add new Attributes to Rover Object in Drive.py
`self.rocks_angles` 
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


### SceenShot:

![alt text][image6]

#### Vedio:
attached 

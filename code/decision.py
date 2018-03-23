import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):
    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # First Always checks if the Rover near an Object
    if Rover.near_sample and not Rover.picking_up:
        Rover.is_stuck = False
        Rover.stuck_counter = 0
        Rover.send_pickup = True
        Rover.heading = False # set The Heading(heading to rock) variable to false when done picking up the rock
    #### Picking up Rocks still doesnt work that's why is being commented #####
    #if len(Rover.rocks_angles) != 0: # when we have rocks in our vesion Image 
    #     rock_angel = np.clip(np.median(Rover.rocks_angles * 180/np.pi), -15, 15) #we calculate the middle Angle to head to 
    #     if Rover.heading == False : # if we have angle but The Rover is not heading to rock
    #         if Rover.mode == 'forward': #if its moving 
    #             if (rock_angel < 0.5 and rock_angel > -0.5): # if the rock within the Rang then trun on the heading mode
    #                 Rover.heading = True
    #             else : # if the rock is not in this range then stop in in stop mode the rover will stear and head again to the Rock
    #                 Rover.throttle = 0
    #                 Rover.steer = 0
    #                 Rover.heading = True
    #                 Rover.mode = 'stop'
    #     else:
    #         if Rover.mode == 'forward': # if heading mode is acivated then keep movin until rech the rock
    #             if Rover.vel < Rover.max_vel:
    #                 Rover.throttle = Rover.throttle_set
    #             else:
    #                 Rover.throttle = 0
    #         else: # if not moving  and heading is true then we should stear and mocve 
    #             if Rover.vel > 0.2:
    #                 Rover.brake = Rover.brake_set
    #                 Rover.throttle = 0
    #                 Rover.steer = 0
    #             # If we're not moving (vel < 0.2) then do something else
    #             elif Rover.vel <= 0.2:
    #                 Rover.brake = 0
    #                 # Set steer to rock angle
    #                 Rover.steer = -rock_angel 
    #                 Rover.mode = 'forward'         

    # # Example:
    # # Check if we have vision data to make decisions with
    #else:
    #    Rover.heading = False
    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'
            #to check whether the Rover stuck or not we create a counter depends on the number of the frames
            # if Rover is moving with a very little speed and Stuck variable is false 
            if Rover.vel <= 0.2 and Rover.vel >= -0.2 and not Rover.is_stuck:
                # we increase the stuck counter by one 
                Rover.stuck_counter += 1
                # if stuck counter reaches 4 sec (104 frames) then set rover stuck to true 
                if Rover.stuck_counter  >= Rover.stuck_wait_frames:
                    Rover.is_stuck = True
            # on the other hand when is stuck is true and and brake or throttle are not 0
            # and the Rover is moving with speed 
            # this means the Rover is not stuck anymore so we set it to false and reset the counter       
            # and we stear like normal 
            elif Rover.is_stuck and (Rover.throttle != 0 or Rover.brake != 0):
                if Rover.vel >= 0.5 or Rover.vel <= -0.5:
                    Rover.stuck_counter = 0
                    Rover.is_stuck = False
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                else:
                # if Rover stuck and has little speed then it's stuck we should do some stearing and moving
                # brake, reverse the movment and reset stearing 
                    Rover.brake = 0
                    Rover.throttle = -Rover.throttle_set
                    Rover.steer = 0
                    # to stear :
                    # now Rover is moving the backwards and 
                    #the numer  condtion (Rover.stuck_counter // Rover.stuck_wait_frames) % 2 == 0 will
                    # br first True when The Robot is stuck since time equles to stuck_wait_frames 
                    # which means by us (8 secs(108 frames)) and eventually it has being moving 
                    #backwords since 4 secs (104 frames) if this this condtion is true the we stear The rover
                    # -Rover.steer + 5 which chane the stear to git him out of being stuck
                    if (Rover.stuck_counter // Rover.stuck_wait_frames) % 2 == 0:
                        Rover.steer = np.clip(-(Rover.steer + 5), -15, 15)
                    #the numer  condtion (Rover.stuck_counter // Rover.stuck_wait_frames) % 5 == 0 will
                    # br first True when The Robot is stuck since time equles to stuck_wait_frames * 5 
                    # and eventually it has being moving backwords since 20 secs (520 frames)
                    # and stearing since 16 sec (416 frames)
                    # if this this condtion is true we stop going backwords 
                    if (Rover.stuck_counter // Rover.stuck_wait_frames) % 5 == 0:
                        Rover.throttle = 0
                    # and after another Rover.stuck_wait_frames (104 frames) we set the throttle
                    # to throttle setting 
                    if (Rover.stuck_counter // Rover.stuck_wait_frames) % 6 == 0:
                        Rover.throttle = Rover.throttle_set
                    #### The Rover could just quit of being stucked after he drove backwards then 
                    # he doesnt need to stear and these inntsruction will not being excuted because we went out 
                    # of the condetion (Rover is not sucked anymore)
            else:
                Rover.is_stuck = False
                Rover.stuck_counter = 0

           

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0   
    return Rover


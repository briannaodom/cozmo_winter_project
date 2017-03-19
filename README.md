cozmo\_winter\_project 
====================

![Meet Cozmo, The Ultimate Follower!](https://s.aolcdn.com/hss/storage/midas/fe249551d88d3ce0c86c7bb0573b9820/204057074/Anki+Cozmo+Still2.jpg)

#### Objective:

Use [Cozmo](https://anki.com/en-us/cozmo), a mini toy robot created by the company [ANKI] based in California, to follow an ar tag attached to the back of an RC car.
=======


#### Goals for Cozmo: 

1. Maintain the appropriate distance and speed for Cozmo to follow the RC car. 
2. Handle the case where Cozmo loses vision of the ar tag.
3. Have cozmo account for changes in direction and speed of the RC car.

#### Materials Needed:
1. Cozmo, which can be bought on [Amazon](https://www.amazon.com/Anki-000-00048-Cozmo/dp/B01GA1298S)
2. RC Car, which also can be bought on [Amazon](https://www.amazon.com/RW-Lamborghini-Veneno-Remote-Control/dp/B01A5NZAE2/ref=sr_1_5?s=toys-and-games&ie=UTF8&qid=1489929175&sr=1-5&keywords=RC+car)
3. 6 double A batteries
4. Several [ar tags] printed out which can be created with [ar_track_alvar](http://wiki.ros.org/ar_track_alvar)
5. An android or apple device to connect to connect to Cozmo and run the Cozmo app for his SDK. The installation setup can be found [here](http://cozmosdk.anki.com/docs/initial.html)
6. A usb to connect Cozmo to an apple or android device


#### ROS/Python Packages Needed
1. [Python3.5](http://cozmosdk.anki.com/docs/install-linux.html) as Cozmo's SDK will not work with any other version released prior to python3.5
2. [Pip](http://cozmosdk.anki.com/docs/install-linux.html)
3. [Tkinter](http://cozmosdk.anki.com/docs/install-linux.html) used to view Cozmo's images
4. [ROS Indigo](http://wiki.ros.org/indigo/Installation) or [ROS Kinetic](http://wiki.ros.org/kinetic/Installation) as they are known to work
5. _ar_track_alvar_ to subscribe to the positions of the ar tags

## Steps

### Note: Cozmo must be hooked up to the Cozmo app, connected to wifi, and running the SDK in order to do any of the following.

#### Camera Calibration

Each Cozmo bought has a camera that by default, is calibrated at the manufacturer.
Thus, it is best to calibrate Cozmo's camera by following the appropritate steps found at [ROS.org](http://www.ros.org/)'s [How to calibrate a Monocular Camera](http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration) page.

The easiest way to calibrate Cozmo would be to run [Cozmo.launch](https://github.com/briannaodom/cozmo_winter_project/blob/master/src/cozmo.launch) which will run the [cozmo_driver](https://github.com/OTL/cozmo_driver/blob/master/nodes/cozmo_driver.py) node. From this, Cozmo's camera will be publishing out raw image data. 

To start calibration example:

```rosrun camera_calibration cameracalibrator.py --size  8x6 --square 0.108 image:=/cozmo_camera/image camera:=/cozmo_camera```

If the above example gives an error, check that the Cozmo's camera info is being published with
```rostopic list``` or ```rostopic echo /cozmo_camera/image```

Note: The number of (m-1)x(n-1) squares and size of each square (in mm) will depend on the checkboard used.

#### AR Tag Tracking

In order to subscribe from _ar_track_alvar_ topic, the marker size, new marker error, track error, camera image and info topics and output frame need to be defined. A good description on how to assign the first three arguments can be found on ar_track_alvar [site](http://wiki.ros.org/ar_track_alvar). The latter three arguments, can be defined as below:

1. The camera image should be defined as ```cozmo_camera/image```
2. The camera info should be defined as ```cozmo_camera/camera_info```
3. The output frame should be defined as ```cozmo_camera```

The above can be viewed in the [cozmo.launch](https://github.com/briannaodom/cozmo_winter_project/blob/master/src/cozmo.launch) file.

After defining these arguments, _ar_track_alvar_ will publish out marker data which can be looked at by looked at through running
```rostopic echo /ar_pose_marker```

When a marker is placed in front of Cozmo's camera, the pose data should change due to the marker changing position relative to Cozmo's camera. 

#### Ar_tag_tracking.py Node

The [follow.py]() node will be used to give each marker their own unique [frame_id](http://docs.ros.org/fuerte/api/std_msgs/html/msg/Header.html) and used to receive the [poses](http://docs.ros.org/jade/api/geometry_msgs/html/msg/Pose.html) of the marker's in the cartesian plane. 

This data will be published as tag_position and be used by the following Follow.py node to determine how Cozmo will react to the changes in the RC car's position based on Cozmo's distance from the ar tag. 

#### Follow.py Node

The [follow.py] node subscribes from the tag_position topic being published by the _ar_tag_tracking.py_ node and calculates the distance from the tag and turns this into the velocity Cozmo should be moving in the x direction. If the distance between Cozmo and the RC car, gets closer to 0, Cozmo will slow down, and if the distance increases between them, he will speed up. Also, if the distance becomes negative this means the RC car is reversing, thus Cozmo should back up as well. 

Also, a PID controller is being created to account for error in Cozmo's movements in relation to the ar tag. This PID value will be calculated in the calc_PID function and then be used in the   
cozmo_follow function to decrease the amount of error in his movement. For instance, we can use the integral term to decrease the amount of oscillation or pausing in each cycle between Cozmo and the RC car as he continuously calculates new velocities.

#### Sources For PID Explanations and Implementation

1. A [blog post](http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/) written on the [brettbeauregard](http://brettbeauregard.com/blog/) project blog's site gives a good basis in understanding PID and implementing it, even though the code is written for 
an arduino and the the PID is for basic line following. 

2. [![](https://i.ytimg.com/vi/4Y7zG48uHRo/maxresdefault.jpg)](https://www.youtube.com/watch?v=4Y7zG48uHRo) Click the image above to watch a video that provides visual footage using a small scaled car-like device to help understand how the proportional, integral, and derivative gains will work individually and in unison to align and adjust Cozmo's position in relation to the RC car. 

#### Cozmo_driver.py Node

The [cozmo_driver.py] node written by Takashi Ogura, integrates ROS and Cozmo to publish out various topics such as odometry and imu as well as subscribe from various topics to increase the functionality of Cozmo and allow programmers to execute different programs that would be otherwise hard to implement as Cozmo has its own SDK and was built with only python in mind. 

I added a twist subscriber that subscribes from the cmd_vel topic being published from the _follow.py_ node. This takes the calculated velocities and publishes them to the drive_straight function. Cozmo will drive 150 mm and in that time try to follow the ar tag.

#### To Dos

1. Finish the PID controller
2. Figure out the proper equations to use for Cozmo's linear velocity in the x and y directions 
3. Figure out the proper equation to use for Cozmo's rotational velocity around the z axis
4. Use in the _twist_callback function written in the _cozmo_driver_ node instead of the drive_straight function possibly by assigning the distance Cozmo should travel
5. Account for Cozmo's behavior if he loses sight of the ar tag


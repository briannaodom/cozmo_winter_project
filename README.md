cozmo\_winter\_project 
====================
<img src="https://s.aolcdn.com/hss/storage/midas/fe249551d88d3ce0c86c7bb0573b9820/204057074/Anki+Cozmo+Still2.jpg" alt="Meet Cozmo, the ultimate follower!" style="width: 10px;"/>


#### Objective:

Use [Cozmo](https://anki.com/en-us/cozmo) a mini toy robot created by the company [ANKI] based in California to follow an ar tag attached to the back of an RC car.

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
1. [Python3] as Cozmo's SDK will not work with any other version released prior to python3
2. [ROS Indigo] or [ROS Kinetic] as they are known to work
3. [ar_track_alvar] to subscribe to the positions of the ar tags

## Steps

#### Camera Calibration

Each Cozmo bought has a camera that by default, is calibrated at the manufacturer.
Thus, it is best to calibrate Cozmo's camera by following the appropritate steps found at [ROS.org](http://www.ros.org/)'s [How to calibrate a Monocular Camera](http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration) page.

The easiest way to calibrate Cozmo would be to run [cozmo.launch](https://github.com/briannaodom/cozmo_winter_project/blob/master/src/cozmo.launch) which will run the [cozmo_driver](https://github.com/OTL/cozmo_driver/blob/master/nodes/cozmo_driver.py) node. From this, Cozmo's camera will be publishing out raw image data. 

To start calibration example:
```rosrun camera_calibration cameracalibrator.py --size  8x6 --square 0.108 image:=/cozmo_camera/image camera:=/cozmo_camera```

If the above example gives an error, check that the Cozmo's camera info is being published
```rostopic list``` or ```rostopic echo /cozmo_camera/image```

Note: The number of (m-1)x(n-1) squares and size of each square (in mm) will depend on the checkboard used.

#### AR Tag Tracking

In order to subscribe from ar_track_alvar topic, the marker size, new marker error, track error, camera image and info topics and output frame need to be defined. A good description on how to assign the first three arguments can be found on ar_track_alvar [site](http://wiki.ros.org/ar_track_alvar). The latter three arguments, can be defined as below:

1. The camera image should be defined as ```cozmo_camera/image```
2. The camera info should be defined as ```cozmo_camera/camera_info```
3. The output frame should be defined as ```cozmo_camera```

The above can be viewed in the [cozmo.launch](https://github.com/briannaodom/cozmo_winter_project/blob/master/src/cozmo.launch) file.

After defining these arguments, ar_track_alvar will publish out marker data which can be looked at by looked at through running
```rostopic echo /ar_pose_marker```

When a marker is placed in front of cozmo's camera, this data should change relative to location of the marker and cozmo's camera.

#### Ar_tag_tracking.py Node

The [follow node]() will be used to give each marker their own unique [frame_id](http://docs.ros.org/fuerte/api/std_msgs/html/msg/Header.html) and used to receive the [poses](http://docs.ros.org/jade/api/geometry_msgs/html/msg/Pose.html) of the marker's in the cartesian plane. 

This data will be published as tag_position and be used by the following Follow.py node to determine how Cozmo will react to the changes in the RC car's position based it's distance from the ar tag. 


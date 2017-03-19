cozmo\_winter\_project
====================

#### Objective:

Use [Cozmo](https://anki.com/en-us/cozmo) a mini toy robot created by the company [ANKI] based in California to follow an ar tag attached to the back of an RC car.

#### Goals for Cozmo: 

*Maintain the appropriate distance and speed for Cozmo to follow the RC car. 
*Handle the case where Cozmo loses vision of the ar tag.
*Have cozmo account for changes in direction and speed of the RC car.

#### Materials Needed:
1. Cozmo, which can be bought on [Amazon](https://www.amazon.com/Anki-000-00048-Cozmo/dp/B01GA1298S)
2. RC Car- the one I used from [Amazon](https://www.amazon.com/RW-Lamborghini-Veneno-Remote-Control/dp/B01A5NZAE2/ref=sr_1_5?s=toys-and-games&ie=UTF8&qid=1489929175&sr=1-5&keywords=RC+car)
3. 6 double A batteries
4. Several [ar tags] printed out which can be created with [ar_track_alvar](http://wiki.ros.org/ar_track_alvar)
5. An android or apple device to connect to run the Cozmo app for his SDK- [Installation Setup](http://cozmosdk.anki.com/docs/initial.html)
6. A usb to connect Cozmo to the apple or andoid device


#### ROS/Python Packages Needed
1. [Python3] as Cozmo's SDK will not work with any other version released prior to python3
2. [ar_track_alvar] to subscribe to the positions of the ar tags

## Steps

#### Camera Calibration

Each Cozmo bought has a camera that by default, is calibrated at the manufacturer.
Thus, it is best to calibrate Cozmo's camera by following the appropritate steps found at [ROS.org](http://www.ros.org/)'s [How to calibrate a Monocular Camera](http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration) page.

The easiest way would be to run [cozmo.launch](https://github.com/briannaodom/cozmo_winter_project/blob/master/src/cozmo.launch) 

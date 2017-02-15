#!/usr/bin/env python3

import cozmo
import asyncio
import rospy
from std_msgs.msg import ColorRGBA
from sensor_msgs.msg import Image


def cozmo_image():

    camera_image = cozmo.camera.latest_image
    if camera_image is not None:
        image = camera_image
        i = Image()
        i.encoding = 'rgb8'
        i.width = image.size[0]
        i.height = image.size[1]
        i.step = 3 * i.width
        i.data = image.tobytes()
        i.header.frame_id = 'cozmo_camera'
        cozmo_time = camera_image.image_recv_time
        i.header.stamp = rospy.Time.from_sec(cozmo_time)

        cozmo_image_pub.publish(i)


def run(cozmo_conn):
    cozmo = cozmo_conn.wait_for_robot()
    cozmo.camera.image_stream_enabled = True
    rospy.spin()

if __name__ == '__main__':

    try:
        cozmo_image_pub = rospy.Publisher('camera_image', Image, queue_size=1)

        rospy.init_node('cozmo_camera_image')

        #cozmo.connect(run)

        cozmo.connect_with_tkviewer(run)

    except rospy.ROSInterruptException:

        pass

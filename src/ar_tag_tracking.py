#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32, Header
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image, Range
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker


def ar_tag_track(data):
    for AlvarMarker in data.markers:
        movement_type = AlvarMarker.id
        if movement_type == 0:
            return
        else:
            if movement_type == 3:
                Header.frame_id = 'follow'

            elif movement_type == 4:
                Header.frame_id = 'stop'

        m.pos.x = AlvarMarker.PoseStamped.pose.point.x
        m.pos.y = AlvarMarker.PoseStamped.pose.point.y
        m.pos.z = AlvarMarker.PoseStamped.pose.point.z

        print m.pos.x, m.pos.y, m.pos.z

        ar_tag_pub.publish(m.pos.x, m.pos.y, m.pos.z)

        return

if __name__ == '__main__':
    try:
        rospy.init_node('ar_tag_tracking.py')

        rospy.Subscriber("/webcam_driver/image_raw", Image, )
        rospy.Subscriber("/ar_pose_marker", AlvarMarkers, ar_tag_track)

        ar_tag_pub = rospy.Publisher('tag_position', PointStamped, queue_size=1)

        except rospy.ROSInterruptException:
            pass

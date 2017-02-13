#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import PointStamped
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker


def ar_tag_track(data):
    p = PointStamped()
    for m in data.markers:
        movement_type = m.id
        if movement_type == 0:
            return
        else:
            if movement_type == 3:
                p.header.frame_id = 'follow'

            elif movement_type == 4:
                p.header.frame_id = 'stop'

        p.position.x = m.pose.pose.point.x
        p.position.y = m.pose.pose.point.y
        p.position.z = m.pose.pose.point.z

        print p

        ar_tag_pub.publish(p)

        return

if __name__ == '__main__':
    try:
        rospy.init_node('ar_tag_tracking')

        rospy.Subscriber("/ar_pose_marker", AlvarMarkers, ar_tag_track)

        ar_tag_pub = rospy.Publisher('tag_position', PointStamped, queue_size=1)

        rospy.spin()

    except rospy.ROSInterruptException:
        pass

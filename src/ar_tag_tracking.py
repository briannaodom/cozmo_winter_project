#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped
from ar_track_alvar_msgs.msg import AlvarMarkers


def ar_tag_track(marker_info):
    p = PointStamped()
    for m in marker_info.markers:
        movement_type = m.id
        if movement_type == 0:
            return
        else:
            if movement_type == 3333:
                p.header.frame_id = 'follow'

            elif movement_type == 4444:
                p.header.frame_id = 'follow'

            elif movement_type == 5555:
                p.header.frame_id = 'stop'

        p.point.x = m.pose.pose.position.x
        p.point.y = m.pose.pose.position.y
        p.point.z = m.pose.pose.position.z
        ar_tag_pub.publish(p)

    return p


if __name__ == '__main__':
    try:
        rospy.init_node('ar_tag_tracking')

        rospy.Subscriber("/ar_pose_marker", AlvarMarkers, ar_tag_track)

        ar_tag_pub = rospy.Publisher('tag_position', PointStamped, queue_size=1)

        rospy.spin()

    except rospy.ROSInterruptException:
        pass

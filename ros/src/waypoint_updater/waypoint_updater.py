#!/usr/bin/env python

import math
import numpy as np
import rospy
from std_msgs.msg import Int32
from styx_msgs.msg import Lane, Waypoint
from scipy.spatial import KDTree
from geometry_msgs.msg import PoseStamped
import math

'''
This node will publish waypoints from the car's current position to some `x` distance ahead.

As mentioned in the doc, you should ideally first implement a version which does not care
about traffic lights or obstacles.

Once you have created dbw_node, you will update this node to use the status of traffic lights too.

Please note that our simulator also provides the exact location of traffic lights and their
current status in `/vehicle/traffic_lights` message. You can use this message to build this node
as well as to verify your TL classifier.

TODO (for Yousuf and Aaron): Stopline location for each traffic light.
'''

LOOKAHEAD_WPS = 200 # Number of waypoints we will publish. You can change this number
MAX_DECEL = 0.5

class WaypointUpdater(object):
    def __init__(self):
        rospy.init_node('waypoint_updater')

        self.stopline_wp_idx = -1

        # TODO: Add a subscriber for /traffic_waypoint and /obstacle_waypoint below


        self.base_waypoints = None
        self.pose = None
        self.waypoints_2d = None
        self.waypoint_tree = None





        rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)
        rospy.Subscriber('/traffic_waypoint', Int32, self.traffic_cb)
        rospy.Subscriber('/obstacle_waypoint', Int32, self.obstacle_cb)


        self.final_waypoints_pub = rospy.Publisher('final_waypoints', Lane, queue_size=1)
        rospy.loginfo('ini t loop')
        # TODO: Add other member variables you need below

        self.loop()

    # from lesso 6 of capstone project
    def loop(self):


        rate = rospy.Rate(10)
        print('loop')
        rospy.loginfo('loop')
        while not rospy.is_shutdown():
            #rospy.info('test loop')
            rospy.loginfo('pose '+str(self.pose))
            #rospy.loginfo('pose '+str(self.base_waypoints))
            if self.pose and self.base_waypoints:
                rospy.loginfo('publish')
                self.publish_waypoints()
            rate.sleep()




    def publish_waypoints(self):
        lane = self.generate_lane()

        #closest_idx = self.get_closest_waypoint_idx()

        #if closest_idx is not None:

        #	lane.header=self.base_waypoints.header

        # 	lane.waypoints=self.base_waypoints.waypoints[closest_idx:closest_idx + LOOKAHEAD_WPS]


        self.final_waypoints_pub.publish(lane)



    def generate_lane(self):
        print('generate_lane')
        rospy.loginfo('generate_lane')
        lane = Lane()
        closest_idx = self.get_closest_waypoint_idx()

        base_waypoints = self.base_waypoints.waypoints[closest_idx:closest_idx + LOOKAHEAD_WPS]
        if self.stopline_wp_idx == -1 or (self.stopline_wp_idx >= closest_idx + LOOKAHEAD_WPS):
            rospy.loginfo('acelerate')
            lane.waypoints = base_waypoints
        else:
            lane.waypoints = self.decelerate_waypoints(base_waypoints, closest_idx)
        return lane


    def decelerate_waypoints(self, waypoints, closest_idx):
        rospy.loginfo('desacelerate')
        temp = []
        for i, wp in enumerate(waypoints):
            p = Waypoint()
            p.pose = wp.pose
            stop_idx = max(self.stopline_wp_idx - closest_idx - 2, 0) # Two waypoints before so front of car is behind line
            dist = self.distance(waypoints, i, stop_idx)
            vel = math.sqrt(2 * MAX_DECEL * dist)
            if vel < 1.:
                vel = 0.
            p.twist.twist.linear.x = min(vel, wp.twist.twist.linear.x)
            temp.append(p)
        return temp



    def get_closest_waypoint_idx(self):
        x = self.pose.pose.position.x
        y = self.pose.pose.position.y

        if self.waypoint_tree is not None:
        	closest_idx = self.waypoint_tree.query([x, y], 1)[1]

        	# Check if closest is ahead or behind vehicle
        	closest_coord = self.waypoints_2d[closest_idx]
        	prev_coord = self.waypoints_2d[closest_idx - 1]

        	# Equation for hyperplane through closest_coords
        	cl_vect = np.array(closest_coord)
        	prev_vect = np.array(prev_coord)
        	pos_vect = np.array([x, y])

        	val = np.dot(cl_vect - prev_vect, pos_vect - cl_vect)

        	if val > 0:
            		closest_idx = (closest_idx + 1) % len(self.waypoints_2d)

        	return closest_idx
        else:
                return None

    def pose_cb(self, msg):
        # TODO: Implement
        self.pose=msg

    def waypoints_cb(self, waypoints):
        # TODO: Implement

        self.base_waypoints = waypoints
        if not self.waypoints_2d:
                self.waypoints_2d = [[waypoint.pose.pose.position.x, waypoint.pose.pose.position.y] for waypoint in
                                 waypoints.waypoints]
                self.waypoint_tree = KDTree(self.waypoints_2d)

    def traffic_cb(self, msg):
         rospy.loginfo('traffic waypoint')
         if self.stopline_wp_idx != msg.data:
            rospy.logwarn(
                "LIGHT: new stopline_wp_idx={}, old stopline_wp_idx={}".format(msg.data, self.stopline_wp_idx))
            self.stopline_wp_idx = msg.data

    def obstacle_cb(self, msg):
        # TODO: Callback for /obstacle_waypoint message. We will implement it later
        pass

    def get_waypoint_velocity(self, waypoint):
        return waypoint.twist.twist.linear.x



    def set_waypoint_velocity(self, waypoints, waypoint, velocity):
        waypoints[waypoint].twist.twist.linear.x = velocity

    def distance(self, waypoints, wp1, wp2):
        dist = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
        for i in range(wp1, wp2+1):
            dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
            wp1 = i
        return dist


if __name__ == '__main__':
    try:
        WaypointUpdater()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start waypoint updater node.')

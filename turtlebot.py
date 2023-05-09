#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib import SimpleActionClient
from geometry_msgs.msg import PoseWithCovarianceStamped



class locationRecorder:
    def __init__(self):
        rospy.init_node('location_recorder')
        self.position_sub = rospy.Subscriber('/amcl_pose',PoseWithCovarianceStamped , self.record_position)
        self.positions = []

    def record_position(self, odom):
        position = odom.pose.pose.position
        self.positions.append((position.x, position.y))

class turtlebotNavigator:
    def __init__(self):
        self.client = SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()
        self.route = []

    def navigate_to_goal(self, goal):
        self.client.send_goal(goal)
        self.client.wait_for_result()
        rospy.loginfo("Hedefe varildi !")


        
    def navigate_to_position(self, position):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.pose.position.x = position[0]
        goal.target_pose.pose.position.y = position[1]
        goal.target_pose.pose.orientation.w = 1.0
        self.navigate_to_goal(goal)

    def save_route(self):
        self.route = self.route + recorder.positions[::-1]

    def go_back(self):
        for position in self.route[::-1]:
            self.navigate_to_position(position)
            rospy.loginfo("mission is completed")
        
        self.client.cancel_all_goals() 
        rospy.signal_shutdown("mission is completed!!!")



if __name__ == '__main__':
    try:
        recorder = locationRecorder()
        navigator = turtlebotNavigator()

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.pose.position.x = 1.3
        goal.target_pose.pose.position.y = -1.7
        goal.target_pose.pose.orientation.w = 1.0

        navigator.navigate_to_goal(goal)
        navigator.save_route()
        print("---------------------")
        
        navigator.go_back()
        

    except rospy.ROSInterruptException:
        pass
   
    



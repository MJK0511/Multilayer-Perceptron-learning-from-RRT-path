#!/usr/bin/env python3
import rospy
from moveit_commander import RobotCommander, MoveGroupCommander

rospy.init_node("xArm6")
robot = RobotCommander()
xarm = MoveGroupCommander("xarm6")

# ゴール
fixed_joint_values = [1.0031064240644607, 0.740823053049743, -2.0603816587531423, -0.0001051592687124625, 1.3187745130631479, 1.0020974406663496] 
xarm.set_start_state_to_current_state()
xarm.set_joint_value_target(fixed_joint_values)

# プランニング
plan = xarm.plan()
print(plan)
xarm.go()
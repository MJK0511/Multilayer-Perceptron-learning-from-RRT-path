import os
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import csv

rospy.init_node('xArm6')

file_path = '/home/nishidalab07/github/6dimension/simulation1/Configuration/After_train/allpath/path_4.txt'

joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']

client = actionlib.SimpleActionClient('/xarm/xarm6_traj_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
client.wait_for_server()

# Iterate through all txt files in the specified folder

trajectory = JointTrajectory()
trajectory.joint_names = joint_names

# Read waypoints from the txt file
with open(file_path, 'r') as file:
    waypoints = [list(map(float, line.strip("[] \n").split(','))) for line in file if line.strip()]
    for i, positions in enumerate(waypoints):
        point = JointTrajectoryPoint()
        # JointTrajectoryPoint()：単一の軌道を表現するメッセージ型.
        point.positions = positions
        point.time_from_start = rospy.Duration(1.0*i) # 各ウェイポイントにどのくらいの時間に到達するか(現在は0.2秒ごとに到達するようにしている)
        # simulation1 = 0.4, simulation2 = 0.7, simulation3_1 = 0.7, simulation3_2 = 1.1
        trajectory.points.append(point)

# ゴールの設定
goal = FollowJointTrajectoryGoal()
goal.trajectory = trajectory
# アクションを実行
client.send_goal(goal)
client.wait_for_result()

result = client.get_result()
if result.error_code == result.SUCCESSFUL:
    print("successful!")
else:
    print(f"failed! Error message: {result.error_string}")

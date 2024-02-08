from operator import ge
import os
from re import T
import sys
import rospy
import moveit_commander
import actionlib
import csv
from datetime import datetime
from randomsg import RandomCoordinatesGenerator
from TaskToConfig import TtoC
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


if not rospy.get_node_uri():
    rospy.init_node('xArm6')

# Initialize MoveIt Commander
moveit_commander.roscpp_initialize(sys.argv)
robot = moveit_commander.RobotCommander()
group = moveit_commander.MoveGroupCommander("xarm6")

joint_names = group.get_active_joints()

# Create a list to store execute times
times = []
count = 3
trajectory = JointTrajectory()

# Get the initial joint values
initial_joint_values = group.get_current_joint_values()
group.set_joint_value_target(initial_joint_values)

# 객체 생성
generatorR = RandomCoordinatesGenerator()
generatorC = TtoC()

# Iterate through all txt files in the specified folder
for i in range(count):
    print("Processing:", i)

    s, g = generatorR.generate_random_coordinates()
    start = generatorC.generate_sg(s)
    goal = generatorC.generate_sg(g)

    # go to start
    plan1 = group.plan(joints=start)
    group.go(wait=True)

    # go to goal
    start_time_plan = datetime.now()

    plan2 = group.plan(joints=goal)

    end_time_plan = datetime.now()
    planning_time = (end_time_plan - start_time_plan).total_seconds()
        
    # Record times
    times.append({
        'count': i,
        'planning_time': planning_time
    })

    # Save the plan to a txt file
    path_filename = f'/home/nishidalab07/github/6dimension/simulation2/Configuration/test/path_{i}.txt'
    # plan2 변수의 내용을 txt 파일에 저장
    with open(path_filename, 'w') as file:
        file.write(str(plan2))


# Shutdown MoveIt Commander
moveit_commander.roscpp_shutdown()

# Save times to a CSV file
csv_filename = '/home/nishidalab07/github/6dimension/simulation2/time_RRT_test.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['count', 'planning_time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in times:
        writer.writerow(entry)

print(f"Times saved to {csv_filename}")

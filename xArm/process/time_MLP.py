import os
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import csv

rospy.init_node('xArm6')

# folder_path = '/home/nishidalab07/github/6dimension/simulation2/extract_train_C/allpath'
folder_path = '/home/nishidalab07/github/6dimension/simulation3/waypoint2/extract_train_C/allpath'
times = []

joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']

client = actionlib.SimpleActionClient('/xarm/xarm6_traj_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
client.wait_for_server()

# Iterate through all txt files in the specified folder
for filename in os.listdir(folder_path):
    print("a")
    if filename.endswith(".txt"):
        trajectory = JointTrajectory()
        trajectory.joint_names = joint_names

        file_path = os.path.join(folder_path, filename)

        # Read waypoints from the txt file
        with open(file_path, 'r') as file:
            waypoints = [list(map(float, line.strip("[] \n").split(','))) for line in file if line.strip()]
            for i, positions in enumerate(waypoints):
                point = JointTrajectoryPoint()
                # JointTrajectoryPoint()：単一の軌道を表現するメッセージ型.
                point.positions = positions
                point.time_from_start = rospy.Duration(1.1*i) # 各ウェイポイントにどのくらいの時間に到達するか(現在は0.2秒ごとに到達するようにしている)
                # simulation1 = 0.4, simulation2 = 0.7, simulation3_1 = 0.7, simulation3_2 = 1.1
                trajectory.points.append(point)

        start_time_execute = rospy.Time.now()
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
        
        end_time_execute = rospy.Time.now()
        execute_time = (end_time_execute - start_time_execute).to_sec()

        # Record execute times
        times.append({'filename': filename, 'execute_time': execute_time})

# Save execute times to a CSV file
# csv_filename = '/home/nishidalab07/github/6dimension/simulation2/time_MLP.csv'
csv_filename = '/home/nishidalab07/github/6dimension/simulation3/waypoint2/time_MLP.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['filename', 'execute_time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in times:
        writer.writerow(entry)

print(f"Execute times saved to {csv_filename}")

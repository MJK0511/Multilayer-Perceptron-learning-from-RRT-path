import os
import sys
import rospy
import moveit_commander
import csv
from datetime import datetime

rospy.init_node('xArm6')

# Initialize MoveIt Commander
moveit_commander.roscpp_initialize(sys.argv)
robot = moveit_commander.RobotCommander()
group = moveit_commander.MoveGroupCommander("xarm6")

joint_names = group.get_active_joints()

# Specify the folder path
folder_path = '/home/nishidalab07/github/6dimension/simulation2/extract_train_C/sgpath/test'
# folder_path = '/home/nishidalab07/github/6dimension/simulation3/waypoint2/extract_train_C/sgpath'

# Create a list to store execute times
times = []

# Get the initial joint values
initial_joint_values = group.get_current_joint_values()

# Iterate through all txt files in the specified folder
# Iterate through all txt files in the specified folder
for filename in os.listdir(folder_path):
    print("Processing:", filename)
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        # Set the start state to the initial joint values
        group.set_joint_value_target(initial_joint_values)

        # Read waypoints from the txt file
        with open(file_path, 'r') as file:
            waypoints = [list(map(float, line.strip("[] \n").split(','))) for line in file if line.strip()]
            print(waypoints)
            
        # Iterate through waypoints and plan for each set of joint values
        for waypoint in waypoints:
            start_time_plan = datetime.now()

            # Plan the trajectory for a single set of joint values
            plan = group.plan(joints=waypoint)

            end_time_plan = datetime.now()
            planning_time = (end_time_plan - start_time_plan).total_seconds()

            start_time_execute = datetime.now()

            # Execute the trajectory for a single set of joint values
            group.go(wait=True)

            end_time_execute = datetime.now()
            execute_time = (end_time_execute - start_time_execute).total_seconds()

            # Record times
            times.append({
                'filename': filename,
                'planning_time': planning_time,
                'execute_time': execute_time
            })


# Shutdown MoveIt Commander
moveit_commander.roscpp_shutdown()

# Save times to a CSV file
# csv_filename = '/home/nishidalab07/github/6dimension/simulation2/time_RRT.csv'
csv_filename = '/home/nishidalab07/github/6dimension/simulation3/waypoint2/time_RRT.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['filename', 'planning_time', 'execute_time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in times:
        writer.writerow(entry)

print(f"Times saved to {csv_filename}")

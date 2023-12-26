#!/usr/bin/env python3
import rospy
from moveit_commander import RobotCommander, MoveGroupCommander
from moveit_msgs.msg import RobotTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

# 초기화
rospy.init_node("xArm6")
robot = RobotCommander()
xarm = MoveGroupCommander("xarm6")

# 초기 관절 각도 설정
fixed_joint_values = [-1.6534045313536774, -0.4344945179660176, -0.9312986710565107, 4.736198222337609e-06, 1.3657615919112918, -1.6534435259080114]  # g의 위치

# 현재 상태를 초기화하고 목표 관절 각도 설정
xarm.set_start_state_to_current_state()
xarm.set_joint_value_target(fixed_joint_values)

# 경로 계획
plan, _, _, _ = xarm.plan()

# 새로운 RobotTrajectory 메시지 생성
robot_trajectory = RobotTrajectory()
robot_trajectory.joint_trajectory.joint_names = plan.joint_trajectory.joint_names

# 새로운 JointTrajectoryPoint를 생성하고 계획된 경로의 포인트들을 추가
for point in plan.joint_trajectory.points:
    new_point = JointTrajectoryPoint()
    new_point.positions = point.positions
    new_point.velocities = point.velocities
    new_point.accelerations = point.accelerations
    new_point.effort = point.effort
    new_point.time_from_start = point.time_from_start
    robot_trajectory.joint_trajectory.points.append(new_point)

# 경로 실행
xarm.execute(robot_trajectory)

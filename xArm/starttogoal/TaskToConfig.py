from operator import ge
from turtle import st
import rospy
from moveit_commander import RobotCommander, MoveGroupCommander
from moveit_msgs.msg import RobotState
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest
from geometry_msgs.msg import PoseStamped
from randomsg import RandomCoordinatesGenerator

class TtoC:
    def __init__(self):
        # 노드가 이미 초기화되었는지 확인하고 초기화되지 않았을 경우에만 초기화
        if not rospy.get_node_uri():
            rospy.init_node("inverse_kinematics_example")

    def inverse_kinematics(self, pose):
        # RobotCommander를 초기화
        robot = RobotCommander()

        # MoveGroupCommander를 초기화
        move_group = robot.get_group("xarm6")

        # 현재 로봇 관절 각을 가져오기
        current_joint_values = move_group.get_current_joint_values()

        # IK 서비스 프록시 생성
        ik_service = rospy.ServiceProxy("/compute_ik", GetPositionIK)

        # 목표 포즈 설정
        target_pose = PoseStamped()
        target_pose.header.frame_id = move_group.get_planning_frame()
        target_pose.pose.position.x = pose.x
        target_pose.pose.position.y = pose.y
        target_pose.pose.position.z = pose.z
        target_pose.pose.orientation.x = pose.ox
        target_pose.pose.orientation.y = pose.oy
        target_pose.pose.orientation.z = pose.oz
        target_pose.pose.orientation.w = pose.ow

        # IK 요청 생성
        ik_request = GetPositionIKRequest()
        ik_request.ik_request.group_name = move_group.get_name()
        ik_request.ik_request.robot_state.joint_state.name = move_group.get_active_joints()
        ik_request.ik_request.robot_state.joint_state.position = current_joint_values
        ik_request.ik_request.pose_stamped = target_pose
        ik_request.ik_request.timeout = rospy.Duration(6.0)

        # IK 서비스 호출
        ik_response = ik_service(ik_request)

        # 결과 확인 및 반환
        if ik_response.error_code.val == ik_response.error_code.SUCCESS:
            return ik_response.solution.joint_state.position
        else:
            rospy.logerr("Failed to find IK solution.")
            return None
        
    def generate_sg(self, pose):
        result = self.inverse_kinematics(pose)
        
        if result is not None:
            extract_result = [result[0], result[1], result[2], result[3], result[4], result[5]]
            return extract_result
        else:
            return None


# 객체 생성
generatorR = RandomCoordinatesGenerator()
generatorC = TtoC()

s, g = generatorR.generate_random_coordinates()
print(s)
print(g)

# # # 역기구학 호출하여 관절 각을 얻기
start = generatorC.generate_sg(s)
goal = generatorC.generate_sg(g)

if start or goal:
    print("Inverse Kinematics Solution:")
    print("start")
    print(start)
    print("\ngoal")
    print(goal)

else:
    print("Failed to find Inverse Kinematics Solution.")

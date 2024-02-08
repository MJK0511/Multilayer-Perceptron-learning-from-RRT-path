import rospy
from moveit_commander import RobotCommander
from moveit_msgs.msg import RobotState
from moveit_msgs.srv import GetPositionFK, GetPositionFKRequest
import re
import os

# waypoints_file = "/home/nishidalab07/github/6dimension/simulation1/extract_train_C/sg.txt"

class Pose:
    def __init__(self, x, y, z, orientation_x, orientation_y, orientation_z, orientation_w):
        self.x = x
        self.y = y
        self.z = z
        self.orientation_x = orientation_x
        self.orientation_y = orientation_y
        self.orientation_z = orientation_z
        self.orientation_w = orientation_w

class CtoT:
    def forward_kinematics(self, joint_angles_list):
        rospy.init_node("forward_kinematics_example")

        # RobotCommanderを初期化
        robot = RobotCommander()

        # MoveGroupCommanderを初期化
        move_group = robot.get_group("xarm6")

        poses = []

        # サービスプロキシの作成
        fk_service = rospy.ServiceProxy("/compute_fk", GetPositionFK)

        for joint_angles in joint_angles_list:
            # 関節角度のリストをRobotStateにセット
            robot_state = RobotState()
            robot_state.joint_state.name = move_group.get_active_joints()
            robot_state.joint_state.position = joint_angles

            # FKリクエストの作成
            fk_request = GetPositionFKRequest()
            fk_request.robot_state = robot_state
            fk_request.fk_link_names = [move_group.get_end_effector_link()]

            # FKサービスの呼び出し
            fk_response = fk_service(fk_request)

            # レスポンスから姿勢を取得
            pose = fk_response.pose_stamped[0].pose

            poses.append(Pose(
                pose.position.x, pose.position.y, pose.position.z,
                pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w
            ))

        return poses

    def add_pose_target(self, x, y, z, orientation_x, orientation_y, orientation_z, orientation_w):
        pose_target = [
            float(x),
            float(y),
            float(z),
            float(orientation_x),
            float(orientation_y),
            float(orientation_z),
            float(orientation_w)
        ]
        pose_target.append(pose_target)

    def process_files(self, input_folder_path, output_folder_path):
        for filename in os.listdir(input_folder_path):
            if filename.endswith('.txt'):
                input_file_path = os.path.join(input_folder_path, filename)
                output_file_path = os.path.join(output_folder_path, filename.replace('.txt', '_visual.txt'))

                waypoints = []
                with open(input_file_path, "r") as file:
                    for line in file:
                        line = line.strip().strip("[]")
                        values = line.split(",")
                        joint_value = [float(value) for value in values]
                        waypoints.append(joint_value)

                poses = self.forward_kinematics(waypoints)

                with open(output_file_path, 'w') as file:
                    for pose in poses:
                        file.write(f'[{pose.x}, {pose.y}, {pose.z}, {pose.orientation_x}, {pose.orientation_y}, {pose.orientation_z},{pose.orientation_w}]\n')

                print(f"Results saved to {output_file_path}")


if __name__ == "__main__":
    input_folder_path = '/home/nishidalab07/github/6dimension/simulation2/sg'
    output_folder_path = '/home/nishidalab07/github/6dimension/simulation2/sg'
    configtotask = CtoT()
    configtotask.process_files(input_folder_path, output_folder_path)
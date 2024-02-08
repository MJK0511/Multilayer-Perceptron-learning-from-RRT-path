import rospy
from moveit_commander import RobotCommander
from moveit_msgs.msg import RobotState
from moveit_msgs.srv import GetPositionFK, GetPositionFKRequest
import re
import os

waypoints_file = "/home/nishidalab07/github/6dimension/hani/start.txt"
# waypoints_file = "goal.txt"

class Pose:
    def __init__(self, x, y, z, orientation_x, orientation_y, orientation_z, orientation_w):
        self.x = x
        self.y = y
        self.z = z
        self.orientation_x = orientation_x
        self.orientation_y = orientation_y
        self.orientation_z = orientation_z
        self.orientation_w = orientation_w

def forward_kinematics(joint_angles_list):
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

def add_pose_target(x, y, z, orientation_x, orientation_y, orientation_z, orientation_w):
    pose_target = [
        float(x),
        float(y),
        float(z),
        float(orientation_x),
        float(orientation_y),
        float(orientation_z),
        float(orientation_w)
    ]
    pose_targets.append(pose_target)

# ウェイポイントをファイルから読み取る
waypoints = []
with open(waypoints_file, "r") as file:
    for line in file:
        line = line.strip().strip("[]")
        values = line.split(",")
        joint_value = [float(value) for value in values]
        waypoints.append(joint_value)

# forward_kinematicsを呼び出してポーズのリストを取得
poses = forward_kinematics(waypoints)

# ポーズのリストをファイルに保存
with open('data.txt', 'w') as file:
    for pose in poses:
        file.write(f'Pose: position: x: {pose.x} y: {pose.y} z: {pose.z} orientation: x: {pose.orientation_x} y: {pose.orientation_y} z: {pose.orientation_z} w: {pose.orientation_w}\n')

# ファイルの読み込み
with open('data.txt', 'r') as file:
    data = file.read()

matches = re.findall(
    r'Pose: position:\s*x: (.*?)\s*y: (.*?)\s*z: (.*?)\s*orientation:\s*x: (.*?)\s*y: (.*?)\s*z: (.*?)\s*w: (.*?)\n',
    data
)

pose_targets = []

def add_pose_target(x, y, z, orientation_x, orientation_y, orientation_z, orientation_w):
    pose_target = [
        float(x),
        float(y),
        float(z),
        float(orientation_x),
        float(orientation_y),
        float(orientation_z),
        float(orientation_w)
    ]
    pose_targets.append(pose_target)

for pose in matches:
    add_pose_target(*pose)

# pose_targetsの内容を表示
with open('/home/nishidalab07/github/6dimension/start_T.txt', 'w') as file:
    for pose_target in pose_targets:
        file.write(f'{pose_target}\n')

# ファイルを削除する
file_path = "data.txt"
os.remove(file_path)
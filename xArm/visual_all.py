import rospy
import os
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Pose
import ast
import random

class Visual:
# 関数定義
    def set_pose(self, pose_tuple):
        pose = Pose()
        pose.position.x = pose_tuple[0]
        pose.position.y = pose_tuple[1]
        pose.position.z = pose_tuple[2]
        pose.orientation.x = pose_tuple[3]
        pose.orientation.y = pose_tuple[4]
        pose.orientation.z = pose_tuple[5]
        pose.orientation.w = pose_tuple[6]
        return pose

    def generate_random_color(self):
        return random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)

    def visualize_trajectory_points(self, positions_list, filename):
        marker_array = MarkerArray()

        for i, position in enumerate(positions_list):
            end_effector_pose = self.set_pose(position)

            marker = Marker()
            marker.header.frame_id = "world"
            marker.header.stamp = rospy.Time.now()
            marker.ns = "end_effector_markers"
            marker.id = i
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose = end_effector_pose
            marker.scale.x = 0.05
            marker.scale.y = 0.05
            marker.scale.z = 0.05

            # # ランダムな色を生成
            marker.color.a = 1.0
            if filename == 'sg':
                marker.color.r, marker.color.g, marker.color.b = 1.0, 1.0, 1.0
            if filename == 'ma':
                marker.color.r, marker.color.g, marker.color.b = 1.0, 0.0, 0.0
            if filename == 'mb':
                marker.color.r, marker.color.g, marker.color.b = 0.0, 1.0, 0.0
            if filename == 'mc':
                marker.color.r, marker.color.g, marker.color.b = 0.0, 0.0, 1.0

            marker_array.markers.append(marker)

        return marker_array
    
    def visualization(self, default_folder, point):
        file_path = os.path.join(default_folder, f'Task/After_train/{point}_visual.txt')
        # すべてのファイルから位置が格納されたリストを読み取る
        positions_list = []
        with open(file_path, "r") as file:
            positions_list.extend([ast.literal_eval(line) for line in file])

        # マーカーパブリッシャー
        marker_pub = rospy.Publisher(f"visualization_{point}", MarkerArray, queue_size=10)
        rospy.sleep(1)  # パブリッシャーのセットアップ待ち

        marker_array = self.visualize_trajectory_points(positions_list, point)
        marker_pub.publish(marker_array)
                  

    def main(self, default_folder):
        rospy.init_node("visualize_end_effector_trajectory")
        while not rospy.is_shutdown():
            self.visualization(default_folder, 'sg')
            self.visualization(default_folder, 'ma')
            self.visualization(default_folder, 'mb')
            self.visualization(default_folder, 'mc')
            rospy.spin()

if __name__ == "__main__":
    default_folder = '/home/nishidalab07/github/6dimension/simulation2'
    visualizationMA = Visual()
    visualizationMA.main(default_folder)

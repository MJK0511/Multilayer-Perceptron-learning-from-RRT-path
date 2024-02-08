import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class Plot():
    def plot_3d_cube(self, ax, length=0.2, center=(0.2, -0.3, 0.1)):
        # 정육면체의 꼭지점 좌표 계산
        vertices = np.array([
            [-length/2, -length/2, -length/2],
            [-length/2, length/2, -length/2],
            [length/2, length/2, -length/2],
            [length/2, -length/2, -length/2],
            [-length/2, -length/2, length/2],
            [-length/2, length/2, length/2],
            [length/2, length/2, length/2],
            [length/2, -length/2, length/2]
        ])

        # 각 꼭지점을 중심으로 이동
        vertices += center

        # 정육면체의 면을 정의
        faces = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [2, 3, 7, 6],
            [0, 3, 7, 4],
            [1, 2, 6, 5]
        ]

        # 정육면체의 각 면을 그림
        for face in faces:
            x = vertices[face, 0]
            y = vertices[face, 1]
            z = vertices[face, 2]
            ax.plot(x, y, z, color='c')

    def plot_3d(self, df):
        # 예시 사용
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        self.plot_3d_cube(ax)

        # 선으로 연결해서 플롯
        ax.plot([df['sx'].values[0], df['mx'].values[0]], [df['sy'].values[0], df['my'].values[0]], [df['sz'].values[0], df['mz'].values[0]], color='k', label='Line: (sx, sy, sz) - (mx, my, mz)')
        ax.plot([df['mx'].values[0], df['gx'].values[0]], [df['my'].values[0], df['gy'].values[0]], [df['mz'].values[0], df['gz'].values[0]], color='k', label='Line: (mx, my, mz) - (gx, gy, gz)')
        # 각 점 플롯
        ax.scatter(df['sx'], df['sy'], df['sz'], marker='o', color='k', label='Start Point (sx, sy, sz)')
        ax.scatter(df['mx'], df['my'], df['mz'], marker='o', color='r', label='Mid Point (mx, my, mz)')
        ax.scatter(df['gx'], df['gy'], df['gz'], marker='o', color='k', label='End Point (gx, gy, gz)')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('3D Plot: Connecting Points')
        plt.legend()
        plt.show()

    def plot_2d(self, df):
        # 각각의 2차원 그래프를 그릴 서브플롯 생성
        fig, axs = plt.subplots(1, 3, figsize=(20, 5))  # Changed the number of subplots to 3

        # XZ 평면 그래프 (bx-bz, ax-az, cx-cz)
        axs[0].plot([df['sx'], df['mcx'], df['gx']], [df['sz'], df['mcz'], df['gz']], marker='o', color='gray')
        # axs[0].plot([0.1, 0.3, 0.3, 0.1, 0.1], [0.0, 0.0, 0.2, 0.2, 0.0], color='k', linestyle='--', label='Cube XZ') #simulation1
        axs[0].plot([-0.1, 0.3, 0.3, -0.1, -0.1], [0.0, 0.0, 0.8, 0.8, 0.0], color='k', linestyle='--', label='Cube XZ') #simulation2
        axs[0].set_xlabel('X')
        axs[0].set_ylabel('Z')
        axs[0].set_title('2D Plot: XZ Plane')

        # YZ 평면 그래프 (by-bz, ay-az, cy-cz)
        axs[1].plot([df['sy'], df['mcy'], df['gy']], [df['sz'], df['mcz'], df['gz']], marker='o', color='gray')
        # axs[1].plot([-0.4, -0.2, -0.2, -0.4, -0.4], [0.0, 0.0, 0.2, 0.2, 0.0], color='k', linestyle='--', label='Cube YZ') #simulation1
        axs[1].plot([0.3, 0.5, 0.5, 0.3, 0.3], [0.0, 0.0, 0.8, 0.8, 0.0], color='k', linestyle='--', label='Cube YZ') #simulation2
        axs[1].set_xlabel('Y')
        axs[1].set_ylabel('Z')
        axs[1].set_title('2D Plot: YZ Plane')

        # XY 평면 그래프 (ax-ay, bx-by, cx-cy)
        axs[2].plot([df['sx'], df['mcx'], df['gx']], [df['sy'], df['mcy'], df['gy']], marker='o', color='gray')
        # axs[2].plot([0.1, 0.3, 0.3, 0.1, 0.1], [-0.4, -0.4, -0.2, -0.2, -0.4], color='k', linestyle='--', label='Cube XY') #simulation1
        axs[2].plot([0.3, 0.3, -0.1, -0.1, 0.3], [0.3, 0.5, 0.5, 0.3, 0.3], color='k', linestyle='--', label='Cube XY') #simulation
        axs[2].set_xlabel('X')
        axs[2].set_ylabel('Y')
        axs[2].set_title('2D Plot: XY Plane')

        # 전체 그래프 제목
        fig.suptitle('2D Plots')

        plt.show()


    def plot_2d_all(self, df):
        # 각각의 2차원 그래프를 그릴 서브플롯 생성
        fig, axs = plt.subplots(1, 3, figsize=(20, 5))  # Changed the number of subplots to 3

        # XZ 평면 그래프 (bx-bz, ax-az, cx-cz)
        axs[0].plot([df['sx'], df['mbx'], df['max'], df['mcx'], df['gx']], [df['sz'], df['mbz'], df['maz'], df['mcz'], df['gz']], marker='o', color='b')
        axs[0].plot([0.1, 0.3, 0.3, 0.1, 0.1], [0.0, 0.0, 0.2, 0.2, 0.0], color='b', linestyle='--', label='Cube XZ')
        axs[0].set_xlabel('X')
        axs[0].set_ylabel('Z')
        axs[0].set_title('2D Plot: XZ Plane')
        axs[0].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])  # Z축 눈금 설정

        # YZ 평면 그래프 (by-bz, ay-az, cy-cz)
        axs[1].plot([df['sy'], df['mby'], df['may'], df['mcy'], df['gy']], [df['sz'], df['mbz'], df['maz'], df['mcz'], df['gz']], marker='o', color='g')
        axs[1].plot([-0.4, -0.2, -0.2, -0.4, -0.4], [0.0, 0.0, 0.2, 0.2, 0.0], color='g', linestyle='--', label='Cube YZ')
        axs[1].set_xlabel('Y')
        axs[1].set_ylabel('Z')
        axs[1].set_title('2D Plot: YZ Plane')
        axs[1].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])

        # XY 평면 그래프 (ax-ay, bx-by, cx-cy)
        axs[2].plot([df['sx'], df['mbx'], df['max'], df['mcx'], df['gx']], [df['sy'], df['mby'], df['may'], df['mcy'], df['gy']], marker='o', color='r')
        axs[2].plot([0.1, 0.3, 0.3, 0.1, 0.1], [-0.4, -0.4, -0.2, -0.2, -0.4], color='r', linestyle='--', label='Cube XY')
        axs[2].set_xlabel('X')
        axs[2].set_ylabel('Y')
        axs[2].set_title('2D Plot: XY Plane')
        

        # 전체 그래프 제목
        fig.suptitle('2D Plots')

        plt.show()


if __name__ == "__main__":
    plotter = Plot()


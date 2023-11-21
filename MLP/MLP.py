import numpy as np
import scipy.special


class neuralNetwork:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # 入力層、隠れ層、出力層のノード数設定
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # リンクの重み行列wihとwho
        # 行列内の重みw_i_j, ノードiから次の層のノードjへのリンクの重み
        # w11 w21
        # w12 w22 など
        self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))

            # 学習率の設定
        self.lr = learningrate

        # 活性化関数：sigmoid
        self.activation_function = lambda x: scipy.special.expit(x)
            
    pass

    def train(self, inputs_list, targets_list):
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        # 隠れ層に入ってくる信号の計算
        hidden_inputs = np.dot(self.wih, inputs)
        # 隠れ層で結合された信号を活性化関数により出力
        hidden_outputs = self.activation_function(hidden_inputs)

        # 出力層に入ってくる信号の計算
        final_inputs = np.dot(self.who, hidden_outputs)
        # 出力層で結合された信号を活性化関数により出力
        final_outputs = self.activation_function(final_inputs)

        # 出力層の誤差　＝（目標出力ー最終出力）
        output_errors = targets-final_outputs
        # 隠れ層の誤差は出力層の誤差をリンクの重みの割合で分配
        hidden_errors = np.dot(self.who.T, output_errors)
            
        # 隠れ層と出力層の間のリンクの重みを更新
        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), np.transpose(hidden_outputs))

        # 入力層と隠れ層の間のリンクの重みを更新
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))

        pass

    def query(self, inputs_list):
        #入力リストを行列に変換
        inputs = np.array(inputs_list, ndmin=2).T
            
        # 隠れ層に入ってくる信号の計算
        hidden_inputs = np.dot(self.wih, inputs)
        # 隠れ層で結合された信号を活性化関数により出力
        hidden_outputs = self.activation_function(hidden_inputs)

        # 出力層に入ってくる信号の計算
        final_inputs = np.dot(self.who, hidden_outputs)
        # 出力層で結合された信号を活性化関数により出力
        final_outputs = self.activation_function(final_inputs)

        return final_outputs

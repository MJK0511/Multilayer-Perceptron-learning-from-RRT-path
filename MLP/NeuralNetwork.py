import numpy as np
from Adam import Adam

class neuralNetwork:
    #ニューラルネットワークの初期化
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # 入力層、隠れ層、出力層のノード数設定
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # リンクの重み行列wih(weights input hidden)とwho(weights hidden output)
        # 行列内の重みw_i_j, ノードiから次の層のノードjへのリンクの重み
        # He
        self.wih = np.random.randn(self.hnodes, self.inodes) * np.sqrt(1.0 / self.inodes)
        self.who = np.random.randn(self.onodes, self.hnodes) * np.sqrt(1.0 / self.hnodes)
        #bias 
        self.bias_h = np.zeros((self.hnodes, 1))
        self.bias_o = np.zeros((self.onodes, 1))
        
        # 学習率の設定
        self.lr = learningrate

        # 活性化関数 
        self.activation_function = self.sigmoid

        # Adam optimizer for weights
        self.optimizer_wih = Adam(self.wih.shape, learning_rate=self.lr)
        self.optimizer_who = Adam(self.who.shape, learning_rate=self.lr)
        pass
    
    def sigmoid(self, x):
        return np.exp(-np.abs(x)) / (1 + np.exp(-np.abs(x)))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def identity(self, x):
        return x
    
    def mse_loss(self, targets, outputs):
        result = np.mean((targets - outputs) **2)
        return np.full((targets.shape[0], 1), result)
        # return targets - outputs

    #ニューラルネットワークの学習
    def train(self, inputs_list, targets_list):
        #入力値とターゲット値を2D配列に変換      
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        #正規化
        inputs = (inputs - np.mean(inputs)) / np.std(inputs)

        # 隠れ層に入ってくる信号の計算
        hidden_inputs = np.dot(self.wih, inputs) + self.bias_h
        hidden_outputs = self.activation_function(hidden_inputs)

        # 出力層に入ってくる信号の計算
        final_inputs = np.dot(self.who, hidden_outputs) + self.bias_o
        final_outputs = self.activation_function(final_inputs)
       
        # 出力層の誤差
        output_errors = self.mse_loss(targets, final_outputs)

        # 隠れ層の誤差は出力層の誤差をリンクの重みの割合で分配
        hidden_errors = np.dot(self.who.T, output_errors)

        # 隠れ層と出力層の間のリンクの重みを更新
        # self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), hidden_outputs.T)
        self.wih += self.optimizer_wih.update(np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), inputs.T))
        self.bias_o += self.lr * output_errors  # 出力層バイアス更新

        # 入力層と隠れ層の間のリンクの重みを更新
        # self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), inputs.T)
        self.who += self.optimizer_who.update(np.dot((output_errors * final_outputs * (1.0 - final_outputs)), hidden_outputs.T))
        self.bias_h += self.lr * hidden_errors  # 隠れ層バイアス更新

        pass
    
    #ニューラルネットワークの照会
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
        # final_outputs = abs(np.round(self.activation_function(final_inputs)))
        final_outputs = np.round(self.activation_function(final_inputs)*100)
        
        return final_outputs
    
    

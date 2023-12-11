import numpy as np

class neuralNetwork:
    #ニューラルネットワークの初期化
    def __init__(self, inputnodes, hiddennodes, hiddenlayers, outputnodes, learningrate):
        # 入力層、隠れ層、出力層のノード数設定
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.hlayers = hiddenlayers
        self.onodes = outputnodes

        self.initialize_weights_and_biases()    # 重みとバイアスの初期化
        self.lr = learningrate                  # 学習率の設定
        self.activation_function = self.sigmoid # 活性化関数 
        
        pass
    
    #ニューラルネットワークの学習
    def train(self, inputs_list, targets_list):
        #入力値とターゲット値を2D配列に変換
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        # 隠れ層に入ってくる信号の計算
        hidden_inputs1 = np.dot(self.wih1, inputs) + self.bias_h1
        hidden_outputs1 = self.activation_function(hidden_inputs1)

        hidden_inputs2 = np.dot(self.wih2, hidden_outputs1) + self.bias_h2
        hidden_outputs2 = self.activation_function(hidden_inputs2)

        hidden_inputs3 = np.dot(self.wih3, hidden_outputs2) + self.bias_h3
        hidden_outputs3 = self.activation_function(hidden_inputs3)

        hidden_inputs4 = np.dot(self.wih4, hidden_outputs3) + self.bias_h4
        hidden_outputs4 = self.activation_function(hidden_inputs4)

        # 出力層に入ってくる信号の計算
        final_inputs = np.dot(self.who, hidden_outputs4) + self.bias_o
        final_outputs = self.activation_function(final_inputs)
       
        # 出力層の誤差
        output_errors = self.mse_loss(targets, final_outputs)

        # 隠れ層の誤差は出力層の誤差をリンクの重みの割合で分配
        hidden_errors4 = np.dot(self.who.T, output_errors)
        update_wih4 = self.lr * (np.dot((hidden_errors4 * hidden_outputs4 * (1.0 - hidden_outputs4)), hidden_outputs3.T))
        self.wih4 += update_wih4

        hidden_errors3 = np.dot(self.wih4.T, hidden_errors4)
        update_wih3 = self.lr * (np.dot((hidden_errors3 * hidden_outputs3 * (1.0 - hidden_outputs3)), hidden_outputs2.T))
        self.wih3 += update_wih3

        hidden_errors2 = np.dot(self.wih3.T, hidden_errors3)
        update_wih2 = self.lr * (np.dot((hidden_errors2 * hidden_outputs2 * (1.0 - hidden_outputs2)), hidden_outputs1.T))
        self.wih2 += update_wih2

        hidden_errors1 = np.dot(self.wih2.T, hidden_errors2)
        update_wih1 = self.lr * (np.dot((hidden_errors1 * hidden_outputs1 * (1.0 - hidden_outputs1)), inputs.T))
        self.wih1 += update_wih1

        # 入力層と隠れ層の間のリンクの重みを更新
        self.who += self.lr * (np.dot((output_errors * final_outputs * (1.0 - final_outputs)), hidden_outputs4.T))
        
        self.bias_o += self.lr * output_errors  # 出力層バイアス更新
        self.bias_h1 += self.lr * hidden_errors1 # 隠れ層バイアス更新
        self.bias_h2 += self.lr * hidden_errors2
        self.bias_h3 += self.lr * hidden_errors3
        self.bias_h4 += self.lr * hidden_errors4

        pass
    
    #ニューラルネットワークの照会
    def query(self, inputs_list):
        #入力リストを行列に変換
        inputs = np.array(inputs_list, ndmin=2).T
        
        # 隠れ層に入ってくる信号の計算
        hidden_layer1 = np.dot(self.wih1, inputs)
        hidden_layer2 = np.dot(self.wih2, hidden_layer1)
        hidden_layer3 = np.dot(self.wih3, hidden_layer2)
        hidden_layer4 = np.dot(self.wih4, hidden_layer3)

        # 隠れ層で結合された信号を活性化関数により出力
        hidden_outputs = self.activation_function(hidden_layer4)

        # 出力層に入ってくる信号の計算
        final_inputs = np.dot(self.who, hidden_outputs)
        # 出力層で結合された信号を活性化関数により出力
        # final_outputs = abs((self.activation_function_q(final_inputs)))
        final_outputs = np.round(self.activation_function(final_inputs)*100)

        return final_outputs
    

    def sigmoid(self, x):
        return np.exp(-np.abs(x)) / (1 + np.exp(-np.abs(x)))
    
    def identity(self, x):
        return x
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def mse_loss(self, targets, outputs):
        result = np.mean((targets - outputs) **2)
        return np.full((targets.shape[0], 1), result)
    
    def initialize_weights_and_biases(self):
        # 初期化関数
        def initialize_matrix(rows, cols):
            # return np.random.randn(rows, cols) * np.sqrt(1.0 / cols)
            return np.random.randn(rows, cols) * np.sqrt(2.0 / (rows + cols))

        # 重みとバイアスの初期化
        for i in range(1, self.hlayers + 2):
            setattr(self, f'wih{i}', initialize_matrix(self.hnodes, self.hnodes if i > 1 else self.inodes))
            setattr(self, f'bias_h{i}', np.zeros((self.hnodes, 1)))

        self.who = initialize_matrix(self.onodes, self.hnodes)
        self.bias_o = np.zeros((self.onodes, 1))

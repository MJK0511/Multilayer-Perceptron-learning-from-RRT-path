from NeuralNetwork import neuralNetwork
import numpy as np 

def normalize_data(data, mean, std):
    normalized_data = (data - mean) / std
    return normalized_data

class MLP3rd:
    def __init__(self):
        self.input_nodes = 4
        self.hidden_nodes = 30
        self.hidden_layers = 4
        self.output_nodes = 2
        self.learning_rate = 0.00001
        self.epochs = 30
    
    def LearningData(self, learningdata):
        #学習データ準備
        self.train_inputs = learningdata.train_input_data[['sx', 'sy', 'gx', 'gy']].values
        self.mean = self.train_inputs.mean(axis=0)
        self.std = self.train_inputs.std(axis=0)
        self.train_inputs = normalize_data(self.train_inputs, self.mean, self.std)
        self.train_outputs = learningdata.train_output_data[['mx', 'my']].values

    def Learning(self):
        # データ学習
        self.n = neuralNetwork(self.input_nodes, self.hidden_nodes, self.hidden_layers, self.output_nodes, self.learning_rate)

        for self.epoch in range(self.epochs):
            for i in range(len(self.train_inputs)):
                inputs = self.train_inputs[i]
                targets = self.train_outputs[i]
                self.n.train(inputs, targets)

            # 손실(MSE) 계산 및 출력
            predictions = [self.n.query(inp) for inp in self.train_inputs]
            mse = np.mean([(t - o) ** 2 for t, o in zip(self.train_outputs, predictions)])
            print(f"Mean Squared Error: {mse}")

    def TestData(self, testdata):
        #テストデータ準備
        testdata2 = []
        testdata3 = []

        # テスト
        for i in range(testdata.shape[0]):
            test_input = testdata[i, :] 
            normalized_test_input = normalize_data(test_input, self.mean, self.std)
            test_output = self.n.query(normalized_test_input).T
            new_testdata2 = [test_input[0], test_input[1], test_output[0, 0], test_output[0, 1]]
            new_testdata3 = [test_output[0, 0], test_output[0, 1], test_input[2], test_input[3]]
            testdata2.append(new_testdata2)
            testdata3.append(new_testdata3)
            print(f"Test Input {i+1}: {test_input}")
            print(f"Test Output: ({test_output})")

        return testdata2, testdata3

    def TestDataRE(self, testdata):
        self.test_data = np.array(testdata)
        return self.test_data  



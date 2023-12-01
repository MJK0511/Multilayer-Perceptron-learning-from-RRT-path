from NeuralNetwork import neuralNetwork
import pandas as pd

class MLP3rd:
    def __init__(self):
        self.input_nodes = 4
        self.hidden_nodes = 30
        self.output_nodes = 2
        self.learning_rate = 0.00001
        self.epochs = 30

    def normalize_data(data, mean, std):
        return (data - mean) / std
    
    def LearningData(self, learningdata):
        #学習データ準備
        self.traindata = learningdata
        self.train_inputs = self.traindata.train_input_data[['sx', 'sy', 'gx', 'gy']].values
        self.mean = self.train_inputs.mean(axis=0)
        self.std = self.train_inputs.std(axis=0)
        self.normalize_data(self.train_inputs,self.mean, self.std)

        self.train_outputs = self.traindata.train_output_data[['mx', 'my']].values
         
    def Learning(self):
        # データ学習
        self.n = neuralNetwork(self.input_nodes, self.hidden_nodes, self.output_nodes, self.learning_rate)
        for self.epoch in range(self.epochs):
            for i in range(len(self.train_inputs)):
                inputs = self.train_inputs[i]
                targets = self.train_outputs[i]
                self.n.train(inputs, targets)

    def TestData(self, testdata):
        #テストデータ準備
        self.normalize_data(testdata, self.mean, self.std)
        test_inputs = testdata.test_data[['sx', 'sy', 'gx', 'gy']].values
        # print(test_inputs.shape)

        testdata2 = []
        testdata3 = []
        # テスト
        for i in range(test_inputs.shape[0]):
            test_input = test_inputs[i, :] 
            test_output = self.n.query(test_input).T
            new_testdata2 = [test_input[0], test_input[1], test_output[0, 0], test_output[0, 1]]
            new_testdata3 = [test_output[0, 0], test_output[0, 1], test_input[2], test_input[3]]
            testdata2.append(new_testdata2)
            testdata3.append(new_testdata3)
            print(f"Test Input {i+1}: {test_input}")
            print(f"Test Output: ({test_output})")

        # Create a DataFrame
        columns = ['sx', 'sy', 'gx', 'gy']
        test_data_df2 = pd.DataFrame(testdata2, columns=columns)
        test_data_df3 = pd.DataFrame(testdata3, columns=columns)

        return test_data_df2, test_data_df3
    


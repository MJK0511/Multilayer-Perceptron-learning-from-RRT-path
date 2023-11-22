import numpy as np
from MLP import neuralNetwork
from Data import TrainingData, TestData

#学習データ準備
traindata = TrainingData()
train_inputs = traindata.all_train_data[['s', 'm1', 'm2', 'm3', 'm4', 'm5', 'g']].values
train_outputs = traindata.all_train_data[['m1', 'm2', 'm3', 'm4', 'm5']].values

#テストデータ準備
testdata = TestData()
test_inputs = testdata.test_data[['start', 'goal']].values

# ニューラルネットワークの構成
input_nodes = 7
hidden_nodes = 9
output_nodes = 5
learning_rate = 0.01
epochs = 1000

n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

# データ学習
for epoch in range(epochs):
    for i in range(len(train_inputs)):
        inputs = train_inputs[i]
        targets = train_outputs[i]
        n.train(inputs, targets)

# テスト
for input_pair in test_inputs:
    predicted_output = n.query(input_pair)
    print(f"Start: {input_pair[0]}, Goal: {input_pair[1]}, Predicted Middle Coordinates: {predicted_output}")

import numpy as np
import pandas as pd
from MLP import neuralNetwork
from Data import TrainingData
from Data import TestData

traindata = TrainingData()

# 入力データと目標データ設定
input_data = traindata.all_train_data[['X', 'Y']].values
output_data = traindata.all_train_data[['X', 'Y']].values # 目標は入力と同じく（例題なので任意）

# ニューラルネットワークの構成
input_nodes = 2
hidden_nodes = 9
output_nodes = 2
learning_rate = 0.01
epochs = 1000

n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

# データ学習
for epoch in range(epochs):
    for i in range(len(input_data)):
        inputs = input_data[i]
        targets = output_data[i]
        n.train(inputs, targets)

# テスト：学習されたニューラルネットワークを利用して予測
testdata = TestData()
for input_point in testdata.test_input:
    predicted_output = n.query(input_point)
    print(f"Input: {input_point}, Predicted Output: {predicted_output}")
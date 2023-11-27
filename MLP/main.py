from MLP import neuralNetwork
from Data import TrainingData, TestData

#学習データ準備
traindata = TrainingData()
train_inputs = traindata.train_input_data[['sx', 'sy', 'gx', 'gy']].values
train_outputs = traindata.train_output_data[['mx', 'my']].values
mean = train_inputs.mean(axis=0)
std = train_inputs.std(axis=0)
train_inputs = (train_inputs - mean) / std

# ニューラルネットワークの構成
input_nodes = 4
hidden_nodes = 4
output_nodes = 2
learning_rate = 0.00001
epochs = 10

n = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

# データ学習
for epoch in range(epochs):
    for i in range(len(train_inputs)):
        inputs = train_inputs[i]
        targets = train_outputs[i]
        n.train(inputs, targets)
        # print(f"Epoch {epoch+1}/{epochs}, Loss: {n.loss}")


#テストデータ準備
testdata = TestData()
# 테스트 데이터 정규화
testdata.normalize_test_data(mean, std)
test_inputs = testdata.test_data[['sx', 'sy', 'gx', 'gy']].values

# テスト
for i in range(test_inputs.shape[0]):
    test_input = test_inputs[i, :]  # 각 행에 대한 데이터를 선택
    test_output = n.query(test_input).T
    print(f"Test Input {i+1}: {test_input})")
    print(f"Test Output: {test_output}")
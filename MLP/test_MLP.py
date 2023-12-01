import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# 다층 퍼셉트론(MLP) 정의
class MLP:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # 가중치 및 편향 초기화
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.bias_hidden = np.zeros((1, hidden_size))
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_output = np.zeros((1, output_size))

    def forward(self, x):
        # 입력층에서 은닉층으로의 전파
        self.hidden_input = np.dot(x, self.weights_input_hidden) + self.bias_hidden
        self.hidden_output = sigmoid(self.hidden_input)

        # 은닉층에서 출력층으로의 전파
        self.output_input = np.dot(self.hidden_output, self.weights_hidden_output) + self.bias_output
        self.model_output = sigmoid(self.output_input)

        return self.model_output

    def backward(self, x, y, learning_rate):
        # 출력층의 오차와 경사 계산
        output_error = y - self.model_output
        output_delta = output_error * sigmoid_derivative(self.model_output)

        # 은닉층의 오차와 경사 계산
        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_delta = hidden_error * sigmoid_derivative(self.hidden_output)

        # 가중치 및 편향 업데이트
        self.weights_hidden_output += self.hidden_output.T.dot(output_delta) * learning_rate
        self.bias_output += np.sum(output_delta, axis=0, keepdims=True) * learning_rate
        self.weights_input_hidden += x.T.dot(hidden_delta) * learning_rate
        self.bias_hidden += np.sum(hidden_delta, axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            # Forward pass
            output = self.forward(X)

            # Backward pass 및 업데이트
            self.backward(X, y, learning_rate)

            # 손실 출력
            loss = np.mean(0.5 * (y - output) ** 2)
            if (epoch + 1) % 100 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss:.4f}')

# 학습 데이터 생성 (임의의 데이터 사용)
np.random.seed(42)
num_samples = 1000
input_size = 10  # 입력 특성의 수
hidden_size = 5  # 은닉층의 크기
output_size = 10  # 출력 특성의 수
input_data = np.random.randn(num_samples, input_size)
target_data = input_data.copy()  # 항등 함수를 사용하므로 출력은 입력과 같게 설정

# 학습
mlp = MLP(input_size, hidden_size, output_size)
mlp.train(input_data, target_data, epochs=1000, learning_rate=0.01)

# 테스트 데이터 생성 (임의의 데이터 사용)
test_data = np.random.randn(5, input_size)

# 테스트
test_output = mlp.forward(test_data)
print("\n테스트 예측 결과:")
print(test_output)

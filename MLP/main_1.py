from Training import MLP3rd
from Data import call_LD, call_TD

# MLP3rd 클래스의 인스턴스 생성
mlp_instance = MLP3rd()

# 학습 데이터 준비 및 학습
learningdata = call_LD()
mlp_instance.LearningData(learningdata)
mlp_instance.Learning()

# 테스트 수행
testdata = call_TD()
result1 = mlp_instance.TestData(testdata)

test_data_df2 = result1[0]
test_data_df3 = result1[1]
print("test_data_df2")
print(test_data_df2)
print("test_data_df3")
print(test_data_df3)

testdata = test_data_df2
result2 = mlp_instance.TestData(testdata)


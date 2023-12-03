from Training import MLP3rd
from Data import call_LD, call_TD

mlp_instance = MLP3rd()

# 学習
learningdata = call_LD()
mlp_instance.LearningData(learningdata)
mlp_instance.Learning()

# テスト
testdata = call_TD()

#MLP1
testdata1 = testdata.test_data
print("Result1")
result1 = mlp_instance.TestData(testdata1)

#MLP2
test_data_df2 = mlp_instance.TestDataRE(result1[0])
print("Result2")
result2 = mlp_instance.TestData(test_data_df2)

#MLP3
test_data_df3 = mlp_instance.TestDataRE(result1[1])
print("Result3")
result3 = mlp_instance.TestData(test_data_df3)

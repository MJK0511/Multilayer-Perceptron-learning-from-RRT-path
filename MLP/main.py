from Training import MLP3rd
from Data import call_LD, call_TD


mlp_instance1 = MLP3rd()
mlp_instance2 = MLP3rd()
mlp_instance3 = MLP3rd()

######################################
# 学習

# MLP1
input_filename1 = 'learning_input_data_m1.csv'
output_filename1 = 'learning_output_data_m1.csv'
learningdata1 = call_LD(input_filename1, output_filename1)
mlp_instance1.LearningData(learningdata1)
mlp_instance1.Learning()

#MLP2
input_filename2 = 'learning_input_data_m2.csv'
output_filename2 = 'learning_output_data_m2.csv'
learningdata2 = call_LD(input_filename2, output_filename2)
mlp_instance2.LearningData(learningdata2)
mlp_instance2.Learning()

# #MLP3
input_filename3 = 'learning_input_data_m3.csv'
output_filename3 = 'learning_output_data_m3.csv'
learningdata3 = call_LD(input_filename3, output_filename3)
mlp_instance3.LearningData(learningdata3)
mlp_instance3.Learning()

######################################
# テスト
test_input_filename = 'test_input_data.csv'
testdata = call_TD(test_input_filename)

#MLP1
testdata1 = testdata.test_data
print("Result1")
result1 = mlp_instance1.TestData(testdata1)

#MLP2
test_data_df2 = mlp_instance2.TestDataRE(result1[0])
print("Result2")
result2 = mlp_instance2.TestData(test_data_df2)

# #MLP3
test_data_df3 = mlp_instance3.TestDataRE(result1[1])
print("Result3")
result3 = mlp_instance3.TestData(test_data_df3)

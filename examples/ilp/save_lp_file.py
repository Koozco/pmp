from knapsack import knapsack_model

# If you need, you can save .lp file in purpose of archivization / verification

file_name = 'example_knapsack.lp'

model = knapsack_model()
model.write_to_file(file_name)

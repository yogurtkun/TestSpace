from function_tool import save_list,load_list

a = [1,2,3,4,5,6,7,8]

file = './test.plk'
save_list(file,a)
b = load_list(file)

print(b)

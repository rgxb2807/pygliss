#Euclid's Algorithm via StackOverFlow
def the_gcd(a, b):
	while (b > 0):
		temp = b
		b = a % b
		a = temp

	return a

def gcd(*args):
	result = args[0]
	for i in range(0, len(args)):
		result = the_gcd(result, args[i])

	return result

def the_lcm(a, b):
	return a * (b / gcd(a, b))

def lcm(num_list):
	result = num_list[0]
	for i in range(0, len(num_list)):
		result = the_lcm(result, num_list[i])
	return result
import numpy as np
from collections import OrderedDict
from pygliss.constants import DIVISIONS, BASE, A440, LOW, HIGH

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



def make_freq_to_steps_map():
    freq_map = OrderedDict()
    freq = A440
    count = 0
    
    # find lowest note
    while freq > LOW:
        count -= 1
        freq = A440 * (2 ** (count/DIVISIONS))        
    
    #build map
    while freq < HIGH:
        freq = A440 * (2 ** (count/DIVISIONS))
        freq_map[freq] = count
        count += 1
        
    return freq_map

def make_freq_vector(divisions=1):
    freqs = []
    freq = A440
    count = 0
    
    # find lowest note
    while freq > LOW:
        count -= 1
        freq = A440 * (2 ** (count/divisions))

    while freq < HIGH:
        freq = A440 * (2 ** (count/divisions))
        freqs.append(np.float64(freq))
        count += 1

    return np.array(freqs)

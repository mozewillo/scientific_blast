import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.interpolate import spline

np.random.seed(2)
###Two words generators###
#First generates random words of given length from given set of words(alphabet)
def random_generator(l, alphabet):
	word = ''.join([random.choice(alphabet) for _ in range(l)])
	return word

#Second generator puts motifs of 100 same letters every time
def repeat_generator(l, alphabet):
	k = 0
	k = l // 100
	word = ''.join([i*100 for i in [random.choice(alphabet) for _ in range(k)] ])
	if l%100 != 0:
		word += (l%100*random.choice(alphabet))
	return word


### Implementation od simple compression algorythm based on Lempel and Ziv method (LZ77)

def lz77_compress(word_in, dictionary_size ):
	words = word_in[0]*(dictionary_size-1)+word_in
	dic = ''
	maxi = 0
	out = []
	new = (0, 0, 'z')
	#encode first element
	out.append((0,0, word_in[0]))
	#delete encoded element
	word_in = word_in[1:]
	while len(word_in) != 0:
		#start from pattern_len = 0
		new = ( 0, 0, word_in[0])
		dic = words[:dictionary_size] * 1000
		for i in range(1, dictionary_size+1):
			#search alignment in dictionary
		 	if dic[-i] == word_in[0]:
		 		for j in range(len(word_in)):
		 			if j == (len(word_in)-1) and new[1]<j:
		 				new = (i, j, word_in[-1])
		 				break
		 			else:
			 			if dic[-i-j] == word_in[j]:
			 				maxi+=1
		 				else:
		 					if new [1] < maxi:
		 						new = (i, maxi, word_in[j])
		 					maxi = 0
		 					break
		out.append(new )
		word_in = word_in[(new[1] + 1) :]
		words = words[(new[1] + 1) :]
	return out


###Decompression

def lz77_decompress(word_in):
	decompressed = []
	decompressedi = []
	while len(word_in) != 0:
		if word_in[0][1] == 0:
			# encoded singletone
			decompressed.append(word_in[0][2])
		else:
			if word_in[0][1] > len(decompressed):
				decompressedi=[decompressed[-word_in[0][0]] for _ in range(100)]
			for i in range(-word_in[0][0], -(word_in[0][0]-word_in[0][1])):
				decompressed.append(decompressed[i])
			decompressed.append(word_in[0][2])		
		word_in = word_in[1:]
	decompressed = ''.join(decompressed)
	return decompressed


# Testing

def testing(compressor, generator, lengths_list, dictionary_size):
	test = []
	w = ''
	alfabet = ['a', 'b', 'c' , 'd', 'e', 'f', 'g' , 'h']
	for i in lengths_list:
		w = (compressor((generator(i, alfabet)), dictionary_size))
		test.append(len(w)) 
	return test


# Compression coeffitient (average)

def cmpr_coeffitient(compressor, generator, lengths_list, dictionary_size, tester=testing):
	cmpr_data = testing(compressor, generator, lengths_list, dictionary_size)
	w = []
	end = 0
	for y in cmpr_data:
		w.append(y / lengths_list[cmpr_data.index(y)])
	for i in w:
		if end != 0:
			end = (end + i) / 2
		else:
			end += 1
	return end


#	dependency between input and output sizes

def plot( compressor, generator, lengths_list, dictionary_size, tester=testing):
	test = tester(compressor, generator, lengths_list, dictionary_size)
	xnewpoint = np.linspace(min(lengths_list), max(lengths_list), 1000)
	smooth = spline(lengths_list, test, xnewpoint)
	plt.figure()
	plt.plot(xnewpoint, smooth)
	plt.xlabel('initial lengths')
	plt.ylabel('after-compression')
	plt.show()

#	compression coeffitient depending on ditionary size

def plot_coeffitients( compressor, generator, lengths_list, dictionary_size, tester=testing, wspol=cmpr_coeffitient ):
	wsp = []
	for i in dictionary_size:
		wsp.append(cmpr_coeffitient(compressor, generator, lengths_list, i)) 
	plt.figure()
	plt.plot(dictionary_size, wsp)
	plt.xlabel('Dictionary size')
	plt.ylabel('Compression coeffitient')
	plt.show()



plot(lz77_compress, random_generator, [200, 400, 600, 800, 1000], 20)
plot_coeffitients(lz77_compress, repeat_generator, [200, 400, 600, 800, 1000], [20, 40, 60, 80, 100])
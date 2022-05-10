alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 
	'g', 'h', 'i', 'j', 'k', 'l', 
	'm', 'n', 'o', 'p', 'q', 'r', 
	's', 't', 'u', 'v', 'w', 'x', 
	'y', 'z']

def get_message_length(message):	
	non_letters = 0
	
	# Counting non-letters
	for letter in message:
		if letter not in alphabet:
			non_letters += 1
	
	# Subtract non-letters from total message length
	total_message_length = len(message)
	alpha_length =  total_message_length - non_letters
	
	return alpha_length

def get_bigram_list(message_as_list):
	message_length = len(message_as_list)
	
	i = 0
	bigram_list = []
	
	while (i+1) < message_length:
		bigram = (message_as_list[i]) + (message_as_list[i+1])
		bigram_list.append(bigram)
		i += 1
	
	return bigram_list

def get_chi_squared_stat(ciphertext_freq, chi_squared_values, ngram_list, english_ngrams_freq):
	
	for ngram in ciphertext_freq.keys():
		ciphertext_freq[ngram] = ngram_list.count(ngram)
	
	for ngram in chi_squared_values.keys():
		# Running the chi-squared calculation for each ngram
		observed_value = ciphertext_freq[ngram]
		expected_value = english_ngrams_freq[ngram]
		
		x = round((((observed_value - expected_value)**2)/expected_value), 3)
		chi_squared_values[ngram] = x
	
	# Returning chi-squared stat for each possible message
	chi_squared_stat = round(sum(chi_squared_values.values()), 2)
	return chi_squared_stat

def decrypt_message(dictionary, p):
	chi_stat_dictionary = {}
	
	for shift, value in dictionary.items():
		chi_stat_dictionary[shift] = value[p]
	
	likely_key = min(chi_stat_dictionary, key = chi_stat_dictionary.get)
	likely_element = dictionary.pop(int(likely_key))
	likely_message = likely_element[0]
	
	return likely_message

def message_decrypted_question(decrypted_flag, dictionary, p):
	""" Looping over the most likely decrypted message from those available in dictionary. """
	
	while decrypted_flag == False:
		# Printing the most likely decrypted message from those available in the dictionary
		decrypted_message = decrypt_message(dictionary, p)
		print("\nLikely decrypted message: \n" + decrypted_message)
		
		# Asking the user if the decrypted message is correct
		question = input("\nIs this the decrypted message? Type Y or N: ")
		
		while True:
			question = question.upper()
			
			# Checking the user's answer is Y or N
			if question in ('Y', 'N'):
				# Looping over the dictionary with the user's response
				if question == 'Y':
					decrypted_flag = True
					break
				if question == 'N':
					break
			else:
				question = input("Please type Y or N: ")
				continue

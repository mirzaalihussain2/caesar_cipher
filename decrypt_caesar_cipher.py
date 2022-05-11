# Import modules
import create_alphabetic_dict as cad
import encrypter as enc
import encryption_functions as ef

# Set up
english_lang_freq = {
	'a': 0.08167,
	'b': 0.01492,
	'c': 0.02202,
	'd': 0.04253,
	'e': 0.12702,
	'f': 0.02228,
	'g': 0.02015,
	'h': 0.06094,
	'i': 0.06966,
	'j': 0.00153,
	'k': 0.01292,
	'l': 0.04025,
	'm': 0.02406,
	'n': 0.06749,
	'o': 0.07507,
	'p': 0.01929,
	'q': 0.00095,
	'r': 0.05987,
	's': 0.06327,
	't': 0.09356,
	'u': 0.02758,
	'v': 0.00978,
	'w': 0.02560,
	'x': 0.00150,
	'y': 0.01994,
	'z': 0.00077
	}

english_bigram_freq = {
	'th': 0.0356,
	'he': 0.0307,
	'in': 0.0243,
	'er': 0.0205,
	'an': 0.0199,
	're': 0.0185,
	'on': 0.0176,
	'at': 0.0149,
	'en': 0.0145,
	'nd': 0.0135,
	'ti': 0.0134,
	'es': 0.0134,
	'or': 0.0128,
	'te': 0.0120,
	'of': 0.0117,
	'ed': 0.0117,
	'is': 0.0113,
	'it': 0.0112,
	'al': 0.0109,
	'ar': 0.0107,
	'st': 0.0105,
	'to': 0.0104,
	'nt': 0.0104,
	'ng': 0.0095,
	'se': 0.0093,
	'ha': 0.0093,
	'as': 0.0087,
	'ou': 0.0087,
	'io': 0.0083,
	'le': 0.0083,
	've': 0.0083,
	'co': 0.0079,
	'me': 0.0079,
	'de': 0.0076,
	'hi': 0.0076,
	'ri': 0.0073,
	'ro': 0.0073,
	'ic': 0.0070,
	'ne': 0.0069,
	'ea': 0.0069,
	'ra': 0.0069,
	'ce': 0.0065,
	'li': 0.0062,
	'ch': 0.0060,
	'll': 0.0058,
	'be': 0.0058,
	'ma': 0.0057,
	'si': 0.0055,
	'om': 0.0055,
	'ur': 0.0054
	}

# Creating a dictionary to hold all possible keys, decrypted messages and chi-squared statistics
keys_dict = dict()
for j in range(0, 26):
	keys_dict[j] = ["", 0, cad.letter_dict(), cad.letter_dict(), 0, cad.bigram_dict(), cad.bigram_dict(), 0]

# Message
encrypted_text = input("Please enter the Caesar cipher-encrypted message you would like to decrypt? Messages should ideally be 30 characters or more. \n")
alpha_length = ef.get_message_length(encrypted_text)

# Standardising the chi-squared value for each letter to the message length
for letter, freq in english_lang_freq.items():
	english_lang_freq[letter] = round(freq * alpha_length, 4)

# Standardising the chi-squared value for each bigram to the message length
for bigram, freq in english_bigram_freq.items():
	english_bigram_freq[bigram] = round(freq * alpha_length, 4)

for shift_key in keys_dict.keys():
	# Using encrypter to return a possible message for each of the 26 keys
	(keys_dict[shift_key])[0] = enc.encrypt_message(encrypted_text, shift_key)
	
for key, message in keys_dict.items():
	# Dictionaries capturing ngram frequency in cipher text
	ciphertext_letter_freq = (keys_dict[key])[2]
	ciphertext_bigram_freq = (keys_dict[key])[5]

	# Dictionaries capturing the chi-squared value for each letter
	chi_squared_letter_values = (keys_dict[key])[3]
	chi_squared_bigram_values = (keys_dict[key])[6]

	message = list(message[0])
	bigram_list = ef.get_bigram_list(message)

	# Returning the chi-squared statistic for letters and bigrams
	chi_squared_letter_stat = ef.get_chi_squared_stat(ciphertext_freq = ciphertext_letter_freq, 
		chi_squared_values = chi_squared_letter_values, ngram_list = message, 
		english_ngrams_freq = english_lang_freq)

	chi_squared_bigram_stat = ef.get_chi_squared_stat(ciphertext_freq = ciphertext_bigram_freq, 
		chi_squared_values = chi_squared_bigram_values, ngram_list = bigram_list, 
		english_ngrams_freq = english_bigram_freq)
	
	# Storing the chi-squared stat for each key in its value-list
	(keys_dict[key])[7] = round((chi_squared_letter_stat * chi_squared_bigram_stat), 2)
	(keys_dict[key])[1] = chi_squared_letter_stat
	(keys_dict[key])[4] = chi_squared_bigram_stat

decrypted_flag = False
ef.message_decrypted_question(decrypted_flag, keys_dict, p = 7)


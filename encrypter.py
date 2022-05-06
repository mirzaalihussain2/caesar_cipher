# Set up
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 
	'g', 'h', 'i', 'j', 'k', 'l', 
	'm', 'n', 'o', 'p', 'q', 'r', 
	's', 't', 'u', 'v', 'w', 'x', 
	'y', 'z']

def get_key():
	# Ask the user for a key
	key = input("To set key, please enter an integer: ")

	# Ensure that key is an integer
	while True:
		try:
			key = int(key)
			break
		except ValueError:
			key = input("Please enter an integer: ")
			continue

	# Set key between 0 and 25
	while key > 25:
		key = key - 26
	while key < 0:
		key = key + 26
	
	return key
	
def encrypt_message(orig_message, key):
	""" Encrypt original message using key. """
	
	orig_message = orig_message.lower()
	encrypted_message = ""
	
	# Substituting original letters for encrypted letters using key
	for orig_letter in orig_message:
		if orig_letter.isalnum():
			if orig_letter in alphabet:
				orig_position = alphabet.index(orig_letter)
				encrypted_position = orig_position + key
				if encrypted_position > 25:
					encrypted_position = encrypted_position - 26
				encrypted_letter = alphabet[encrypted_position]
			else:
				encrypted_letter = orig_letter
			encrypted_message = encrypted_message + encrypted_letter
	
	# Return encrypted message
	return encrypted_message

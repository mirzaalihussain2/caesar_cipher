# Import modules
import encrypter as enc

# Asking for user input
orig_message = input("What message would you like to encrypt using a Caesar cipher? \n")

# Encrypting the user's input
print("\n")
key = enc.get_key()
encrypted_text = enc.encrypt_message(orig_message, key)

# Printing encrypted output
print("\n")
print("Your message, encrypted using a Caesar cipher with a shift of " 
		+ str(key) + ": \n" + encrypted_text)


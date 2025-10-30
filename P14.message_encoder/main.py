#encode a message and give encoding an id to be able to decode later
#decode a message with given id

#

from string import ascii_lowercase

letters = ascii_lowercase
numbers = '0123456789'
punctuation = ".,'!?"
coded_punctuation = '#+@$%'


def caesar_cipher(message: str, jump: int):
	new_msg = ''
	for item in message:
		#check if item is a letter
		if item in letters:
			#get index of the letter and create new index 
			index = letters.index(item)
			new_index = index + jump
			#check that the new index is valid
			while new_index > len(letters) - 1:
				new_index -= 26
			#add new letter to coded message
			new_msg += letters[new_index]
		#if item is not a letter, add a space
		else:
			new_msg += item

	return new_msg

def caesar_decipher(message: str, jump: int):
	while jump > 26:
		jump -= 26
	return caesar_cipher(message, 26 - jump)

#aol zbu pz zbuuf
def number_coder(message: str):
	index = 0
	new_msg = ''
	for item in message:
		if item in letters:
			if index % 2 == 0:
				i = letters.index(item)
				new_msg += str(i)
			else:
				new_msg += str(item)
			index += 1
		else:
			new_msg += str(item)
	return new_msg


def number_decoder(message: str):
	double_digits_index = False
	decoded_msg = ''
	for index, item in enumerate(message):
		if double_digits_index:
			double_digits_index = False
			continue
		if item in numbers:
			letter_index = item
			if index < len(message) - 1 and message[index + 1] in numbers:
				letter_index = message[index : index+ 2]
				double_digits_index = True
			letter = letters[int(letter_index)]
			decoded_msg += letter
		else:
			decoded_msg += item
	return decoded_msg

def punctuation_coder(message: str, punct1: str, punct2: str):
	new_msg = ''
	for item in message:
		if item in punct1:
			index = punct1.index(item)
			new_msg += punct2[index]
		else:
			new_msg += item
	return new_msg

def word_jumbler(message: str):
	words_list = message.split(' ')
	jumbled_list = []
	for word in words_list:
		if len(word) % 2 == 0:
			mid_index = int(len(word) / 2)
			jumbled = word[mid_index:] + word[:mid_index]
			jumbled_list.append(jumbled)
		else:
			jumbled_list.append(word[::-1])
	new_message = " ".join(jumbled_list)
	return new_message

def word_unjumbler(message: str):
	return word_jumbler(message)


def message_encoder(message: str, id: str):
	c_jump = id
	coded0 = punctuation_coder(message, punctuation, coded_punctuation)
	coded1 = caesar_cipher(coded0, c_jump)
	coded2 = number_coder(coded1)
	return coded2

def message_decoder(encrypted_message: str, id: str):
	c_jump = id
	decoded1 = number_decoder(encrypted_message)
	decoded2 = caesar_decipher(decoded1, c_jump)
	decoded3 = punctuation_coder(decoded2, coded_punctuation, punctuation)
	return decoded3




#coded = message_encoder("So this will be a test. Let's see how the coder manages, with this! It seems to be doing pretty well, at least so far, right?", 7)
#print(coded)

#decoded = message_decoder(coded, 7)
#print(decoded)

print(word_jumbler('These are all odd words'))
print(word_unjumbler('esehT era lla ddo sdrow'))
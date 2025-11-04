

"""
Description: 
	the message encoder receives a message and an id. The encoder outputs an encrypted version of the message
	that can be reverted back to the original message with the id. 

Restrictions:
- cannot use integers in initial message
- cannot use special symbols #+@$% in initial message

Suggestions:
- the message can be written with or without spaces 
(This is a message or ThisIsAMessage both work)
- the id should not be 0-3, as these are easier to decrpyt

 

"""

from string import ascii_lowercase

LETTERS = ascii_lowercase
NUMBERS = '0123456789'
punctuation = ".,'!?"
coded_punctuation = '#+@$%'


def caesar_cipher(message: str, jump: int):
	new_msg = ''
	for item in message:
		#check if item is a letter
		if item in LETTERS:
			#get index of the letter and create new index 
			index = LETTERS.index(item)
			new_index = index + jump
			#check that the new index is valid
			while new_index > len(LETTERS) - 1:
				new_index -= 26
			#add new letter to coded message
			new_msg += LETTERS[new_index]
		elif item == ' ':
			new_msg += '/'
		elif item == '/':
			new_msg += ' '
		#if item is not a letter or space, add item
		else:
			new_msg += item

	return new_msg


def caesar_decipher(message: str, jump: int):
	#make sure jump is a valid number for alphabet
	while jump > 26:
		jump -= 26
	#undo caesar cipher
	return caesar_cipher(message, 26 - jump)

def number_coder(message: str):
	index = 0
	new_msg = ''
	#iterate thorugh every item 
	for item in message:
		#check if item is a letter
		if item in LETTERS:
			#check if index is even
			if index % 2 == 0:
				#replace the letter by its index representation in alphabet
				i = LETTERS.index(item)
				new_msg += str(i)
			else:
				#if index is odd, add letter without changes
				new_msg += str(item)
			#update index
			index += 1
		#if item is not a letter, add item
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
		if item in NUMBERS:
			letter_index = item
			if index < len(message) - 1 and message[index + 1] in NUMBERS:
				letter_index = message[index : index+ 2]
				double_digits_index = True
			letter = LETTERS[int(letter_index)]
			decoded_msg += letter
		else:
			decoded_msg += item
	return decoded_msg

def punctuation_coder(message: str, punct1: str, punct2: str):
	new_msg = ''
	for item in message:
		#check if item is in first punctuation list
		if item in punct1:
			#convert item into coded or decoded punctuation
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

def convert_a(message: str, coded=True):
	converted = 'xaz'
	words_list = message.split(' ')
	for index, value in enumerate(words_list):
		if value == 'a' and coded:
			words_list[index] = converted
		elif value == converted and not coded:
			words_list[index] = 'a'
	new_message = ' '.join(words_list)
	return new_message
	
	


def message_encoder(message: str, id: str):
	c_jump = id
	coded0 = convert_a(message)
	coded1 = word_jumbler(coded0)
	coded2 = punctuation_coder(coded1, punctuation, coded_punctuation)
	coded3 = caesar_cipher(coded2, c_jump)
	coded4 = number_coder(coded3)
	return coded4

def message_decoder(encrypted_message: str, id: str):
	c_jump = id
	decoded1 = number_decoder(encrypted_message)
	decoded2 = caesar_decipher(decoded1, c_jump)
	decoded3 = punctuation_coder(decoded2, coded_punctuation, punctuation)
	decoded4 = word_jumbler(decoded3)
	decoded5 = convert_a(decoded4, False)
	return decoded5



#examples
if __name__ == '__main__':

	coded = message_encoder("How had she been so wrong? All her instincts and intuition completely failed her for the first time in her life. She had so heavily relied on both when making decisions up until this moment and she felt a seismic shift take place in her self-confidence. If she could be so completely wrong about something so simple as this, how could she make decisions about really important things taking place in her life? She wasn't sure what she should do next.", 11)
	print(coded)

	print()

	decoded = message_decoder(coded, 11)
	print(decoded)



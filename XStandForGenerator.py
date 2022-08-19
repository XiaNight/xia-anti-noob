import random
import string

from google_trans_new import google_translator

translate_urls = ["com", "co.kr", "at", "de", "ru", "ch", "fr", "es"]

translator = google_translator(url_suffix = translate_urls)

class XStandFor:

	texts = None
	raw_langs = None
	lang = []
	classified = {}

	def __init__(self):
		file1 = open('words60000.txt', 'r') 
		self.texts = file1.readlines()
		file1.close()

		file2 = open('langs.txt', 'r') 
		self.raw_langs = file2.readlines()
		file2.close()


		for i in range(len(self.texts)):
			self.texts[i] = self.texts[i].strip()

		for tlang in self.raw_langs:
			rawSplits = tlang.split('\'')
			self.lang.append(rawSplits[1])

		
		for text in self.texts:

			if text[0] not in self.classified:
				self.classified[text[0]] = []
			if '-' not in text:
				self.classified[text[0]].append(text)
		print('init done')

	def tryTranslate(self, words):
		filtered = ''
		temp = ''
		found = False
		for t in range(len(words)):
			if is_ascii(words[t]) and words[t] != ' ':
				if found == False:
					temp = ''
					found = True
				temp += words[t]
			else:
				if found:
					found = False
					translated = translator.translate(temp, lang_tgt='zh-tw')
					filtered += remove_ascii(translated)
				else:
					filtered += words[t]
		return filtered

	def idea_transformer(self, keyword, iterations = 5):
		return self.RandomTranslate(keyword, 'zh-tw', iterations)

	def fetch(self, keyword, times):
		output = ""
		for i in range(times):
			out = ""
			userInput = keyword.lower()

			result = []

			for char in userInput:
				result.append(self.GetRandomIndex(self.classified[char]))

			sentence = self.Merge(result)
			out += str(i+1) + '\t' + sentence + '\n'

			translations = translator.translate(sentence, lang_tgt='zh-tw')
			# filtered = self.tryTranslate(translations) # Try to translate un-translatable words.
			filtered = translations

			out += '\t' + filtered
			output += out + '\n\n'
		return output

	def Merge(self, LIST):
		output = ''
		for index in LIST:
			output += index + ' '
		return output

	def RandomTranslate(self, origin, target, iterations = 5):
		current = origin
		for i in range(iterations):
			targetLang = self.GetRandomIndex(self.lang)
			current = translator.translate(current, lang_tgt=targetLang)
		current = translator.translate(current, lang_tgt=target)
		return current

	def GetRandomIndex(self, LIST):
		rand = random.randint(0, len(LIST) - 1)
		return LIST[rand]

ascii = set(string.printable)
def is_ascii(s):
	return s in ascii
def is_not_ascii(s):
	return s not in ascii

def remove_non_ascii(s):
    return filter(lambda x: is_ascii(x), s)
def remove_ascii(s):
	output = ''
	for a in s:
		if a not in ascii:
			output += a
	return output

def merge_collection(c):
	output = ''
	for a in remove_non_ascii(c):
		output += a
	return output

def Main():

	XSF = XStandFor()
	userInput, times = input().split(' ')
	times = int(times)
	while(userInput != "-1"):
		print(XSF.fetch(userInput, times))

		userInput, times = input().split(' ')
		times = int(times)


if __name__ == '__main__':
	Main()
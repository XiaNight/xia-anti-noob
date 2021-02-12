import random

from google_trans_new import google_translator
translator = google_translator()  

class XStandFor:

	texts = None
	raw_langs = None
	lang = []
	classified = {}

	def __init__(self):
		file1 = open('words.txt', 'r') 
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
			self.classified[text[0]].append(text)
		print('init done')


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

			# translations = RandomTranslate(sentence, 'zh-tw')
			# for t in translations:
			# 	print(t)
			
			translations = translator.translate(sentence, lang_tgt='zh-tw')
			out += '\t' + translations
			output += out + '\n\n'
		return output

	def Merge(self, LIST):
		output = ''
		for index in LIST:
			output += index + ' '
		return output

	def RandomTranslate(self, origin, target, iterations = 5):
		current = origin
		translates = []
		for i in range(iterations):
			targetLang = GetRandomIndex(self.lang)
			current = translator.translate(current, lang_tgt=targetLang)
			translates.append(translator.translate(current, lang_tgt=target) + targetLang)
		return translates

	def GetRandomIndex(self, LIST):
		rand = random.randint(0, len(LIST) - 1)
		return LIST[rand]

if __name__ == '__main__':
	XSF = XStandFor()
	userInput, times = input().split(' ')
	times = int(times)
	while(userInput != "-1"):

		print(XSF.fetch(userInput, times))

		userInput, times = input().split(' ')
		times = int(times)
import random
import string

from google.cloud import translate
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file('credentials.json')

class XStandFor:

	texts = None
	raw_langs = None
	lang = []
	classified = {}
	client = None
	location = "global"
	parent = None
	project_id = "quickstartsheet-1613031202201"

	def __init__(self):
		self.InitialzeGoogleTranslate()

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
					translated = self.TranslateText(temp, "en-US", 'zh-tw')
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

			translations = self.TranslateText(sentence, "en-US", 'zh-tw')
			# filtered = self.tryTranslate(translations) # Try to translate un-translatable words.
			filtered = translations

			out += '\t' + filtered
			output += out + '\n\n'
		return output
	
	def InitialzeGoogleTranslate(self):
		self.client = translate.TranslationServiceClient(credentials=credentials)
		self.parent = f"projects/{self.project_id}/locations/{self.location}"
	
	def TranslateText(self, text, src, dest):
		response = self.client.translate_text(
		request={
			"parent": self.parent,
			"contents": [text],
			"mime_type": "text/plain",
			"source_language_code": src, # "en-US"
			"target_language_code": dest, # "es"
		})
		return response.translations[0].translated_text
	
	def Merge(self, LIST):
		output = ''
		for index in LIST:
			output += index + ' '
		return output

	def RandomTranslate(self, text, finalLanguage, iterations = 5):
		current = text
		lastLanguage = "en-US"
		for i in range(iterations):
			currentLanguage = self.GetRandomIndex(self.lang)
			current = self.TranslateText(current, lastLanguage, currentLanguage)
			lastLanguage = currentLanguage
		current = self.TranslateText(current, lastLanguage, finalLanguage)
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
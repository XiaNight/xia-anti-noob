import random
import sys

class PoemGenerator:
	texts = None
	length = None

	def __init__(self):
		with open("./Ch_1000.txt", 'r', encoding="utf8") as f:
			self.texts = f.readline()
			self.length = len(self.texts)
			print("Loaded", self.length, "texts")

	def GetCharacter(self):
		return self.texts[random.randrange(self.length)]

	def GetSentense(self, length, end = "，", lineEnd = False):
		output = ""
		for i in range(length):
			output += self.GetCharacter()
		output += end
		output += "\n" if lineEnd else ""
		return output

	def GetPoem(self, sentenseSize = 5, lineEnd = True):
		output = ""
		output += self.GetSentense(sentenseSize, "，", lineEnd)
		output += self.GetSentense(sentenseSize, "。", lineEnd)
		output += self.GetSentense(sentenseSize, "，", lineEnd)
		output += self.GetSentense(sentenseSize, "。", lineEnd)
		return output

	def GetScatterPoem(self, minSize = 3, maxSize = 9, sentenseSizeMin = 4, sentenseSizeMax = 12):
		sentenseSize = random.randrange(sentenseSizeMin, sentenseSizeMax)
		output = []
		for s in range(sentenseSize):
			size = random.randrange(minSize, maxSize)
			output.append(self.GetSentense(size, ""))
			pass
		output = "，".join(output) + "。"
		return output

if __name__ == "__main__":
	PG = PoemGenerator()
	print(PG.GetScatterPoem(4, 7, 4, 7))
	print(PG.GetPoem(4, False))
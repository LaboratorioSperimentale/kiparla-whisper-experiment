import json
import datetime

file_words = "output/Pasti_A.words.json"
file_text = "output/Pasti_A.text.annotato.txt"

words = json.load(open(file_words))

output = {}
turns = []

word_index = 0
speaker = ""
with open(file_text) as fin:
	for line in fin:
		linesplit = line.split("\t")
		curr_speaker, text = linesplit
		segmented_text = text.strip().split(" ")

		if len(curr_speaker) > 0:
			speaker = curr_speaker

		if not speaker in output:
			output[speaker] = []

		start = -1
		end = -1

		for i, word in enumerate(segmented_text):
			# print(i, word)
			unique_word = words[word_index]
			if word_index < len(words)-1: #TODO check
				word_index += 1

			output[speaker].append((word, unique_word["start"], unique_word["end"]))

			if i == 0:
				start = unique_word["start"]
			if i == len(segmented_text)-1:
				end = unique_word["end"]

		turns.append((speaker, text, start, end))



for speaker in output:
	with open(f"output/Pasti_A_speaker{speaker}.srt", "w") as fout:
		for word, begin, end in output[speaker]:
			begin_formatted = datetime.timedelta(seconds=begin)
			end_formatted = datetime.timedelta(seconds=end)
			print(f"{begin_formatted} --> {end_formatted}", file=fout)
			print(word, file=fout)
			print("", file=fout)


	with open(f"output/Pasti_A_turns_speaker{speaker}.srt", "w") as fout:
		for sp, text, begin, end in turns:
			if sp == speaker:
				begin_formatted = datetime.timedelta(seconds=begin)
				end_formatted = datetime.timedelta(seconds=end)
				print(f"{begin_formatted} --> {end_formatted}", file=fout)
				print(text, file=fout)
				print("", file=fout)


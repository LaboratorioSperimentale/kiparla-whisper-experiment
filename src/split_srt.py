import collections

words = []
file_words = "data/large_SBIM_prova.wav.words.srt"

file_words_content = open(file_words).readlines()
# print(file_words_content[:10])
# input()

times = [word.strip().split(" ") for i, word in enumerate(file_words_content) if i%4 == 1]
transcribed_words = [word.strip() for i, word in enumerate(file_words_content) if i%4 == 2]

words = []

for i in range(len(times)):
	words.append((transcribed_words[i], times[i][0], times[i][2]))


# print(words[:10])
# input()
	
	# for line in fin:
	# 	line = line.strip()

	# 	if len(line) == 0:
	# 		pass
	# 	elif len(line.split(" ")) == 1 and line[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
	# 		pass
	# 	elif line[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
	# 		start, _, end = line.split(" ")
	# 	else:
	# 		word = line.strip()

	# 		words.append((word, start, end))
	# 		# print(words)
	# 		# input()

disfluencies = []
for i, word in enumerate(words):
	word, start, end = word
	if word == "[*]":
		disfluencies.append(i)

merged_words = []
i = 0
while i < len(words):
	word_curr, start_curr, end_curr = words[i]

	if i in disfluencies:
		word_next, start_next, end_next = words[i+1]
		merged_words.append((f"{word_curr} {word_next}", start_curr, end_next))
		i += 2
	
	else:
		merged_words.append((word_curr, start_curr, end_curr))
		i+=1

# print(words[:10])

words = merged_words
# print(words[:10])
# input()
		

# print(disfluencies)
# input()



turns = []
srts = {}
i = 0

file_input = "data/annotated_large_SBIM_prova.wav.srt"

with open(file_input) as fin:
	for line in fin:
		line = line.strip()

		if len(line) == 0:
			pass
		elif line[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
			pass
		elif line[0] == "#":
			speaker = line
			if not speaker in srts:
				srts[speaker] = []
			# print("New turn", line)
		else:
			turn = line.split(" ")
			print(turn)
			# input()
			annotated_turn = []

			for el in turn:

				# while words[i] == "[*]":
				# 	i+=1
				
				annotated_turn.append(words[i])
				
				# input()
				i += 1
			print([x[0] for x in annotated_turn])
			# input()
			srts[speaker].append(annotated_turn)
			turns.append([speaker, annotated_turn[0][1], annotated_turn[-1][-1], turn])


srts_fout = {}
for speaker in srts:
	srts_fout[speaker] = open(f"output/{speaker}.srt", "w")

	# with open(f"output/{speaker}.srt", "w") as fout:
	# 	for turn in srts[speaker]:
	# 		for word, begin, end in turn:
	# 			print(f"{begin} --> {end}", file=fout)
	# 			print(word, file=fout)
	# 			print("", file=fout)


with open(f"output/SEGMENTS.srt", "w") as fout:
	i = 0
	w = 0

	for speaker, begin, end, segment in turns:
		# print(speaker, begin, end, ' '.join(segment))
		# input()

		pos_in_segment = 0
		while pos_in_segment < len(segment) and w < len(words):
			
			word = segment[pos_in_segment]
			pos_in_segment += 1

			listed_w, w_begin, w_end = words[w]
			w += 1

			# while listed_w == "[*]":
			# 	print(f"{w_begin} --> {w_end}", file=srts_fout[speaker])
			# 	print(listed_w, file=srts_fout[speaker])
			# 	print("", file=srts_fout[speaker])
			# 	listed_w, w_begin, w_end = words[w]
			# 	w+=1

			print(f"{w_begin} --> {w_end}", file=srts_fout[speaker])
			# print(word, file=srts_fout[speaker])
			print(listed_w, file=srts_fout[speaker])
			print("", file=srts_fout[speaker])

		
		print(f"{begin} --> {end}", file=fout)
		print(f"SEGMENT::{i} -- SPEAKER::{speaker} -- DEBUG::{' '.join(segment)}", file=fout)
		i += 1
		print("", file=fout)
		# input()
import tqdm

import whisper_timestamped as whisper
import json
import datetime


def transcribe_timestamped(input_files, output_folder, model_path,
						   language):

	model = whisper.load_model(model_path, device="cpu")

	for filename in tqdm.tqdm(input_files): #TODO add tqdm description
		stem = filename.stem
		audio = whisper.load_audio(filename)

		result = whisper.transcribe(model, audio, language=language)

		with open(output_folder.joinpath(f"{stem}.json"), "w", encoding="utf-8") as fout:
			print(json.dumps(result, indent = 2, ensure_ascii = False), file=fout)


def create_input(input_files, output_folder):

	for filename in tqdm.tqdm(input_files):
		stem = filename.stem
		data = json.load(open(filename, encoding="utf-8"))

		text = []
		words = []

		segments = data["segments"]
		for segment in segments:
			text_string = segment["text"].split(" ")
			text.append(" ".join(x.strip(".,?!").lower() for x in text_string))
			for w in segment["words"]:
				w["text"] = w["text"].strip(".,?!").lower()
				words.append(w)

		with open(output_folder.joinpath(f"{stem}.text.txt"), "w", encoding="utf-8") as fout:
			for t in text:
				print(f"\t{t.strip()}", file=fout)

		print(json.dumps(words, indent = 2, ensure_ascii = False),
		file=open(output_folder.joinpath(f"{stem}.words.json"), "w", encoding="utf-8"))


def produce_srt(input_files, words_files, output_folder):

	for filename in input_files:
		print(filename)
		stem = filename.stem[:-5]
		words_file = ""

		for word_filename in words_files:
			stem_word = word_filename.stem[:-6]

			if stem_word == stem:
				words_file = word_filename

		words = json.load(open(words_file, encoding="utf-8"))

		output = {}
		turns = []

		word_index = 0
		speaker = ""

		with open(filename, encoding="utf-8") as fin:
			for lineno, line in enumerate(fin):
				linesplit = line.split("\t")
				print(linesplit)
				curr_speaker, text = linesplit
				segmented_text = text.strip().split(" ")

				if len(curr_speaker) > 0:
					speaker = curr_speaker

				if speaker not in output:
					output[speaker] = []

				start = -1
				end = -1

				for i, word in enumerate(segmented_text):
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
			# with open(f"output/Pasti_A_speaker{speaker}.srt", "w") as fout:
			# 	for word, begin, end in output[speaker]:
			# 		begin_formatted = datetime.timedelta(seconds=begin)
			# 		end_formatted = datetime.timedelta(seconds=end)
			# 		print(f"{begin_formatted} --> {end_formatted}", file=fout)
			# 		print(word, file=fout)
			# 		print("", file=fout)

			with open(output_folder.joinpath(f"{stem}_turns_speaker{speaker}.srt"),
			 		"w", encoding="utf-8") as fout:
				for sp, text, begin, end in turns:
					if sp == speaker:
						begin_formatted = datetime.timedelta(seconds=begin)
						end_formatted = datetime.timedelta(seconds=end)
						print(f"{begin_formatted} --> {end_formatted}", file=fout)
						print(text, file=fout)
						print("", file=fout)
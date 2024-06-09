import csv

import kit.utils as u

def count_tokens(participant_timestamps, input_files, output_fname):

	participants_data = {}
	transcribed_tokens = {}

	with open(participant_timestamps, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		header = reader.__next__()
		header = [x.strip() for x in header]
		for row in reader:
			d = dict(zip(header, row))
			# print(d)
			participants_data[d["Code"]] = d
			transcribed_tokens[d["Code"]] = {"Code": d["Code"],
											"Phase": d["Phase"],
											"T1": 0,
											"T2": 0,
											"T3": 0,
											"T4": 0}


	for file in input_files:
		basename = file.stem
		# print(basename)
		worker_name = basename.split("_")[-1][-1]

		timestamps = [float(participants_data[worker_name]["T1"]),
					  float(participants_data[worker_name]["T2"]),
				      float(participants_data[worker_name]["T3"]),
					  100000000]

		# print(timestamps)

		texts = []

		i=0
		with open(file, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')
			header = reader.__next__()
			cur_text = []
			for row in reader:
				d = dict(zip(header, row))

				cur_t = float(d["end"])

				if cur_t <= timestamps[i]:
					cur_text.append(d["ortographic-text"])
				else:
					texts.append(cur_text)
					cur_text = [d["ortographic-text"]]
					i += 1

			texts.append(cur_text)

		count = 0
		for label, text in zip(["T1", "T2", "T3", "T4"], texts):
			for sent in text:
				count += len(sent.split(" "))
			transcribed_tokens[worker_name][label] = count

		# print(transcribed_tokens)
		# input()


	with open(output_fname, "w", newline='') as csvfile:
		header = ["Code", "Phase", "T1", "T2", "T3", "T4"]
		writer = csv.DictWriter(csvfile, fieldnames=header)
		writer.writeheader()
		for code in transcribed_tokens:
			writer.writerow(transcribed_tokens[code])


def count_tokens_per_minute(input_files, output_fname):

	data = {}

	max_seconds = 0

	for file in input_files:
		basename = file.stem
		# print(basename)
		worker_name = basename.split("_")[-1][-1]
		data[worker_name] = {"Code": worker_name, "times": []}

		# print(timestamps)

		texts = []

		sec_threshold = 60

		with open(file, newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')
			header = reader.__next__()
			cur_text = []
			for row in reader:
				d = dict(zip(header, row))

				cur_t = float(d["end"])

				if cur_t <= sec_threshold:
					cur_text.append(d["ortographic-text"])
				else:
					texts.append(cur_text)
					cur_text = [d["ortographic-text"]]
					sec_threshold += 60
					if sec_threshold > max_seconds:
						max_seconds = sec_threshold

			# texts.append(cur_text)

		count = 0
		for text in texts:
			for sent in text:
				count += len(sent.split(" "))
			data[worker_name]["times"].append(count)

		for worker in data:
			j=0
			for i in range(60, max_seconds, 60):
				data[worker][str(i)] = 0
				if j<len(data[worker]["times"]):
					data[worker][str(i)] = data[worker]["times"][j]
					j+=1

	with open(output_fname, "w", newline='') as csvfile:
		header = ["Code"]
		header.extend([str(x) for x in range(60, max_seconds, 60)])
		writer = csv.DictWriter(csvfile, fieldnames=header, extrasaction='ignore')
		writer.writeheader()
		for code in data:
			writer.writerow(data[code])


def verticalize(f_input, f_output, key):

	fout = open(f_output, "w")

	with open(f_input, newline="") as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		header = reader.__next__()
		# header = [x.strip() for x in header]

		for row in reader:
			d = dict(zip(header, row))
			# print(d)
			speaker = d["Speaker"]
			start = d["start"]
			end = d["end"]
			if key == "ortographic-text":
				text = d["ortographic-text"].strip().split(" ")
			else:
				# print(d["jefferson-text"])
				text = u.simplify_json(d["jefferson-text"]).strip().split(" ")
				# print(text)
				# input()

			for word in text:
				print(f"{speaker}\t{start}\t{end}\t{word}", file=fout)
			# input()


def verticalize_batch(files_input, output_folder, key):

	for filename in files_input:
		basename = filename.stem
		output_fname = output_folder.joinpath(f"{basename}.vert.csv")

		verticalize(filename, output_fname, key)

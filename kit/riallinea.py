import json
import datetime
import time
import collections

import lis as lis


def allinea(text1, text2):

	text1_fqdist = collections.defaultdict(int)
	text2_fqdist = collections.defaultdict(int)

	for w in text1:
		text1_fqdist[w]+=1
	for w in text2:
		text2_fqdist[w]+=1

	text1_fingerprint = []
	text2_fingerprint = []
	for i, w in enumerate(text1):
		if text1_fqdist[w] == 1:
			text1_fingerprint.append((i, w))
	for i, w in enumerate(text2):
		if text2_fqdist[w] == 1:
			text2_fingerprint.append((i, w))


	allineamento = {}
	allineamento_rev = {}
	for i, w1 in text1_fingerprint:
		found = -1
		for j, w2 in text2_fingerprint:
			if w1 == w2:
				found = j
				break
		if found > -1:
			allineamento[i] = found
			allineamento_rev[found] = i

	ys = [y for x, y in allineamento.items()]
	len_lis, seq_lis = lis.lis(ys)
	seq_lis = list(seq_lis)

	i=0

	indexes_1 = []
	indexes_2 = []
	for i_1, i_2 in allineamento.items():
		if i_2 == seq_lis[i]:
			indexes_1.append(i_1)
			indexes_2.append(i_2)
			i+=1

	offsets_1 = [indexes_1[0]]
	offsets_2 = [indexes_2[0]]

	for i, j in zip(indexes_1, indexes_2):
		if i>offsets_1[-1]+5 and j>offsets_2[-1]+5:
			offsets_1.append(i)
			offsets_2.append(j)

	print(allineamento)
	print(offsets_1)
	print(offsets_2)

if __name__ == "__main__":

	text1 = []
	with open("/home/ludovica/Documents/GitHub/kiparla-whisper-experiment/data/Fase1_vert_json/ParlaBOA_workerE.vert.csv") as fin:
		for line in fin:
			line = line.strip().split("\t")
			if len(line)>3:
				text1.append(line[-1])
	text2 = []
	with open("/home/ludovica/Documents/GitHub/kiparla-whisper-experiment/data/Fase2_vert_json/ParlaBOA_workerI.vert.csv") as fin:
		for line in fin:
			line = line.strip().split("\t")
			if len(line)>3:
				text2.append(line[-1])

	allinea(text1[:500], text2[:500])

	from sequence_align.pairwise import hirschberg, needleman_wunsch

	aligned_seq_a, aligned_seq_b = needleman_wunsch(
		text1[:500],
		text2[:500],
		match_score=1.0,
		mismatch_score=-2.0,
		indel_score=-1.0,
		gap="_",
	)

	for w1, w2 in zip(aligned_seq_a, aligned_seq_b):
		print(w1, w2)
		# input()

	# Expects ["G", "_", "A", "T", "T", "A", "C", "A"]
	# print(aligned_seq_a)

	# Expects ["G", "C", "A", "_", "T", "G", "C", "G"]
	# print(aligned_seq_b)

# ys = [y for x, y in ipotesi_allineamento.items()]
# print(ys)
# len_lis, seq_lis = lis.lis(ys)

# allineamento = [(ipotesi_allineamento_rev[x], x) for x in seq_lis]
# print(allineamento)

# portions = []

# old_x, old_y = -1, -1
# for x, y in allineamento:
# 	whisper_portion = []
# 	tot_portion = []


# print(len(whisper_words))
# print(len(tot_words))

########################################
# file_words = "output/ParlaBO_A.words.json"
# whisper_words = json.load(open(file_words))

# file_srt_A = "output/ParlaBO_A_A.sistemato.srt"
# file_srt_B = "output/ParlaBO_A_B.sistemato.srt"
# tot_words = []

# for speaker, filename in [("A", file_srt_A), ("B", file_srt_B)]:
# 	with open(filename) as fin:
# 		lines = fin.readlines()
# 		i=0

# 		while i < len(lines):
# 			line = lines[i]
# 			if i%4==0:
# 				pass
# 			elif i%4==1:
# 				times = line.strip().split(" ")
# 				begin,_, end = times
# 				floatpart_begin = int(begin.split(",")[1])/1000
# 				floatpart_end = int(end.split(",")[1])/1000

# 				begin = time.strptime(begin,'%H:%M:%S,%f')
# 				end = time.strptime(end, '%H:%M:%S,%f')

# 				total_begin = datetime.timedelta(hours=begin.tm_hour,minutes=begin.tm_min,seconds=begin.tm_sec).total_seconds()
# 				total_end = datetime.timedelta(hours=end.tm_hour,minutes=end.tm_min,seconds=end.tm_sec).total_seconds()
# 				#TIME STAMPS
# 				# print("TIME:", line, total_begin+floatpart_begin, total_end+floatpart_end)

# 			elif i%4==2:
# 				words = line.strip().split(" ")

# 				for n_w, w in enumerate(words):

# 					w_pulito = w
# 					for sym in "[]().?!:°-~":
# 						w_pulito = w_pulito.replace(sym, "")

# 					annotated_w = {"text": w_pulito,
# 									"jefferson": w,
# 									"start": total_begin,
# 									"end": total_end,
# 									"speaker": speaker}

# 					if n_w == 0:
# 						annotated_w["start"] = total_begin
# 					if n_w == len(words)-1:
# 						annotated_w["end"] = total_end
# 					tot_words.append(annotated_w)


# 				# print("WORDS:", line)

# 			else:
# 				pass

# 			# input()
# 			i+=1

# tot_words = sorted(tot_words, key=lambda x: x["start"])

# whisper_str = [x["text"] for x in whisper_words]
# tot_str = [x["text"] for x in whisper_words]

# whisper_freqdist = collections.defaultdict(int)
# tot_freqdist = collections.defaultdict(int)

# for w in whisper_str:
# 	whisper_freqdist[w]+=1
# for w in tot_str:
# 	tot_freqdist[w]+=1

# whisper_fingerprint = []
# tot_fingerprint = []

# for i, w in enumerate(whisper_str):
# 	if whisper_freqdist[w] == 1 and whisper_words[i]["confidence"] > 0.9:
# 		whisper_fingerprint.append((i, whisper_words[i]))

# for i, w in enumerate(tot_str):
# 	if tot_freqdist[w] == 1:
# 		tot_fingerprint.append((i, tot_words[i]))


# print(json.dumps(tot_words, indent=2, ensure_ascii=False), file=open("output/prova_allineamento.json", "w"))
# print(json.dumps(whisper_fingerprint, indent=2, ensure_ascii=False), file=open("output/prova_allineamento_whisperfingerprint.json", "w"))
# print(json.dumps(tot_fingerprint, indent=2, ensure_ascii=False), file=open("output/prova_allineamento_totfingerprint.json", "w"))


# print(json.dumps(tot_words, indent=2, ensure_ascii=False), file=open("output/prova_allineamento.json", "w"))


# ipotesi_allineamento = {}
# ipotesi_allineamento_rev = {}

# for i, ww in whisper_fingerprint:
# 	found = -1
# 	for j, tw in tot_fingerprint:
# 		if ww["text"] == tw["text"]:
# 			found = j

# 	if found > -1:
# 		ipotesi_allineamento[i] = found
# 		ipotesi_allineamento_rev[found] = i


# ys = [y for x, y in ipotesi_allineamento.items()]
# print(ys)
# len_lis, seq_lis = lis.lis(ys)

# allineamento = [(ipotesi_allineamento_rev[x], x) for x in seq_lis]
# print(allineamento)

# portions = []

# old_x, old_y = -1, -1
# for x, y in allineamento:
# 	whisper_portion = []
# 	tot_portion = []


# print(len(whisper_words))
# print(len(tot_words))

# # for x, y in allineamento:
# # 	print(x, whisper_words[x])
# # 	print(y, tot_words[y])
# # 	print("---")
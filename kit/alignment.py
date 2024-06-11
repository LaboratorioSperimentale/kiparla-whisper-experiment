import collections

from sequence_align.pairwise import hirschberg, needleman_wunsch

import kit.lis as lis


def find_matching_subsequence(text1, text2):

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

def align(seq_a, seq_b, match_score=1, mismatch_score=-1, indel_score=-0.5):

    aligned_seq_a, aligned_seq_b = needleman_wunsch(
        seq_a,
        seq_b,
        match_score=1.0,
        mismatch_score=-1.0,
        indel_score=-1.0,
        gap="_",
    )

    score_seq = []
    for x, y in zip(aligned_seq_a, aligned_seq_b):
        if x == y:
            score_seq.append(0)
        elif x == "_" or y == "_":
            score_seq.append(0.5)
        else:
            score_seq.append(1)

    tot_score = sum(score_seq)/len(score_seq)

    return aligned_seq_a, aligned_seq_b, score_seq, tot_score
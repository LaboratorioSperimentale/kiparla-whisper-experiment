# Or use strings, lists, etc
seq1, seq2 = "ciao come stai io sono Ludovica Pannitto", "ciao come stai ? io mi chiamo Ludovica"
seq1, seq2 = seq1.split(), seq2.split()

from sequence_align.pairwise import hirschberg, needleman_wunsch


# See https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm#/media/File:Needleman-Wunsch_pairwise_sequence_alignment.png
# Use Needleman-Wunsch default scores (match=1, mismatch=-1, indel=-1)
seq_a = seq1
seq_b = seq2

aligned_seq_a, aligned_seq_b = needleman_wunsch(
    seq_a,
    seq_b,
    match_score=1.0,
    mismatch_score=-1.0,
    indel_score=-1.0,
    gap="_",
)

# Expects ["G", "_", "A", "T", "T", "A", "C", "A"]
print(aligned_seq_a)

# Expects ["G", "C", "A", "_", "T", "G", "C", "G"]
print(aligned_seq_b)


# See https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm#Example
# seq_a = ["A", "G", "T", "A", "C", "G", "C", "A"]
# seq_b = ["T", "A", "T", "G", "C"]

aligned_seq_a, aligned_seq_b = hirschberg(
    seq_a,
    seq_b,
    match_score=2.0,
    mismatch_score=-1.0,
    indel_score=-2.0,
    gap="_",
)

# Expects ["A", "G", "T", "A", "C", "G", "C", "A"]
print(aligned_seq_a)

# Expects ["_", "_", "T", "A", "T", "G", "C", "_"]
print(aligned_seq_b)
import re


#TENERE------ , Intonazione debolmente ascendente
#TENERE------ >ciao< Pronuncia più rapida
#TENERE------ . Intonazione discendente
#TENERE------ <ciao> Pronuncia più lenta
#TENERE------ : Suono prolungato
#TENERE------ [ciao] Sovrapposizione tra parlanti
#TENERE------ (.) Pausa breve

# ((ride)) Comportamento non verbale
# (ciao) sequenza di difficile comprensione (ipotesi del trascrittore)

#TENERE------ = Unità legate prosodicamente
#TENERE------ xxx sequenza non comprensibile (idealmente, ad ogni x corrisponde una sillaba)
#TENERE------ °ciao° Volume più basso
#TENERE------ CIAO Volume più alto

def get_ortographic(text):

	symbols = [",", ".", ":", "<", ">", "[", "]", "°", "(", ")", "#"]
	# print(text)
	text = text.lower()
	# print(text)
	text = re.sub(r" ?\(\.\) ?", " ", text, count=10)
	# print(text)
	text = re.sub(r" ?\(\([^\)]*\)\) ?", " ", text, count=10)
	text = re.sub(r"\bx+\b", "UNK", text, count=10)
	# print(text)
	for sym in symbols:
		text = text.replace(sym, "")
	# print(text)
	text = text.replace("=", " ")

	return text
	# print(text)

	# input()

def simplify_json(text):
	text = re.sub(r" ?\(\.\) ?", " @@@ ", text, count=10)
	text = re.sub(r" ?\(\([^\)]*\)\) ?", " ", text, count=10)
	text = text.replace("(", "")
	text = text.replace(")", "")
	text = re.sub(r" @@@ ", " (.) ", text, count=10)

	return text


def load(filename, cutoff_threshold):
	ret = []
	with open(filename) as fin:
		for line in fin:
			line = line.strip().split("\t")
			if float(line[3])<=cutoff_threshold:
				ret.append(line[-1])

	return ret

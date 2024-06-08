import re


#------ , Intonazione debolmente ascendente
# cia- Parola interrotta
#------ ? Intonazione ascendente
#------ >ciao< Pronuncia più rapida
#------ . Intonazione discendente
#------ <ciao> Pronuncia più lenta
#------ : Suono prolungato
#------ [ciao] Sovrapposizione tra parlanti
#------ (.) Pausa breve
# (ciao) sequenza di difficile comprensione (ipotesi del trascrittore)
#------ = Unità legate prosodicamente
#------ xxx sequenza non comprensibile (idealmente, ad ogni x corrisponde una sillaba)
#------ °ciao° Volume più basso
# ((ride)) Comportamento non verbale
#------ CIAO Volume più alto

def get_ortographic(text):

	symbols = [",", ".", ":", "<", ">", "[", "]", "°", "(", ")"]
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
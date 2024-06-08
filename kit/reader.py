from speach import elan
import csv
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
	# print(text)
	for sym in symbols:
		text = text.replace(sym, "")
	# print(text)
	text = text.replace("=", " ")

	return text
	# print(text)

	# input()


with open('data/eaf/prova.eaf', encoding='utf-8') as eaf_stream:
	eaf = elan.parse_eaf_stream(eaf_stream)

	text = eaf.to_csv_rows()
	timesorted_text = sorted(text, key=lambda x: float(x[2]))

	with open("data/eaf/prova.csv", "w") as fout:
		fieldnames = ["Speaker", "start", "end", "span", "jefferson-text", "ortographic-text"]
		writer = csv.DictWriter(fout, fieldnames=fieldnames)
		writer.writeheader()
		for row in timesorted_text:
			d = {"Speaker": row[0],
			 	"start": row[2],
				"end": row[3],
				"span": row[4],
				"jefferson-text": row[5],
				"ortographic-text": get_ortographic(row[5])
			}
			writer.writerow(d)
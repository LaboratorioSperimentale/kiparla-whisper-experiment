import json

input_file = "output/Pasti_A.json"
id = "Pasti_A"

data = json.load(open(input_file))

# print(data)
text = []
words = []

segments = data["segments"]
for segment in segments:
	text_string = segment["text"].split(" ")
	text.append(" ".join(x.strip(".,?!").lower() for x in text_string))
	for w in segment["words"]:
		w["text"] = w["text"].strip(".,?!").lower()
		words.append(w)

# print(words)

with open("output/Pasti_A.text.txt", "w") as fout:
	for t in text:
		print(f"\t{t.strip()}", file=fout)


print(json.dumps(words, indent = 2, ensure_ascii = False), file=open("output/Pasti_A.words.json", "w"))

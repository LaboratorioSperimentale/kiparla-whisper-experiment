import argparse
from pathlib import Path

import tqdm

import kit.transcribe as transcribe

def _transcribe_data(args):
	input_files = Path(args.input_dir).glob("*.wav")
	output_folder = Path(args.output_dir)
	transcribe.transcribe_timestamped(input_files, output_folder,
								   Path(args.model), args.language)


def _create_input(args):
	input_files = Path(args.input_dir).glob("*.json")
	output_folder = Path(args.output_dir)
	transcribe.create_input(input_files, output_folder)


def _produce_srt(args):
	input_files = list(Path(args.input_dir).glob("*.text.txt"))
	words_files = list(Path(args.input_dir).glob("*.words.json"))

	print(input_files)
	print(words_files)
	output_folder = Path(args.output_dir)
	transcribe.produce_srt(input_files, words_files, output_folder)

if __name__ == "__main__":

	parent_parser = argparse.ArgumentParser(add_help=False)

	root_parser = argparse.ArgumentParser(prog='kit', add_help=True)
	subparsers = root_parser.add_subparsers(title="actions", dest="actions")

	parser_processdata = subparsers.add_parser('transcribe', parents=[parent_parser],
											   description='run whisper model',
											   help='run whisper model')
	parser_processdata.add_argument("-o", "--output-dir", default="output/",
								   help="path to output dir, default is output/")
	parser_processdata.add_argument("-i", "--input-dir",
									help="path to folder containing audio files in .wav format")
	parser_processdata.add_argument("-m", "--model", default="models/medium.pt",
									help="path to model file")
	parser_processdata.add_argument("-l", "--language", default="it")
	parser_processdata.set_defaults(func=_transcribe_data)

	parser_input = subparsers.add_parser("create-input", parents=[parent_parser],
										description='create input for human annotators',
										help='create input for human annotators')
	parser_input.add_argument("-o", "--output-dir", default="annotators_input/",
							help="path to output dir, default is annotators_input/")
	parser_input.add_argument("-i", "--input-dir", default="output/",
							help="path to folder containing whisper transcriptions in json format")
	parser_input.set_defaults(func=_create_input)

	parser_produce = subparsers.add_parser("produce-srt", parents=[parent_parser],
										  description='produce srt for elan import',
										  help='produce srt for elan import')
	parser_produce.add_argument("-o", "--output-dir", default="output_srts/",
								help="path to output dir, default is output_srts/")
	parser_produce.add_argument("-i", "--input-dir", default="annotators_input",
							 	help="folder containing text documents annotated with speaker on first column")
	parser_produce.set_defaults(func=_produce_srt)

	args = root_parser.parse_args()

	if "func" not in args:
		root_parser.print_usage()
		exit()

	args.func(args)

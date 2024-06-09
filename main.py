import argparse
import csv
from pathlib import Path

import tqdm

import kit.transcribe as transcribe
import kit.stats as stats

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


def _convert_eaf(args):
	input_files = list(Path(args.input_dir).glob("*.eaf"))

	output_folder = Path(args.output_dir)
	transcribe.convert_eaf(input_files, output_folder)


def _count_tokens(args):

	input_files = list(Path(args.input_dir).glob("*.csv"))
	output_fname = Path(args.output_fname)

	participant_timestamps = args.timestamps

	stats.count_tokens(participant_timestamps, input_files, output_fname)


def _count_tokens_per_minute(args):

	input_files = list(Path(args.input_dir).glob("*.csv"))
	output_fname = Path(args.output_fname)


	stats.count_tokens_per_minute(input_files, output_fname)


def _verticalize(args):

	stats.verticalize(Path(args.input_fname), Path(args.output_fname), args.key)


def _verticalize_batch(args):

	input_files = list(Path(args.input_dir).glob("*.csv"))
	output_folder = Path(args.output_dir)

	stats.verticalize_batch(input_files, output_folder, args.key)


def _align(args):
	pass



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

	parser_convert = subparsers.add_parser("convert-eaf", parents=[parent_parser],
										  description='convert eaf to csv',
										  help='convert eaf to csv')
	parser_convert.add_argument("-i", "--input-dir")
	parser_convert.add_argument("-o", "--output-dir")
	parser_convert.set_defaults(func=_convert_eaf)

	parser_tokens = subparsers.add_parser("count-tokens", parents=[parent_parser],
									   	  description='count number of transcribed tokens',
										  help='count number of transcribed tokens')
	parser_tokens.add_argument("-t", "--timestamps", help="path to csv file containing transcription times")
	parser_tokens.add_argument("-i", "--input-dir", help="path to dir containing input files")
	parser_tokens.add_argument("-o", "--output-fname", help="path to file for saving output")
	parser_tokens.set_defaults(func=_count_tokens)

	parser_tokens = subparsers.add_parser("count-tokens-perminute", parents=[parent_parser],
									   	  description='count number of transcribed tokens per minute',
										  help='count number of transcribed tokens per minute')
	parser_tokens.add_argument("-i", "--input-dir", help="path to dir containing input files")
	parser_tokens.add_argument("-o", "--output-fname", help="path to file for saving output")
	parser_tokens.set_defaults(func=_count_tokens_per_minute)

	parser_verticalize = subparsers.add_parser("verticalize", parents=[parent_parser],
											help="verticalize ortographic transcription",
											description="verticalize ortographic transcription")
	parser_verticalize.add_argument("-i", "--input-fname")
	parser_verticalize.add_argument("-o", "--output-fname")
	parser_verticalize.add_argument("--key", choices=["ortographic-text", "jefferson-text"])
	parser_verticalize.set_defaults(func=_verticalize)

	parser_verticalizeb = subparsers.add_parser("verticalize-batch", parents=[parent_parser],
											help="verticalize ortographic transcription",
											description="verticalize ortographic transcription")
	parser_verticalizeb.add_argument("-i", "--input-dir")
	parser_verticalizeb.add_argument("-o", "--output-dir")
	parser_verticalizeb.add_argument("--key", choices=["ortographic-text", "jefferson-text"])
	parser_verticalizeb.set_defaults(func=_verticalize_batch)

	parser_align = subparsers.add_parser("align", parents=[parent_parser],
									  help="compute alignments between verticalized files",
									  description="compute alignments between verticalized files")
	parser_align.add_argument("--input-dir-1", help="input dir phase 1")
	parser_align.add_argument("--input-dir-2", help="input dir phase 2")
	parser_align.add_argument("--whisper-dir")
	parser_align.add_argument("--transcription-times-1")
	parser_align.add_argument("--transcription-times-2")
	parser_align.set_defaults(func=_align)

	args = root_parser.parse_args()

	if "func" not in args:
		root_parser.print_usage()
		exit()

	args.func(args)

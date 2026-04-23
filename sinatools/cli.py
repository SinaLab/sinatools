import argparse
import importlib


COMMANDS = {
    "install_env": {
        "module": "sinatools.install_env",
        "help": "Create the SinaTools environment.",
    },
    "arStrip": {
        "module": "sinatools.CLI.utils.arStrip",
        "help": "Strip Arabic text features.",
    },
    "jaccard_similarity": {
        "module": "sinatools.CLI.utils.jaccard",
        "help": "Compute Jaccard similarity.",
    },
    "implication": {
        "module": "sinatools.CLI.utils.implication",
        "help": "Measure word implication.",
    },
    "sentence_tokenizer": {
        "module": "sinatools.CLI.utils.sentence_tokenizer",
        "help": "Split text into sentences.",
    },
    "transliterate": {
        "module": "sinatools.CLI.utils.text_transliteration",
        "help": "Transliterate text.",
    },
    "morphology_analyzer": {
        "module": "sinatools.CLI.morphology.morph_analyzer",
        "help": "Run morphology analysis.",
    },
    "alma_multi_word": {
        "module": "sinatools.CLI.morphology.ALMA_multi_word",
        "help": "Analyze ALMA multi-word expressions.",
    },
    "entity_extractor": {
        "module": "sinatools.CLI.ner.entity_extractor",
        "help": "Extract named entities.",
    },
    "remove_punctuation": {
        "module": "sinatools.CLI.utils.remove_punctuation",
        "help": "Remove punctuation from text.",
    },
    "remove_latin": {
        "module": "sinatools.CLI.utils.remove_latin",
        "help": "Remove Latin characters.",
    },
    "wsd": {
        "module": "sinatools.CLI.wsd.disambiguator",
        "help": "Run word sense disambiguation.",
    },
    "corpus_tokenizer": {
        "module": "sinatools.CLI.utils.corpus_tokenizer",
        "help": "Tokenize a text corpus.",
    },
    "appdatadir": {
        "module": "sinatools.CLI.DataDownload.get_appdatadir",
        "help": "Print the SinaTools data directory.",
    },
    "download_files": {
        "module": "sinatools.CLI.DataDownload.download_files",
        "help": "Download required data files.",
    },
    "corpus_entity_extractor": {
        "module": "sinatools.CLI.ner.corpus_entity_extractor",
        "help": "Extract entities from a corpus CSV.",
    },
    "text_dublication_detector": {
        "module": "sinatools.CLI.utils.text_dublication_detector",
        "help": "Detect duplicate text in CSV data.",
    },
    "evaluate_synonyms": {
        "module": "sinatools.CLI.synonyms.evaluate_synonyms",
        "help": "Evaluate a synonym set.",
    },
    "extend_synonyms": {
        "module": "sinatools.CLI.synonyms.extend_synonyms",
        "help": "Extend a synonym set.",
    },
    "semantic_relatedness": {
        "module": "sinatools.CLI.semantic_relatedness.compute_relatedness",
        "help": "Compute semantic relatedness.",
    },
    "relation_extractor": {
        "module": "sinatools.CLI.relations.relation_extractor",
        "help": "Extract relations from text.",
    },
}


def build_parser():
    parser = argparse.ArgumentParser(prog="sinatools", description="SinaTools command line interface.")
    subparsers = parser.add_subparsers(dest="command", title="commands", metavar="command")

    for name, metadata in COMMANDS.items():
        subparser = subparsers.add_parser(name, help=metadata["help"], add_help=False)
        subparser.set_defaults(module_name=metadata["module"])

    return parser


def main(argv=None):
    parser = build_parser()
    args, command_argv = parser.parse_known_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    module = importlib.import_module(args.module_name)
    return module.main(command_argv)


if __name__ == "__main__":
    main()

import argparse
from sinatools.synonyms.synonyms_generator import extend_synonyms

def main():
    parser = argparse.ArgumentParser(description='Morphological Analysis using SinaTools')
      
    parser.add_argument('--synset', type=str, help='Set of synonyms seperated by |')
    parser.add_argument('--level', type=int, help='The depth of edges the algorithm needs to reach')

    args = parser.parse_args()

    if args.synset is None and args.level is None:
        print("Error: Either --synset or --level argument must be provided.")
        return

    results = extend_synonyms(args.synset, args.level)

    print(results)

if __name__ == '__main__':
    main()

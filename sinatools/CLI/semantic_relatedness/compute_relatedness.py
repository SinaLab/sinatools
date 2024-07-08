import argparse
from sinatools.semantic_relatedness.compute_relatedness import get_similarity_score

def main():
    parser = argparse.ArgumentParser(description='Computes the degree of association between two sentences across various dimensions, meaning, underlying concepts, domain-specificity, topic overlap, viewpoint alignment.')
      
    parser.add_argument('--sentence1', type=str, help='The first sentence to be compute similarity based on')
    parser.add_argument('--sentence2', type=str, help='The second sentence to be compute similarity based on')
    

    args = parser.parse_args()

    if args.sentence1 is None and args.sentence2 is None:
        print("Error: Either --sentence1 or --sentence2 argument must be provided.")
        return

    score = get_similarity_score(args.sentence1, args.sentence2)

    print(score)

if __name__ == '__main__':
    main()

import argparse 
import re
from typing import List, Tuple
from collections import Counter
import random

def tokenize_sample(content: str) -> List[str]:
    text = re.sub(r'[^\w\s</>]','',content.lower()) 
    return text.split()

def main():
    parser = argparse.ArgumentParser(description='This is a n-grams model command line')
    parser.add_argument('filename', type=str, help='Filename of training corpus')
    parser.add_argument('--s', action='store_true', help='Provides a 50 word sample of the text supplied')

    args = parser.parse_args()
    with open(args.filename, 'r') as file:
        content = file.read()
        tokens = tokenize_sample(content)

        ngrams = generate_ngrams(tokens,2)
        bigram_count = generate_bigram_count(tokens)
        generate_sentence_prob(bigram_count)
        print(compute_perplexity(tokens))
    if (args.s):
        print(content[:49])

def generate_ngrams(tokens:List[str],n:int) -> List[Tuple[str,...]]:
    ngram = [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    return ngram

def generate_unigram_count(tokens):
    unigrams = generate_ngrams(tokens,1)
    counts = Counter(unigrams)
    for item in counts:
        counts[item] = counts[item] / len(unigrams)
    return counts

def generate_bigram_count(tokens):
    bigrams = generate_ngrams(tokens,2)
    counts = Counter(tokens)
    bigram_count = Counter(bigrams)
  
    for item in bigram_count:
        bigram_count[item] = bigram_count[item] / counts[item[0]]
   
    return bigram_count

def return_random_top_probability(ngrams):
    top_five = random.sample(list(ngrams.items()), 5)
    random_number = random.randint(0,4)
    return top_five[random_number]

def generate_sentence_prob(ngrams):
    sentence_limit = random.randint(5, 10)
    word = 0
    sentence = []
    
    while (word < sentence_limit):
        top_bigram = return_random_top_probability(ngrams)
        new_word = list(list(top_bigram)[0])[0]
        word += 1
        sentence.append(new_word)

    return ' '.join(sentence)

def compute_perplexity(tokens):

    test_set = random.sample(list(generate_bigram_count(tokens).values()),5)
    return sum(test_set) 
    
      
if __name__ == "__main__":
    main()


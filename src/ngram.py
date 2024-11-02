import argparse 
import re
from typing import List, Tuple
from collections import Counter
import random

def tokenize_sample(content: str) -> List[str]:
    text = re.sub(r'[^\w\s</>]','',content.lower().strip()) 
    return text.split()

def main():
    parser = argparse.ArgumentParser(description='This is a n-grams model command line')
    parser.add_argument('filename', type=str, help='Filename of training corpus')
    parser.add_argument('--s', action='store_true', help='Provides a 50 word sample of the text supplied')

    args = parser.parse_args()
    try: 
        with open(args.filename, 'r') as file:
            content = file.read()
            tokens = tokenize_sample(content)
            bigram_count = generate_bigram_count(tokens)
            print(generate_sentence_prob(bigram_count))
            print(compute_perplexity(tokens,5))
        
    except FileNotFoundError:
        print(f"Error: File'{args.filename} not found")
        return
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
    top_five = ngrams.most_common(5) 
    return random.choice(top_five)

def generate_sentence_prob(ngrams):
    sentence_limit = random.randint(5, 10)
    word_count = 0
    sentence = []
    current_word = random.choice(list(ngrams.keys()))[0]
  
    while (word_count < sentence_limit):
        possible_bigrams = {k:v for k,v in ngrams.items() if k[0] == current_word}

        if not possible_bigrams:
            break

        next_bigram = return_random_top_probability(Counter(possible_bigrams))
        current_word = next_bigram[0][1] if next_bigram else None
        sentence.append(current_word)
        word_count += 1
    print(sentence)
    return ' '.join(sentence)

def compute_perplexity(tokens,test_set_no):
    bigrams_probabilities = generate_bigram_count(tokens).values()
    if test_set_no > len(bigrams_probabilities):
        print("Warning: Test set size is larger than available bigram probabilities")
    test_set = random.sample(list(bigrams_probabilities),test_set_no)
    return (1/sum(test_set))**(1 / test_set_no)
    
if __name__ == "__main__":
    main()


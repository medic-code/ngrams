import argparse 
from typing import List, Tuple
from collections import Counter
import random
import math

import nltk
from nltk.tokenize import sent_tokenize, RegexpTokenizer


nltk.download('punkt_tab')


def tokenize_sample(content: str) -> List[str]:
    sentences = sent_tokenize(content)
    tagged_sentences = [f"<s> {sentence} </s>" for sentence in sentences]
    tagged_text = " ".join(tagged_sentences)
    tokenizer = RegexpTokenizer(r'<\/?s>|[\w\'\-]+|[.,!?;]')
    all_words = tokenizer.tokenize(tagged_text) 
    return all_words
    
def split_data(tokens):
    index_split = int(0.8*len(tokens))
    training_data = tokens[:index_split]
    test_data = tokens[index_split:]
    return training_data,test_data


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
    unigram_counts = Counter(tokens)
    bigram_count = Counter(bigrams)
    bigram_probs = {}
    for bigram in bigram_count:
        bigram_probs[bigram] = bigram_count[bigram] / unigram_counts[bigram[0]]
   
    return bigram_probs

def return_random_top_probability(ngrams):
    top_five = ngrams.most_common(5) 
    return random.choice(top_five)

def generate_sentence_prob(ngrams):
    sentence_limit = random.randint(5,15)
    word_count = 0
    sentence = []
    current_word = random.choice(list(ngrams.keys()))[0]
  
    while (word_count < sentence_limit and current_word != '</s>'):

        if current_word != '<s>':
            sentence.append(current_word)
            word_count += 1

        possible_bigrams = {k:v for k,v in ngrams.items() if k[0] == current_word}

        if not possible_bigrams:
            break

        next_bigram = return_random_top_probability(Counter(possible_bigrams))
        current_word = next_bigram[0][1] if next_bigram else None

        if current_word is None:
            break 
            
    print(sentence)
    return ' '.join(sentence)

def compute_perplexity(tokens,test_set_size = 5, smoothing = 1e-6):
    bigram_probs = [max(prob, smoothing) for prob in generate_bigram_count(tokens).values()]
    if test_set_size > len(bigram_probs):
        print("Warning: Test set size is larger than available bigram probabilities")
        test_set_size = len(bigram_probs)
    test_set = random.sample(bigram_probs,test_set_size)
    log_sum = sum(math.log(prob) for prob in test_set if prob > 0)
    return math.exp(-log_sum / test_set_size)


def main():
    parser = argparse.ArgumentParser(
        description='This is a n-grams model command line'
    )
    parser.add_argument('filename', type=str, help='Path to the text file to be processed')
    parser.add_argument('--s', action='store_true', help='Displays the first 50 word sample of the text supplied')

    args = parser.parse_args()
    try: 
        with open(args.filename, 'r') as file:
            content = file.read()
            tokens = tokenize_sample(content)
       
            train_data, test_data = split_data(tokens)
            bigram_count = generate_bigram_count(train_data)
            print(generate_sentence_prob(bigram_count))
            print(compute_perplexity(test_data,5))
        
    except FileNotFoundError:
        print(f"Error: File'{args.filename} not found, Please check file path")
        return
    if (args.s):
        print(content[:49])
    
if __name__ == "__main__":
    main()


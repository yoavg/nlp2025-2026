# Intro to NLP 2025-2026, Assignment 1.

This assignment has two parts. You can start working on the Part A right away, but may want to wait with Part B until after the class on parts of speech, morphology and tokenization. However, while the class is useful, it is not essential, and you will likely understand what you have to do also before the class. You can start taking that route.

# Part A: Experimenting with static word vectors (40 points)

## Word vectors

Use the `word2vec-google-news-300` pre-trained vectors, from the `gensim` python package.

https://radimrehurek.com/gensim/models/word2vec.html

You can learn about the different available models here: https://github.com/RaRe-Technologies/gensim-data

After installing the gensim package (using `pip install gensim` from the commandline), you can load the model as follows:

```python
import gensim.downloader as dl
model = dl.load("word2vec-google-news-300") 
# this will take a while on first load as it downloads a 1.6G file.
# later calls will be cached.

# You can now use various methods of the “model“ object.

# you can access the vocabulary like so:
vocab = model.index_to_key
```

## Code
Your python scripts that may use the `numpy`, `sklearn` (`scikit-learn`) and `gensim` packages.

## A.1 Polysemous Words (10 points)

_Polysemous words_ are words that have several meanings (for example, the word "bank" or the word "bat").

Find three polysemous words (words with at least two different meanings) such that the top-10 neighbors of each word _reflect both word meanings_, and three polysemous words such that the top-10 neighbors of each word _reflect only a single meaning_.

- Which three polysemous words belong in the first group, and what are their neighbors?
- Which three polysemous words belong in the second group, what are the possible senses for each word, and which of the senses was reflected in the top-10 neighbors?
- Can you explain why the second group words neighbors reflect only one sense?

## A.2 Synonyms and Antonyms (10 points)

_Synonyms_ (מילים נרדפות) are words that share the same meaning.

_Antonyms_ are words that have an opposite meaning (like "cold" and "hot"). 

Find a triplet of words (w1, w2, w3) such that all of the following conditions hold:

- $w_1$ and $w_2$ are synonyms or almost synonyms.
- $w_1$ and $w_3$ are antonyms.
- $\text{sim}(w_1,w_2) \lt \text{sim}(w_1, w_3)$

$\text{sim}$ should be the _cosine similarity_ measure.

Write your triplet.

Can you explain this behavior in which the antonyms are more similar than the synonyms?

## A.3 The Effect of Different Corpora (10 points)

In this section, we would like to compare models based on two sources.

The first model is based on _wikipedia and news text_, and the second based on _twitter data_. 

For the wikipedia and news model, use the gensim model `glove-wiki-gigaword-200`.

For the twitter data, use the gensim model `glove-twitter-200`.

("glove" is a different algorithm than word2vec, but its essence is similar.  You can read more about it [here](https://nlp.stanford.edu/pubs/glove.pdf))

- Find 5 words whose top 10 neighbors based on the news corpus are very similar to their top 10 neighbors based on the twitter corpus.
- Find 5 words whose top 10 neighbors based on the news corpus are substantially different from the top 10 neighbors based on the twitter corpus.

Which words did you find?

For the second case, describe in words the difference in neighbors you observe.

What was your strategy (either manual or _automatic_) for finding these 10 words?

## A.4 Plotting words in 2D (10 points)

### Dimensionality Reduction

Dimensionality reduction is a technique by which you take $n$-dimensional data and transform it into $m$-dimensional data ($m \lt n$), while attempting to maintain properties (such as distances) of the original data. Of course, dimensionality reduction is always a lossy process (because there is more information in $n$-dimension than in $m \lt n$ dimensions). Yet, it is still useful.

One way of dimensionality reduction is via the PCA algorithm. This algorithm is implemented in the `scikit-learn` (`sklearn`) python package. You can use it like so:


```python
from sklearn import decomposition

pca = decomposition.PCA(n_components=2)
pca.fit(X)   	# use a set of vectors to learn the PCA transformation
Z = pca.transform(Z)  # transform a set of vectors to reduce their dim
# (it is possible that Z=X)
```

Here, we reduce dimensionality to two dimensions, which is useful for plotting. But you can also reduce to more dimensions.


Take the first 5000 words in the vocabulary (`model.index_to_key[1:5000]`).

From these, keep only words that end either with `ed` or with `ing` (you should be left with 708 words). From the resulting list of 708 words, create a matrix with 708 rows, where each row is a 300-dim vector for one word, and reduce the dimensionality of the matrix to 2-d (the result is a matrix with 708 rows and 2 columns). Plot the resulting 2-d vectors (you can use the scatter plot in the `matplotlib` package) where each vector/word is a dot in a scatter plot, according to its coordinates. Color points that correspond to words that end with `ed` in _blue_, and points that correspond to words that end with `ing` in _green_.  Submit the resulting plot. Also submit a discussion of it (are the colors separated? why or why not? is the information included in the model? etc). 


# Part B: words and tokens vocabularies (60 points)

You are given texts in two languages. The file `english.txt.gz` contains texts in English, while the file `hebrew.txt.gz` contains text in Hebrew (both files are in UTF-8 encoding, and compressed using gzip).

- [english.txt.gz](https://github.com/yoavg/nlp2024-2025/releases/download/ass1a-data/english.txt.gz)
- [hebrew.txt.gz](https://github.com/yoavg/nlp2024-2025/releases/download/ass1a-data/hebrew.txt.gz)

## Token and type counts

### Definitions

In this part, we define a *token* to be a sequence of non-whitespace and non-punctuation characters. Many tokens roughly correspond to "words", but as we saw in class the definition of a word is much more nuanced.

We will also talk about *tokens in a text* which are all the individual occurrences in the text, and *token-types in a text* which are the set of distinct tokens that appear in the text (also called "*the vocabulary*").

For example, in the text:
```
they ate apples, and then, they ate some ice-cream!!
```

The tokens are (each in its own line): 
```
they
ate
apples
and
then
they
ate
some
ice-cream
```

Note that we stripped the punctuation symbols `,` and `!!` (but not the word-internal `-`). Some definitions of tokens do include also such punctuation symbols, and treat them as standalone tokens. In this assignment, for simplicity, we discard them.

The types are:
```
they
ate
apples
and
then
some
ice-cream
```

The types `ate` and `they` each appear twice in the text, while the other types appear just once.

### Unigrams (15 points)

You should produce answers to the following questions. You probably want to do it by writing one or several short programs. Python would be a good choice, but we leave the decision up to you.

For each of the files (Hebrew, English):
1. How many tokens are in the file?
2. How many distinct types are in the file?
3. What is the tokens/types (tokens divided by types) ratio for each language? Can you explain this difference?
4. Now, let's look at the first half of each file (if the number of tokens in the file is N, we look at the first N/2 tokens). How many distinct types are in this first half? How many distinct types were added when going from the first half to the entire file? Are there types that don't appear in the first half, but appear more than two times in the second half? more than 5 times? more than 10 times? provide examples of each, or say that none exist.
5. Back to the full files: what are the top 50 most frequent token-types in each file (sorted from most frequent to least frequent)? Are the lists similar or different? Briefly discuss the reasons for this.
6. Which is the 100th most frequent word in each language? What is the 1,000th most frequent? What is the 10,000 most frequent?
7. In each language, how many types appear: exactly once? exactly twice? exactly three times? exactly 5 times? how many types appear 10 times or more? 100 times or more? 1,000 times or more? 10,000 times or more? Arrange these numbers in a table.

These answers should appear in a PDF file called `unigrams.pdf` . 

**Hint**: for these items, it might be useful to write code that goes over the file once, extracts and counts tokens, and then writes out a file with the counts of each type. This file can then be read by future program for further computations. The `defaultdict` and `Counter` objects from the built-in `collections` module are useful for this kind of counting.

### N-grams (15 points)

We define a sequence of $n$ tokens as an "n-gram". For example, `I am not the` is a 4-gram, and `the big brown box` is also a 4-gram. 

1. In each language, what are the top-ten 5-grams in each file and their frequencies? What are the top-ten 10-grams in each file and their frequencies? what is the longest n-gram with a frequency above 1 in each file and its frequency? Briefly discuss and explain the results that you see. 
   
These answers should appear in a PDF file called `ngrams.pdf`.

**Hint**: to save memory and be more efficient, consider that in order for a n-gram to appear more than once, then every k-gram $k<n$ within it should also appear more than once. In particular, every token in the n-gram should appear more than once.

## Subword-tokenization with BPE

We now switch to a different definition of *tokens*, which is made popular in recent years, and in particular in the context of deep-learning and large language models.

As you saw in the previous part, the number of distinct types ("the vocabulary size") can be quite large. It also keeps growing as we grow the text size. It is convenience to be able to work with a fixed-size vocabulary, which is also not too big, but that will still be able to cover all the letter sequences we'll observe in every text. For this, we turn to so-called "sub-word units". Instead of each token be a unit separated by white-space and punctuation (as the definition above), we instead have a fixed vocabulary of token-types, and each "classic token" (according to the definition above) will be split into smaller tokens from the pre-defined token-type vocabulary.

For example, a sequence like `democratic` may be represented as `demo crat ic§` where `demo`, `cra` and `ic§` are all vocabulary items, and `§` is a special `end-of-word` character (in principle we could just use the `[SPACE]` character instead of `§`, but it will be less readable to humans looking at the tokens.

A tokenization algorithm according to this definition will take a text and a vocabulary, and split the text to units according to the vocabulary.

How do we decide on the vocabulary? If we want to be able to construct every possible text in the language, the vocabulary should, at a minimum, include all the possible characters (which we can get by looking at a large-enough file, like the ones we provide in this assignment). But we also want to allow for larger units than single characters. For this, we use a *training algorithm* that will learn a good set of units from data.

In this assignment, we will be working with the popular `byte-pair encoding` (or `BPE`) sub-word token algorithm, which is often used in practice in modern-day NLP systems. You will implement the BPE algorithm, apply it to data, and inspect the resulting token vocabulary.

### BPE Training

The BPE algorithm is described in the following paper:
[https://arxiv.org/pdf/1508.07909](https://arxiv.org/pdf/1508.07909)

BPE training works as follows:

**As input**, we get a text to train on, as well as a target vocabulary size N (which must be larger than the number of distinct characters in the data).
**The output** will be a list of N strings, each of length 1 or more, representing the vocabulary.

The algorithm's behavior is simple. Conceptually:

Initialize the vocabulary with the all the distinct characters in the input file.
Then, while the vocabulary size is smaller than N:
- Consider all the consecutive pairs of vocabulary items in the file (in the first round, it will be all the pairs of characters).
- Take the most frequent such pair of consecutive items, and merge them. (For example, if the most frequent pair was `t h`, merge them into a single unit `th`).
- Add the merged term to the vocabulary, growing the vocabulary by 1.
- Replace all occurrences of the pair in the text with the new item just created. (In the following round, it may further merge with other units).
When we exit the loop, the vocabulary has N items, which is our output.

During the algorithm, we treat consecutive sequences of whitespace as a single whitespace item. We also treat whitespace as a special symbol, and don't allow merging a whitespace with items after it, only with items before it (this ensures that vocabulary items never cross white-space-separated word boundaries). In our output vocabulary, a whitespace will be either standalone or appear at the end of an item (never in the middle or in the beginning). For convenience, we replace all whitespace with the character `§` which we assume does not appear in the file. (What should we do if it does appear in the file? this is a technical detail which is left as a thought exercise.)

**Efficiency tips**: counting all pairs in a long text can be time consuming. Since we never cross "classic token boundaries" in this algorithm (we never merge whitespace with an item following it), we can do something much more efficient: we first tokenize the text on whitespace, and count each resulting classic token-type (much like you did in the first part of this assignment). We can then do the pair counts over the token-types, where we count each pair according to the frequency of the type it is in. So for example if the sequence "room" appeared 5681 times in the text, we may increase each of the counter for `r o`, `o o` , `o m` and `m §` by 5681 when we go over the token-types list. ``

### BPE Inference/tokenization:

How is the trained vocabulary used to tokenize a new input text? The tokenization algorithm is a very simple greedy procedure: at each point, take the longest prefix of the text that is available in the vocabulary, and split it off.

For example, for the vocabulary: “abc ab de bcde a b c d e f g” and the input text “abcdefg abfbcdef” the output will be "abc" "de" "f" "g§" "ab" "f" "bcde" "f§". 

### Your assignment (30 points):

Implement the BPE training algorithm in a file called `bpe.py` which has a function called `train_bpe(filename, N)` that takes in a filename to train on and a number N, and returns a list of N strings representing the learned vocabulary. 

**Train a BPE vocabulary for each of the files, with N=30,000**

Answer the following questions:
1. How many "complete tokens" (according to the previous definition of token) end up in the BPE vocabulary for each of the languages?
2. What are some learned vocabulary items in each language that are larger than a single character, smaller than a complete token, and "make sense" linguistically? briefly discuss why you think they make sense.
3. What are some learned vocabulary items in each language that are larger than a single character, smaller than a complete token, and do not "make sense" linguistically? briefly discuss why you think they do not make sense.
4. Are there learned vocabulary items in either of the languages that "make sense" linguistically when used to split some words, but do not "make sense" linguistically when used to split some other words? show such examples if they exist and discuss briefly.

Submit your BPE implementation (`bpe.py`) as well as the answers to the questions above in a file called `bpe.pdf`. 

The `bpe.py` file must include a function `train_bpe` with the signature defined above, and we should be able to write `from bpe import train_bpe` in our own script and run the file. In other words, the `bpe.py` should act as a module: all runnable code which is not inside a function should be guarded under:
```python
if __name__ == "__main__":
```

# Summary of files to be submitted:

Include all the files mentioned above (and summarized below) in a single `zip` file.
Include also a plain-text file called `ids.txt` where each line corresponds to one of the students, and has the following format:
```
ID_NUMBER submit_user_name name_in_english
```

For example, a pair of two students my have an `ids.txt` file that looks like this:

```
040083249 ddavid1 David Davidi
543943239 yael92 Yael Yaeli
```

In addition to `ids.txt`, the files to be submitted are:

**Part A**:

A PDF file called `part-A.pdf` containing your names and IDs, and:

- Your answers and discussion of the polysemous words.
- Your answers and discussion of the synonyms and antonyms.
- Your answers and discussion of the effect of different corpora.
- Your plot + discussion for the plotting-in-2d part.

**Part B**:
```
unigrams.pdf
ngrams.pdf
bpe.py
bpe.pdf
```


**Good Luck and have fun!**

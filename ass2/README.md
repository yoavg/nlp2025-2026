# Intro to NLP 2024-2025, Assignment 2.

This assignment has two parts. You can start working on the Part A right away, while part B contains concepts you will only see in the contextualized word vectors class (on Dec. 10). However, parts of part B (namely B.1.1 and B.1.2) do not require these concepts and you can start with them.
Additionally, the class will be helpful, but is not _essential_, and you can also read the other parts and attempt to start with them right away.

# Part A: Experimenting with static word vectors (20 points)

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

## A.1 Polysemous Words (5 points)

_Polysemous words_ are words that have several meanings (for example, the word "bank" or the word "bat").

Find three polysemous words (words with at least two different meanings) such that the top-10 neighbors of each word _reflect both word meanings_, and three polysemous words such that the top-10 neighbors of each word _reflect only a single meaning_.

- Which three polysemous words belong in the first group, and what are their neighbors?
- Which three polysemous words belong in the second group, what are the possible senses for each word, and which of the senses was reflected in the top-10 neighbors?
- Can you explain why the second group words neighbors reflect only one sense?

## A.2 Synonyms and Antonyms (5 points)

_Synonyms_ (מילים נרדפות) are words that share the same meaning.

_Antonyms_ are words that have an opposite meaning (like "cold" and "hot"). 

Find a triplet of words (w1, w2, w3) such that all of the following conditions hold:

- $w_1$ and $w_2$ are synonyms or almost synonyms.
- $w_1$ and $w_3$ are antonyms.
- $\text{sim}(w_1,w_2) \lt \text{sim}(w_1, w_3)$

$\text{sim}$ should be the _cosine similarity_ measure.

Write your triplet.

Can you explain this behavior in which the antonyms are more similar than the synonyms?

## A.3 The Effect of Different Corpora (5 points)

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

## A.4 Plotting words in 2D (5 points)

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


# Part B: Contextualized Vectors, Parts of Speech, and Named Entities (80 points)

This part of the assignment will have you working with word vectors (both static and contextualized) in the context of sequence tagging tasks.
You will also explore the concepts of _Part-of-speech (POS) tagging_ and _named-entity-recognition (NER)_.

## B.0 Warmup on Contextualized Vectors

The `huggingface transformers` python library provides many sentence encoders.

We will be using the `roberta-base` model.

https://huggingface.co/roberta-base

It was trained as a "masked language model".

To learn to use the model, after installing the library (`pip install transformers`) do the following tasks:

1) Encode the sentence "I am so MASK" and:
1.1) Extract the vectors for "am" and for "MASK".
1.2) extract the top-5 word predictions for "am" and for "MASK" and their probabilities.
2) Find two sentences that share the same word, such that the cosine similarity between the word vectors in the two sentences is very high.
3) Find two sentences that share the same word, such that the cosine similarity between the word vectors in the two sentences is very low.
4) Find a sentence with $n$ words, that is tokenized into $m \gt n$ tokens by the tokenizer.

Note: when we say "MASK" we mean a special sequence which is known by the model is being the MASK token. See the usage instruction of the model to figure out how to feed this token to the model.

## B.1 Parts-of-speech Tagging

Your first task will be part-of-speech tagging, that is, given a text, assign each word in the text its correct part-of-speech.

### Intro

The "standard" way to perform part-of-speech tagging with word vectors, is to get a vector representation of each word in a window surrounding the target work (or a contextualized vector of each word in its context) and then use an annotated corpus to _train a classifier_ to predict the correct part-of-speech tag from the vector (or vectors). The classifier can either be on top of the vectors (where the encoder that produces the vectors is fixed), or it may also include the encoder itself (so both the classifier and the encoder that produces the vectors are changed during the training process). Using such an approach, and based on the `roberta-base` encoder, we can easily get part-of-speech tagging accuracies of 97% or above. The `transformers` library, together with the `pytorch` library, makes such training quite easy, once you get the hang of it. 

In this assignment, however, **we will not take this approach** (though you are certainly welcome and encouraged to experiment with it on your own, if you wish). Instead, we will experiment with predicting parts of speech of words in context based on the out-of-the-box vectors, _without training any classifiers_ (that is, without changing any parameters, without running SGD, etc).

### Training, validation (dev) and test data

The training, validation (dev) and test data are in the `pos.tgz` file.

- [pos.tgz](https://github.com/yoavg/nlp2024-2025/releases/download/ass2-data/pos.tgz)


The format is one sentence per line, the text is already pre-tokenized (in the sense of text tokenization that splits punctuation from words etc, not in the BPE/word-pieces sense that is needed to feed the sentence into a contextualized vectors encoder).

### Task

In each of the following sections, your task will be simple: use the annotated data in the training set, to best predict the parts-of-speech of the words in the test set sentences.

You can do whatever you want to achieve a good accuracy, as long as you don’t:

1) look at the labels of the test data—this is never allowed.
2) tune any parameters or train any model—this is not allowed in this assignment.

What can you do, then? You are free to choose any approach you wish. For example, you could encode some or all the data in the training set, remember the labels, and look for similarities to encoded test vectors. Or you could predict the top-k words for some or all the words in the training set, and use them somehow. Or you could use clustering of vectors. Or you could use dimensionality reduction as we did in part A. Or you can mix-and-match these approaches. Or you could do something else.

### Notes

**Combining vectors**: as we discuss in class, natural ways to combine vectors are by concatenation or by addition.

**Runtime**: we do not talk about efficiency or running time in this assignment, and things are possible to run also without a GPU. However, if your predictor cannot finish tagging the data before you need to submit the assignment, then there might be a problem.

**What to submit**: In addition to the written report, for each of the following subtasks, send a prediction file named `POS_preds_X.txt` where `X` is replaced by the subtask number (B-1-1, B-1-2 or B-1-3). Each line in the predictions should correspond to a test sentence and be in the same format of the training data.

### B.1.1 No Word Vectors (20 points)

In this part of the assignment, you are not allowed to use any word vectors at all. However, you are allowed to count word, count (word,tag) pairs, to look into the characters the words are made of and count them as well, etc. 

One simple approach would be to count for each word type in the training corpus what is its most frequent part-of-speech tag, and then assign this tag for every occurrence of this word in the test corpus, regardless of its context (you also need to figure out which tags to assign to words that did not appear in the training corpus). How well does this approach get you? Can you do better? What is the accuracy of the best parts-of-speech predictor you can achieve with this approach? (reaching 85% accuracy should be trivial, and you can do more than that).

Describe your approach in the report, and submit your predictions over the test data in a file called `POS_preds_B-1-1.txt`.

### B.1.2 Static Word Vectors (20 points)

As before, but now you are allowed to use static vectors (word2vec or glove vectors, as used in part A). You can use either single vectors, or vectors in a window surrounding the word. You can also use some of the counts from part B.1.1, if you find them helpful. What is the best accuracy you can get?

Describe your approach in the report, and submit your predictions over the test data in a file called `POS_preds_B-1-2.txt`.

### B.1.3 Contextualized word vectors (20 points)

As before, but now you are allowed to use the output of roberta-base (either the word vectors for each position, or the word predictions for each position, or both, or any other output you can get out of the pre-trained roberta-base model). You can also use some of the counts from part B.1.1, or the static vectors from part B.1.2, if you find them helpful. What is the best accuracy you can get?

Describe your approach in the report, and submit your predictions over the test data in a file called `POS_preds_B-1-3.txt`.

## B.2 Named Entity Recognition (20 points)

We now switch from predicting parts-of-speech (which are per-word) to named entities (which are spans).

As you saw in class, there is a reduction (B-I-O tagging) by which you can perform span prediction by predicting tags for individual words. This is also the format the annotated data comes in. However, you are not required to use this reduction in this assignment, you can also predict spans directly.

As before, the standard (and effective) way to perform named entity recognition, is to train (fine-tune) a classifier to predict the named-entity tags. You are, however, again, not allowed to do so in this assignment. Instead, you will need to work under the same constraints as in part B.1.

You are allowed to use counts, as well as static word vectors, and the output of roberta-base (as in B.1.3). What is the best named-entity-predictor you can produce?

Describe your approach in the report, and submit your predictions over the test data. The predictions should be sent in a text file `NER_preds.txt`. Here again each line should correspond to a test sentence and be in the same format of the input data.

### Training, validation (dev) and test data

The training, validation (dev) and test data are in the `ner.tgz` file.

- [ner.tgz](https://github.com/yoavg/nlp2024-2025/releases/download/ass2-data/ner.tgz)

The format is like in the parts-of-speech part, using the BIO encoding for spans. Note however that while the input and output should be in the BIO format, your prediction algorithm could be different from treating the problem as a per-token tagging task, and can attempt to predict spans directly. You can be creative.

### Evaluation metric

It might be tempting to measure our success on the NER task by measuring the per-word accuraccy of the B-I-O tags assignments (that is, treat it as a per-word tagging task, and measure accuracy on that task). This is, however, a bad choice, as the measure can be very misleading. To convince yourself of that, construct a sentence and a tagging pair such that the per-word tagging accuracy is very high, while no gold span is correctly indentified.

Instead, your evaluation metrics in this part should be _precision_, _recall_ and _F1_ over predicted spans.

- _precision_ is computed as the number of correctly predicted spans, divided by the number of all predicted spans.
- _recall_ is comuted as the number of correctly predicted spans, divided by the number of all gold spans.
- _F1_ is the harmonic mean of precision and recall: 2*(precision * recall) / (precision + recall).

You should understand these measures and how they are computed.

You can perform span-level evaluation using the [ner_eval.py](ner_eval.py) script,
which should be run as:
```sh
python ner_eval.py gold_file predicted_file
```

Read the evaluation script and see that you understand it.


# What to submit

Submit everything in a single `.zip` file.

Code: 

## For Part A:

A PDF file called `part-A.pdf` containing your names and IDs, and:

- Your answers and discussion of the polysemous words.
- Your answers and discussion of the synonyms and antonyms.
- Your answers and discussion of the effect of different corpora.
- Your plot + discussion for the plotting-in-2d part.

## For Part B:

Your predictions on the test sets (we will measure your accuracies on these using hidden test labels which we have).

- `POS_preds_B-1-1.txt`
- `POS_preds_B-1-2.txt`
- `POS_preds_B-1-3.txt`
- `NER_preds.txt`

A PDF file called `part-B.pdf` containing your names and IDs, and a description of your train and dev scores and the approaches and the working process you took for each of the pars B.1.1, B.1.2, B.1.3, B.2.

# A note on grading:

Part of your grade for part B will be based on the test-set performance of your models: the best-performing model will receive full credit (100%) for its section, while other models will be graded proportionally. The creativity of you solutions and the quality of your reports will also be taken into account when grading.


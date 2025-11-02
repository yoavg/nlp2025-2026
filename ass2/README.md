# Intro to NLP 2025-2026, Assignment 2.

This assignment has two parts. You can start working on the Part A right away, while part B contains concepts you will only see in the contextualized word vectors class (on Dec. 10). However, parts of part B (namely B.1.1 and B.1.2) do not require these concepts and you can start with them.
Additionally, the class will be helpful, but is not _essential_, and you can also read the other parts and attempt to start with them right away.

# Part A: Generating sentences with a Context-Free Grammar (50 points)

   _Credit due_: This part of the assignment is based on [an assignment](https://www.cs.jhu.edu/~jason/465/hw-grammar/hw-grammar.pdf) by Jason Eisner at JHU.

## Goal
This part will help you understand how Context-Free Grammars (CFGs) work, and how they can be used --- sometimes comfortably, sometimes not so much --- to describe sentences in natural language. It will also make you think about some linguistic phenomena that are interesting in their own right.

## Deliverables 

In this part, you will submit a report file (`cfg.pdf`) as well as some other files (corresponding to code, grammars, and generated sentences) to be discussed below. Whenever the assignment says _"discuss..."_ or _"describe..."_ it means that you should write a discussion or a description in the `cfg.pdf` file. Make sure this file is clearly organized, and indicates clearly which question you are answering.

## Part A.0: Generating Sentences from a CFG (1 point)

We provide you with the following components:

1. A basic grammar file [grammar](grammar).  Make sure to review its format below.
2. A python program [generate.py](generate.py) that generates sentences from a grammar.

The program `generate.py` takes a grammar file as an argument, and generates a sentence from it. Your task is to generate sentences from the grammar using the `generate.py` program:

```bash
python generate.py grammar
```

**The Grammar File:**
The format of the grammar file is as follows: 
```grammar
# A fragment of the grammar to illustrate the format.
1 ROOT S .
1 S NP VP
1 NP Det Noun # There are multiple rules for NP.
1 NP NP PP
1 Noun president
1 Noun chief of staff   
```
   
These lines correspond to the following rules (in this order):

- ROOT $\rightarrow$ S 
- S $\rightarrow$ NP VP
- NP $\rightarrow$ Det Noun
- NP $\rightarrow$ NP PP
- Noun $\rightarrow$ president
- Noun $\rightarrow$ chief of staff

Notice that a line consists of three parts:
1. a number (ignore this for now) 
2. a nonterminal symbol, called the "left-hand side" (LHS) of the rule
3. a sequence of zero or more terminal and nonterminal symbols, which is called the "right-hand side" (RHS) of the rule

A hash sign (`#`) indicates a comment, and everything after it is ignored.

We take `ROOT` to be the root of the grammar. 

That is, every generation must start with a ROOT.


**The Program File:**
Look at the `generate.py` program and **understand** it.

**Extend** the program so that it accepts an optional argument (indicated by `-n`) that specifies the number of sentences to generate. 
For example, the invocation: 
```sh
python generate.py grammar -n 5
```
will generate 5 sentences, the invocation:
```sh
python generate.py grammar -n 2
```
will generate two sentences, and 
```sh
python generate.py grammar
```
will generate one sentence, as it does now.

Each generated sentence should be printed on its own line, and there should be no blank lines between them.

**Note** the list `sys.argv` includes the command line arguments of a python program. You can either take care of the command line processing logic yourself, or use a module such as [docopt](https://github.com/docopt/docopt)or the built-in `argparse`.

## Part A.1: Weights (5 points)

Consider the output sentences you generated in part B.0 and answer the following questions (in `cfg.pdf`):

1. Why does the program generate so many long sentences? Specifically, what grammar rule is responsible for that and why? What is special about this rule? discuss.
2. The grammar allows multiple adjectives, as in: _"the fine perplexed pickle"_. Why do the generated sentences show this so rarely? discuss.
3. The grammar format allows specifying different weights for different rules.

For example, in the grammar:
```grammar
3 NP A B
1 NP C D E
1 NP F
2 X NP NP
```
The NP rules have a relative ratio of 3:1:1, so, when generating an NP, the generator will pick the first rules 3/5 of the times, the second one 1/5 of the times, and the third one 1/5 of the times.

Which numbers must you modify to fix the problems in (1) and (2), making the sentences shorter and the adjectives more frequent?

Verify your answer by generating from the grammar. Discuss your solution (which rules did you modify, and why).

4. What other numeric adjustments can you make to the grammar in order to favor a set of more natural sentences? Experiment and discuss.

**What to Submit:**
- Submit your grammar file (including the solution to (3) above), with comments that motivate your changes, in a file named `grammar1`.
- Hand in 10 sentences generated via `grammar1`, in a file called `grammar1.gen` .

```sh
python generate.py grammar1 -n 10 > grammar1.gen
```

## Part A.2: Extending the Grammar (15 points)

Modify the grammar so that it can also generate the types of phenomena illustrated in the following sentences:
1. Sally ate a sandwich .
2. Sally and the president wanted and ate a sandwich .
3. the president sighed .
4. the president thought that a sandwich sighed .
5. it perplexed the president that a sandwich ate Sally .
6. the very very very perplexed president ate a sandwich .
7. the president worked on every proposal on the desk .
8. Sally is lazy .
9. Sally is eating a sandwich .
10. the president thought that sally is a sandwich .

You want to end up with a single grammar that can generate _all_ of the sentences in part B.1 as well as _all_ sentences (1)--(10) here.  Furthermore, we expect your grammar to generate sentences which do not exist in this list but have grammatically similar structures.

While your new grammar may generate some very silly sentences, it should not generate any that are strictly ungrammatical. For example, in the following pair, your grammar must be able to generate the first sentence (11), but it must exclude the second one (12) marked with an asterix \*[^1]


[^1]: In linguistics, * is traditionally used to mark ungrammatical sentences.

12. the president thought that a sandwich sighed .
13. \* the president thought that a sandwich sighed a pickle.

More specifically, your grammar should respect the _subcategorization frame_ of verbs (number and types of required arguments, as defined in class). Think, for instance, about VP taking an S and not NP. However it doesn't have to respect _selectional restrictions_ (the semantic restrictions on the kind of arguments). That is, no need to distinguish between nouns that can eat, want, or think and ones that cannot. 

Overall, while the sentences should be okay structurally, they don't need to really make sense.

**Notes:**
- Be sure you can handle the particular examples we suggested here, which means, among other things, that your grammar must include the words in those examples.
- Make sure that your grammar can generalize from the suggested example sentences. For example, sentence (2) invites you to think about the ways in which conjunctions ("and", "or", etc) can be used in English. Sentence (7) invites you to think about how prepositional phrases ("on the desk", "over the rainbow", "of the United States") look like, and how they are used in English sentences.
- Furthermore, note that handling sentences (2) and (8)/(9) can interact in a bad way, to create ungrammatical sentences. You do not need to solve this issue in this part of the assignment, but you do need to discuss it and explain what the problem is, using an example and a short explanation (in `cfg.pdf`).
- Finally, an important technical note. The grammar file allows comments and whitespace because the grammar is really a kind of specialized programming language for describing sentences. Throughout this assignment, **when writing grammars, you should strive for the same level of elegance, generality and documentation  as when writing code.**

**Implementation Hints:**
If you want to see the effect of various rules while developing your grammar, you can give them a very high weight so that they will trigger often.
Implementing Part B.3 can also help you debug your grammar.

**What to submit:**
Briefly discuss your modifications to the grammar (in `cfg.pdf`). Hand in the new grammar (commented) as a file named `grammar2` and about 20 random sentences that illustrate your modifications in a file named `grammar2.gen`.

**How your grammars will be tested:**
We want to see that your grammar can produce sentences with structures as we specified, and generalize to similar structures, but not produce bad (i.e., ungrammatical) sentences. We will run a parser that uses your grammar to try and parse a set of sentences you have not previously seen. Your parser should be able to parse the grammatical ones, and not be able to parse the ugrammatical ones. 
**Recall,** you can parse a sentence with a grammar if and only if this sentence can be generated by the grammar.

## Part A.3: Tree Structures (5 points)
Modify the `generate.py` program so that it gets an optional command line switch `-t`. When `-t` is present, the program should generate not only sentences, but also the tree structures that generates the sentences.

For example, when invoked as: 
```sh
python generate.py grammar -t
```
instead of just printing `the floor kissed the delicious chief of staff .` it should print the more elaborate version
```
(ROOT
     (S (NP (Det the)
        (Noun floor))
     (VP  (Verb kissed)
          (NP  (Det the)
               (Noun (Adj delicious)
                     (Noun chief
                           of
                           staff)))))
   .)
```

which includes extra information showing how the sentence was generated. For example, the above derivation used the rules Noun $\rightarrow$ floor and Noun $\rightarrow$  Adj Noun, among others.

Note: It's not too hard to print the pretty indented format above. But it's not necessary. It's sufficient if you will the entire expression on a single line:
```
(ROOT (S (NP (Det the) (Noun floor)) (VP (Verb kissed) (NP (Det the) 
(Noun (Adj delicious) (Noun chief of staff))))) .)
```

The bracketed expression can be visualized in tree form using web-based visualizers like [this](http://christos-c.com/treeviewer/) and [this](http://mshang.ca/syntree/).  This sort of output can be useful when debugging your grammar -- understanding which rules are responsible for what structures.

**Implementation Hint:** The changes to the original code are not big. You don't have to represent a tree in memory, so long as the string you print has the parentheses and non-terminals in the right places.

Your code should support both the `-n` from part B.0, and the `-t` switch, either alone or together.

**What To Submit:**
Generate 5 more random sentences, in tree format. Submit them as in a file called `b3.gen` as well as the code for the modified `generate.py` program.

## Part A.4: Additional Linguistic Structures (24 pts, 12 each)

Think about all of the  additional linguistic phenomena presented below, and extend your grammar from part B.2 to handle **TWO** of them -- any two your choice. Briefly discuss your solutions and provide sample output.

Be sure you can handle the particular examples suggested herein, which means among other things that your grammar must include the words in those examples. You should also generalize appropriately beyond these examples. 

As always, try to be elegant in your grammar design, but you will find that these phenomena are somewhat harder to handle elegantly with CFG notation.

### (a) "a" vs. "an". 
Add some vocabulary words that start with vowels, and fix your grammar so that it uses "a" or "an" as appropriate (e.g., "an apple" vs. "a president"). This is harder than you might think: how about "a very ambivalent apple"?

### (b) Yes-no questions. 
Examples:
- did Sally eat a sandwich ?
- will Sally eat a sandwich ?

Of course, don't limit yourself to these simple sentences. Also consider how to make yes-no questions out of the statements in part 2.

### (c) Relative clauses.
Examples:
- the pickle kissed the president that ate the sandwich .
- the pickle kissed the sandwich that the president ate .
- the pickle kissed the sandwich that the president thought that Sally ate .

Of course, your grammar should also be able to handle relative-clause versions of more complicated sentences, like those in part 2.

**Hint:** These sentences have something in common with (d).
### (d) WH-word questions. 

If you also did (b), handle questions like

- what did the president think ?
- what did the president think that Sally ate ?
- what did Sally eat the sandwich with ?
- who ate the sandwich ?
- where did Sally eat the sandwich ?

If you didn't also do (b), you are allowed to make your life easier by instead handling "I wonder" sentences with so-called "embedded questions":

- I wonder what the president thought .
- I wonder what the president thought that Sally ate .
- I wonder what Sally ate the sandwich with .
- I wonder who ate the sandwich .
- I wonder where Sally ate the sandwich .

Of course, your grammar should be able to generate wh-word questions or embedded questions that correspond to other sentences.

**Hint:** All these sentences have something in common with (c).

### (e) Singular vs. plural agreement.

For this, you will need to use a present-tense verb, since past tense verbs in English do not show agreement.

Examples:
- the citizens choose the president .
- the president chooses the chief of staff .
- the president and the chief of staff choose the sandwich .

You are not allowed to select both this question (e) and question (a), as the solutions are somewhat similar.

### (f) Tense and Aspect.

Expression tense information may involve more than a single verb. For example,
"the president has been eating a sandwich" . 
Here, you should try to find a reasonably elegant way of generating all the following 12 tense (present, past, future) $\times$ aspect (simple, perfect, progressive, perfect-progressive) combinations:

| tense $\rightarrow$<br>aspect $\downarrow$ | present         | past            | future                |
| ------------------------------------------ | --------------- | --------------- | --------------------- |
| **Simple**                                     | eats            | ate             | will eat              |
| **Perfect**                                    | has eaten       | had eaten       | will have eaten       |
| **Progressive**                                | is eating       | was eating      | will be eating        |
| **Perfect Progressive**                        | has been eating | had been eating | will have been eating |

### (g) Appositives.

Examples:
- the president perplexed Sally , the fine chief of staff .
- Sally , the chief of staff , 59 years old , who ate a sandwich , kissed the floor .

The tricky part of this one is to get the punctuation marks right. For the appositives themselves, you may rely on some canned rules such as "Appos $\rightarrow$ 59 years old". 
However, if you also did (c), try to extend your rules from that problem to automatically generate a range of appositives such as who ate a sandwich and which the president ate.

**What To Submit:**
Hand in your grammar (commented) as a file named `grammar4`.
The first line of `grammar4` must be a comment, including the letters of the two phenomena you chose to implement, separated by space. Example `# b f`:

Submit 50 random generated sentences from your grammar in `grammar4.gen`.

In addition, provide a description of your solution in `cfg.pdf`.

**Important Note:** Your final grammar should handle everything from part B.2, plus both of the phenomena you chose to add. This means you have to worry about how your rules might interact with one another. Good interactions will elegantly use the same rule to help describe two phenomena. Bad interactions will allow your program to generate ungrammatical sentences, which will hurt your grade.



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

In addition to the `ids.txt` file:

## For Part A:

The files

```
cfg.pdf
generate.py  # including -n and -t switches
grammar1
grammar1.gen
grammar2
grammar2.gen
b3.gen
grammar4
grammar4.gen
```

## For Part B:

Your predictions on the test sets (we will measure your accuracies on these using hidden test labels which we have).

- `POS_preds_B-1-1.txt`
- `POS_preds_B-1-2.txt`
- `POS_preds_B-1-3.txt`
- `NER_preds.txt`

A PDF file called `part-B.pdf` containing your names and IDs, and a description of your train and dev scores and the approaches and the working process you took for each of the pars B.1.1, B.1.2, B.1.3, B.2.

# A note on grading:

Part of your grade for part B will be based on the test-set performance of your models: the best-performing model will receive full credit (100%) for its section, while other models will be graded proportionally. The creativity of you solutions and the quality of your reports will also be taken into account when grading.


# Intro to NLP 2024-2025, Assignment 1.

This assignment has two parts. You can start working on the Part A right away, but may want to wait with Part B until after the class on syntax and grammar.
# Part A: words and tokens vocabularies (50 points)

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

### Unigrams (10 points)

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

### N-grams (10 points)

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

# Part B: Generating sentences with a Context-Free Grammar (50 points)

   _Credit due_: This part of the assignment is based on [an assignment](https://www.cs.jhu.edu/~jason/465/hw-grammar/hw-grammar.pdf) by Jason Eisner at JHU.
## Goal
This part will help you understand how Context-Free Grammars (CFGs) work, and how they can be used --- sometimes comfortably, sometimes not so much --- to describe sentences in natural language. It will also make you think about some linguistic phenomena that are interesting in their own right.

## Deliverables 

In this part, you will submit a report file (`cfg.pdf`) as well as some other files (corresponding to code, grammars, and generated sentences) to be discussed below. Whenever the assignment says _"discuss..."_ or _"describe..."_ it means that you should write a discussion or a description in the `cfg.pdf` file. Make sure this file is clearly organized, and indicates clearly which question you are answering.

## Part B.0: Generating Sentences from a CFG (1 point)

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

## Part B.1: Weights (5 points)

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

## Part B.2: Extending the Grammar (15 points)

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

## Part B.3: Tree Structures (5 points)
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

## Part B.4: Additional Linguistic Structures (24 pts, 12 each)

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
```
unigrams.pdf
ngrams.pdf
bpe.py
bpe.pdf
```

**Part B**:
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

**Good Luck and have fun!**

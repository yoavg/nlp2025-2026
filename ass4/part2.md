# Intro to NLP 2025-2026, Assignment 4 - Part 2

**Trying to help people get their rights!**

Back to [Part 1](README.md)

## Eval Set:

This is the evaluation set ("test-set") based on your submissions, which you should evaluate your system on (see "Evaluation") below.

- [eval-set.csv](eval-set.csv)

It is composed of a random sample of queries you submitted. Not all your submissions are represented: some lines were just not selected in the random sample, while other submissions were in the wrong format and we could not parse them automatically (those of you with such submissions, pleae fix this by submitting a fix).

## Part 2: Retrieval Augmented Generation system (65 points)

In this part you will try and create a system to answer the queries you (collectively) created in part 1. This may not be easy, but try to answer as many of them as possible. 

This work has four conceptual parts (which interact with each other):

1. Pre-processing and text extraction.
2. Indexing the data.
3. Query formulation and retrieval.
4. RAG-based LLM.

Each one of them have multiple choices and options, which are up to you to explore. We will now describe the different parts and give you potential directions and questions to think about for each stage.

Part of the problem is that we are working with Hebrew, which is more challenging than English: we have fewer existing models at our disposal, we have fewer annotated data resources to train models from, and we have various properties of the language (for example its morphological system, and the writing-without-diacritics (בלי ניקוד) system) which makes it harder than English. But is it the only thing that makes the task in this part harder than Part 1? Think about it while trying to solve it.

### Pre-processing and Text Extraction

We need to answer questions based on text in the כל זכות pages, but these pages come as HTML pages, and contain additional content such as menus, links, etc. We need to process these pages and convert them into textual units which we will then index and retrieve.

**_Extracting content from HTML to text_**

The  following script uses the `Beautiful Soup` (`pip install bs4`) and the `markdownify` (`pip install markdownify`) python packages for parsing HTML and for converting parsed HTML to markdown format. Read it, try to understand it, and make sure that you can make it work.

- [src/extract_content.py](src/extract_content.py)

This is a basic script, which is not meant to be used as is. At a minimum, you want to change the various print statements to write indexable units to some file or files instead. But even beyond that, you may consider tweaking what is extracted from the page, how things are converted to HTML (maybe you want to add some information to some content before converting it to markdown?), and how things are split. This is all up to you to explore (which will be a recurring theme in this part).

**_Deciding What to Index_**

The first step of the process is converting the corpus of HTML pages into textual units you can index (Indexing is discussed in the next section).
In particular, a key question to answer in this stage is "what do we index?" or "what is the basic unit we work with". Do we index entire pages? Or do we index smaller units like paragraphs, or sections, or individual sentences? What is even a paragraph or a section in our case? And what do we do with bulleted lists? We said we don't ask questions about tables, but do we want to keep tables content for indexing and retrieval? will it be useful? or just a distraction? etc.

And, if we index something which is smaller than the entire document (like a section) maybe we want to add to it also other items from the page? For example, we may want our unit of indexing to be a section, or a pair of "page title + section" or "page title + main paragraph + section" and so on. Think about this, it is up to you.

Another option is to index things in multiple levels of granularity: maybe we want to index both the title on its own, _and_ each section on its own, _and_ the entire page, and then the retriever could return any of them.

Another thing to think about is, are there items you want to _not_ index?

The answer to these questions relate a lot to what you will do in the following stages, and you may revise your decisions as you go on, but in any case you must do _something_ at this stage so that you have what to experiment with when indexing.

### Indexing

In this stage the aim is to index the textual units you extracted in the previous stage, towards retrieval. 
The input to this stage is a set of textual units, and the source (URL or file-name or ID) that each unit came from. The output is an index that you can query. In response to the query, you should be able to return:

1. The top K most relevant units.
2. The source of each of these K units.

You may create a single index, or multiple ones. 

We ask you to experiment with both BM25-based indices, _and_ with some dense indexing options (this should be trivial to do technically, as you already implemented the required skeleton codes in part 1).

Here are some models you could consider:

**Sparse, lexical, BM25-based indices**

Sparse lexical indices coupled with BM25-ranking can be very effective. Hebrew does pose a challenge though, as we index exact lexical units, which will make us miss things in case of inflections (if we index אמהות and search for אמא, we won't find it) and prefixes (if we index בית and search for לבית, or index לבית and search for בית). You can try (and are encouraged to do so) to think of ways to mitigate this issue, either at indexing time (for example by either stemming, lemmatizing or adding additional words to the text at indexing time (that is, if we index a string אבג we may change the document to be indexed to include also לאבג, ואבג etc)).

It is also possible to enrich the document with "similar words" (for example obtained by word2vec or a masked-language model) to index in addition to the words in the document.

And finally, you may want to consider filtering some words before indexing.

The following external tools may be of use:

1. The [yap](https://github.com/OnlpLab/yap) (yet another parser) system, an in-grown parser from our research lab at Bar Ilan provides a full morphological analysis and disambiguation for each word in the text. The yap model accepts as input a single sentence (it assumes you already split the text to sentences and space-separated punctuation), and as output it provides the segmentation, lemma, pos tag and morphological features (paradigm cell) of each token. It is very accurate and provides the full analysis in one call. However it requires some preprocessing on your side (splitting the text to sentences and separating punctuation with white spaces), as well as running a server-process on your computer which you call from your code.
   
2. The [trankit](https://trankit.readthedocs.io/en/latest/overview.html) package (`pip install trankit`) is a nicely-packaged and easy-to-use set of core NLP tools (sentence splitting, tokenization, segmentation, pos-tagging, NER, parsing) that work in many languages. While trankit is not as accurate in its segmentation as tools like the [yap](https://github.com/OnlpLab/yap) system, and while it does not contain all of yap's functionality (for example, yap outputs lemmas!), trankit doe not require you to pre-split sentences and punctuation, and is substantially easier to use directly from python. 

3. The [dictabert](https://huggingface.co/collections/dicta-il/dictabert-6588e7cc08f83845fc42a18b) set of models, also developed by researchers affiliated with Bar-Ilan, contain tools for segmentation ([dictabert-seg](https://huggingface.co/dicta-il/dictabert-seg) ) and for lemmatization ([dictabert-lex](https://huggingface.co/dicta-il/dictabert-lex) ). 

4. For a more hands-on, quick-and-dirty approach, that does not require running a computationaly-heavy model, but is a bit hacky and requires some coding, you may find this [lexicon file](https://github.com/yoavg/nlp2024-2025/releases/download/heblex/lexicon.txt) and [prefix lexicon-file](https://github.com/yoavg/nlp2024-2025/releases/download/heblex/prefix-lexicon.txt) to be of use. Each line lists a Hebrew form, followed by its potential morphological analyses and associated lemmas. However, being a static list of words, it does not resolve ambiguities, which you have to handle yourself somehow (or ignore).

**Dense, vector-based indices**

We've seen these in Part 1. The selection of models for Hebrew is not as diverse, and there are no models trained specifically for Hebrew-sentence-similarity, but some Hebrew encoding models do exist, as well as some multilingual models. We list a few of them here, though this is far from being an exhaustive list.

1. **Static word vectors** . You can find pre-trained Hebrew word vectors [here](https://drive.google.com/drive/folders/1qBgdcXtGjse9Kq7k1wwMzD84HH_Z8aJt).
2. **Combined ("pooled") contextual word-vectors**.  For Hebrew, you can use existing pre-trained BERT-like models that are available in the Hugging-face `Transformers` library. Specifically you can use [alephbert-base](https://huggingface.co/onlplab/alephbert-base) or  [dictabert](https://huggingface.co/dicta-il/dictabert).[^2] You can also experiment with _multilingual_ or _crosslingual_ masked language models that were trained on multiple languages, including Hebrew. Examples of such models are [mbert](https://huggingface.co/google-bert/bert-base-multilingual-uncased) and [xlm](https://huggingface.co/FacebookAI/xlm-roberta-base). The [mt5](https://huggingface.co/google/mt5-base) model is another multilingual model trained as an encoder-decoder architecture, from which you can use the encoder component.
3. **Pre-trained text embedder**, which is trained specifically for encoding texts as single vectors for use in similarity or retrieval settings. While no specialized text-embedding model currently exist for Hebrew, there are some "multilingual" ones, that supposedly work with many languages, including Hebrew. 
	- In particular, the [sentence-transformers](https://sbert.net/) package has some [pre-trained multilingual models](https://sbert.net/docs/sentence_transformer/pretrained_models.html#multilingual-models), some of which support Hebrew (`he`).  
	- Models like [intfloat/multilingual-e5-base](https://huggingface.co/intfloat/multilingual-e5-base)  and [intfloat/multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large) are tuned masked language models (so they produce tokens which you have to combine manually for a sentence representation), but they were tuned specifically for retrieval-like similarity tasks.[^5]
	- Finally, LLM APIs of providers like [OpenAI](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings?lang=node) , [Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/embeddings) and [Google](https://ai.google.dev/gemini-api/docs/embeddings) have `embedding` endpoints that will produce results also for Hebrew texts. 

Feel free to experiment! 

Note that the different embedding methods may have a limit on the size of text (number of tokens) that can be encoded in each vector, so you may not be able (and may not want to anyhow) encode complete pages, and have to work with smaller units. 

We note also that while combined contextualized vectors and pre-trained text encoders work rather well for English texts, in Hebrew the vector representations are often sub-optimal. This is a challenge we need to work with. Training dedicated Hebrew text embedders is very much worthwhile, but we do not require or expect it for this assignment.[^3] 

_Techical Note_

Embedding the text units may take some time (maybe up to several hours) on the CPU. We'd recommend saving intermediate results (say, save every K items that you encode). If working on a GPU, it will be much faster to encode a batch of K documents at a time, rather than one by one.

**Enriched Documents**

You may index---in addition to (or even instead of) the document text---also other texts. For example, you may ask an LLM to ask questions about the page, and index the questions. You may ask an LLM to summarize a page, and index the summary. You may translate the text and index the translation. These indices could be either sparse or dense, and the same or separate from your main indices. This is optional of course, but something to think of.

### Retrieval

Now that you have an index, we should perform retrieval to obtain the relevant texts for our query. Retrieval can be very simple: just use the user's query text as your query, and obtain the results. However, it can also be more elaborate: for example, we can:

- use __query enrichment__ to add words to our query (using fixed lists, lexicons, lemmas, static word vectors, completions from contextualized vector models, or by asking an LLM, to name a few options).
- ask an __LLM to convert the question__ into a good query, or into multiple queries.
- use a __method like HyDE__ (discussed in class. Briefly: use an LLM to generate an answer, and then use the answer as the query.)
- make __multiple rounds of retrieval__, where the later rounds depend on the results of the earlier rounds, e.g. pseudo-relevance feedback (or LLM-relevance-feedback).
- etc.

You can be creative here, and it can improve the system.

__Reranking__
Another possibility to do in the retrieval stage is _reranking_: if you want to feed $k$ items to the prompt, retrieve $m \gt k$ items, and then choose the best $k$ of the $m$ based on a stronger model (or an LLM), that sees the query and the item together.

### End-to-end RAG System

Finally, we got to the end-to-end system. Wrap it all together in a system that:

- Gets a query from the user.
- Retrieves relevant documents from the index (or several indices) that you previously created.
- Sends a prompt to an LLM that combines the question and retrieved documents[^4], and instructions to answer the question based on the text in the prompt. Then, return the answer to the user.

This is mostly technical, but tying everything together is important, and the phrasing of the prompt does matter. If you want to go overboard, it will be nicer if the prompt can not only answer the question, but also cite the document (or documents) from which it found the answer, and provide links to them, so that the answers are _grounded_ in concrete sources the user may refer to.

One question to consider though is "how many retrieved items do I include in my prompt". This is something for you to experiment with, try to find a good set.

We will experiment with two setups:

- __Unconstrained__: you can do whatever you want in terms of incorporating retrieved documents.
- **Constrained Token Budget**: here, you are allowed to allocate only a limited number of tokens in the prompt (in this assignment, we set the budget at 1000 tokens) for the retrieved document. How will your design change, if at all, if the retrieved documents you add to the prompt cannot be more than 1000 tokens? (such constraints can arise in practice if you have other things that must fit in the prompt, or if you want to keep inference time very quick. 1000 tokens is an artifically-low constraint for this assignment, but token-budget constraints do exist).

_How should the inputs and outputs look?_

We will not run the code you submit, so do whatever is convenient to you. Something that is easy to do is to, for example, expose the system as a function called "Query" that takes in a string and returns the result. You can then call it several times in a python notebook. Somewhat more elaborate is to have a script that takes the query as a commandline parameter, and another option is to create a quick UI with a system like [streamlit](https://streamlit.io/) (a nice to know system). But really, this is up to you. We will not see this part. It is helpful to have something convenient to work with and look at the results when you develop your system, though.

### Evaluation

We ask you to perform two kinds of evaluation:

1. **End-to-end evaluation**, in which you go from query to final answer. This will have to be done manually. Choose 10-20 queries and manually evaluate their answers. Beyond accuracy, see if you can find common trends. Additionally, see if you can identify cases where the retrieval found the correct document but the overall system produced a wrong answer, or the other way around: cases where the retrieval failed but the system overall produced an adequate answer. Do things change from the unconstrained to the token-budget constrained cases?
2. **Retrieval Evaluation**, here, we evaluate the system on its ability to find the correct page (ignoring the RAG part). Following part 1, we ask you to use two metrics: The first metric is _recall@k_ which measures how many times the correct page was within the top-k retrieved documents (after reranking, if you do them). Use k=5 and k=20. The second metric is MRR. 

Your report should include both the end-to-end evaluation, and also the retrieval evaluation. For the retrieval evaluation, you should report numbers for two sets of queries: 
- Your own _dev-set_ you created in part 1.
- The _test-set_ we release, which is based on queries from all the teams.

We also ask you to submit a file called `ranks.txt` in which each line corresponds to a single query from the _test-set_, and contains two numbers separated by space: `QUERY_ID RANK` where `QUERY_ID` is the ID of the query, and `RANK` is the position in which the human selected (gold) relevant page was returned by your retriever (0 for first position, 1 for second position, etc). If the rank is larger than 1000, write 1000.

Can you think of ways to perform non-manual end-to-end evaluation, given the data you created? Note that we asked you to also include an annotated text-span containing the answer. Can you use this for automatic evaluation of the end-to-end RAG system? How? Discuss this in your report.

## What to submit

**For part 2**, submit 

(1) **The predictions file** `ranks.txt`

(2) **Code** for your pre-processing, indexing, retrieval and RAG parts (if you use API keys, be sure to remove them from the code before submitting). Include also a `README.md` file that describes which files belong to which part. 

We will not try to run the code, but we will look at it.

(3) **a detailed report** in a file called `report.pdf` which should include:
- Your names
- A description of your system and the choices you made. We should be able to understand how your system works in all the different parts, and especially the key choices and key points that are required to replicate it. If something worked particularly well, specify it. Structure this part with a dedicated section for each of the stages: pre-processing, indexing (sparse and dense), retrieval, RAG (unconstrained and budget-constrained).
- The evaluation results you obtained.
- If you experimented with different methods and ideas, it is good to describe not only what worked, but also what didn't work.
- What would you have implemented if you had unlimited time and compute resources? What would be an ideal approach that you think would work very well? Be specific, e.g. don’t say general things like “I will train my own similarity model” but describe on what kind of data you will train it.
- Any additional thoughts you had based on the assignment, or ideas you may have.
- A discussion of the challenges of part 2 compared to part 1, what are their causes, and what do you think is needed to overcome them.

Your grade will be based mostly on the report, so invest time in it! Of course, a good report must be based on good work. You will be assessed on your solution, its robustness and its creativity, as well as the effort you put into it and, if you didn't manage to find a strong solution, the alternatives you tried and approaches you took. However, doing good work is not enough: if you fail to report it properly, we would not know the work that you did... so be sure to describe your work clearly, fully and concisely.

## Good luck!

# Footnotes

[^2]: In both cases, make sure that you use the representation vectors and not the vocabulary-prediction vectors, which are much larger (use `AutoModel` and not `AutoModelForMaskedLM`). 
[^3]: Unless you really really want to, in which case you are encouraged to try, it may work very well. The `sentence-transformers` package provides training code. You still need to figure out which text-pairs to train them on, of course. A Hebrew QA dataset such as [HeQ](https://github.com/NNLP-IL/Hebrew-Question-Answering-Dataset?tab=readme-ov-file) is a natural candidate, though it is unclear how effective it will be for our setup.
[^4]: Note that you can include exactly what you retrieved, or something a bit different. For example, if you retrieved a piece of text that resulted from page X, you may include in the prompt also additional information from page X, if you think it is useful.
[^5]: These could fit in either this or the former category. On the one hand they produce a vector for each token and not a single vector for the text. On the other hand, they were trained specifically for the semantic-similarity / retrieval tasks. 

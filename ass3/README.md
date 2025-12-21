# Intro to NLP 2025-2026, Assignment 3.

**Prompting, question generation, and evaluation.**

## Introduction

In this assignment we will take a task we discussed in class (Question Generation), attempt to perform it using calls to an LLM, assess the results in various ways, and discuss our results.

## The Task

The task we attempt to perform is called Questuion Generation (QG) and is defined as follows:

> Given a short text and a span within the text, generate all the questions whose answer, based on the text, is the given span.
> The generated set of questions should be comprehensive (ask all the semantically different questions) but also distinct (if two questions in a set are just paraphrases of each other, we should be aware of it and treat them as the same question).
> The questions should be grammatically valid, fluent, and naturally sounding.

**For example**, given the text "_The focus on this assignment is Question Generation, an NLP task that is concerned with generating questions_" and the span "Question Generation", the set {"_what is the focus of this assignment?_", "_what is the name of the NLP task?_" } is comprehensive and covers the two questions that can be asked based on the text whose answer is "_Question Generation_". The two questions "_what is the name of the NLP task?_" and "_how is the NLP task called?_" are paraphrases of one another and are considered as the same question.

## The Data

You will work with a set of 100 text-span pairs that we extracted from the [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) dataset. 

The data is in the following file:

- [data.jsonl](data.jsonl)

Each line in the file is a JSON object representing one text-span pair and several questions about it. The SQuAD data-collection was not meant to be exhaustive, so the set of questions may or may not be comprehensive.

In case you are interested or find this useful, the complete SQuAD training set, in HuggingFace format, is available [here](https://huggingface.co/datasets/rajpurkar/squad_v2). This set includes also the ones in the `data.jsonl` file above.

## Part 1: Manual Annotation

Select 20 text-span pairs from the file. Without looking at the provided questions, annotate (generate a comprehensive set of questions) for each of the 20 text-span pairs. We will call these manually generated questions the _gold annotation_ set (or _the gold set_ for short).

**Output of this part:**

- A file (`annotations.jsonl`) with your annotations in a JSON format to your choosing.
- Short discussion of your effort and reflection of the process, in the report.

## Part 2: Automatic Generation

Use an LLM API to perform the question generation task. For each of the text-span pairs in `data.jsonl`, you need to use the LLM to generate a good and comprehensive set of questions. Do your best to get high-quality results. Try and experiment with different prompting techniques, and different query formulations, as you deem relevant for the task.

**Output of this part:**

- A file (`generations.jsonl`) with generated questions, in the same JSON format as the previous part.
- A description of your final method, and discussion on why you chose it and how it compared to other methods you tried.


## Part 3: Basic Statistics

How many questions on average were generated for each pair? What is the distribution of number-of-questions over the entire set? How long on average is each question (choose a length metric that makes sense to you). Compare the numbers to the ones in your annotated set.

**Output of this part:**

- Readable graphs and/or tables with the above information.
- A brief discussion of the results and what you learn from them.

Both of these items should be incorporated in your report.

## Part 4: Automatic Evaluation via the ROUGE Metric

**Essential Preliminaries**

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is a set of metrics used for evaluating the quality of generated content by models, particularly in the context of text summarization and long-form answer generation.
The ROUGE metric focuses on comparing the generated text against one (or more) human-generated references.

There are different variants of the ROUGE metric:

- **ROUGE-N**: This measures n-gram overlap between the generated and reference texts. The higher the overlap, the better the score. Commonly used n-grams are:
- **ROUGE-1**: Overlap of unigrams (single words).
- **ROUGE-2**: Overlap of bigrams (two-word sequences).
- **ROUGE-L**: This metric captures the longest common subsequence (LCS) between the generated text and reference. 
- **ROUGE-W**: This is a weighted version of ROUGE-L that takes into account the length of the LCS, emphasizing longer matches more significantly.

All versions of ROUGE provide measurements of:
   - Recall: The proportion of n-grams in the reference text that are also found in the generated text.
   - Precision: The proportion of n-grams in the generated text that are found in the reference text.
   - F1 Score: The harmonic mean of recall and precision, providing a single score to summarize the balance between the two.

ROUGE is very widely used as a computationally efficient way to assess the quality of generated text. However, as shall be seen shortly, it has advantages but also disadvantages, and it is often advised to complement ROUGE with qualitative evaluations to capture aspects of coherence, relevance, and readability not reflected by the n-gram overlap alone.

**Your task***

Evaluate the generated questions using ROUGE, using your manual annotations as the gold set.

In order to use ROUGE to evaluate the generated question sets, we will view the set of questions as a single piece of text to be evaluated. For each set of questions, order the questions alphabetically, wrap each question with `<BOQ>` (Begin of Question) and `<EOQ>` markers, and concatenate them into a single string where each wrapped question is separated by a newline. Do this once for the gold set (g) and once for the predicted set (p), and compute ROUGE between `g` and `p`.

_Which rouge metrics?_

- use the [rouge-score](https://github.com/google-research/google-research/tree/master/rouge) python package (`pip install rouge-score`) to compute the ROUGE-2, ROUGE-L and ROUGE-W scores for each of your 20 (g,p) pairs in the evaluation set.
- Compute an average ROUGE-2, average ROUGE-L and average ROUGE-W of all pairs.

Note that the way we compute ROUGE scores over the sets of questions by linearizing each set into a single string and comparing ROUGE between two strings representing sets, is not ideal (why?). You are encouraged to think of better alternatives (and possibly also to implement them).

Write down your results (the different ROUGE scores you obtained) and observations based on them.

**Output of this part:**

Discuss the following items in your pdf report:

1) Add to your report a table that, for each of the text+answer pair in your evaluation set, provides its ROUGE-2 ROUGE-L and ROUGE-W scores (Precision, Recall, F), and a summary line reporting the averages of all metrics over the 20 questions.
2) For each of the metrics (ROUGE-2 ROUGE-L and ROUGE-W) look at the best F score, worst F score and a middle-way F score in the table. Now fetch the corresponding sets from your evaluation and rank the triplet manually. For each of these metrics, does the order provided by the metric reflects your own judgment of which question is better? Among the three ROUGE variants, does any one variant reflect your judgment better than the others? If you had to choose only one version, which one would you go for an why?
3) Reflect on our use of ROUGE for evaluating question generation. What are the pros and cons of using ROUGE in general, and of the way we used ROUGE here? Can you think of a different way to use ROUGE for evaluating the quality of the questions? Can you think of other variants not considered here, for evaluating question generation
4) If you experimented with alternative ways to use ROUGE over the question sets, describe and discuss these efforts as well.


## Part 5: Validation using an LLM

A common practice is to use a process that involves an LLM as a **validator**. Here, we check the quality of the generated questions based on the LLM's ability to handle them. 

In a "real-life" process, usually this part acts as quality assurance (if many questions are not handled well by the LLM, maybe the entire process is bad), or, more commonly, as a filter (if only a small number of questions are not handled well, maybe we should just throw them---or the pairs they are in---out of the set). Another use is to build a more elaborate process that attempts to improve the items the LLM validator failed on. **In this work** we will just perform the validation and record the result (i.e., we will count, but will not filter).

Concretely, you need to validate the ability of the LLM to answer the generated questions, based on the text, and get the same (or equivalent) answers  to the original spans. Do this by writing a strong prompt template that will receive instructions, text and question, and answer the question based on the text. Run this on all the generated questions, record the answers, and validate them.

A related quantity we ask you to compute is the ability of the model to answer the questions _without seeing the texts_ while providing the same (or equivalent) answers as those based on the texts.

This part should be based on the entire set (100 pairs), and not just the 20 annotated pairs. You should compute numbers both based on the entire set, and based on the 20 pairs for which you have gold annotations.

**Output of this part:**

- A description of your procedure / prompts.
- The LLM's output (`validation_outputs.jsonl`).
- Readable graphs and/or tables with the above information.
- A brief discussion of the results and what you learn from them.

Your JSON format should include all the requested items, in a way that is understandable and clear to an external reader.

## Part 6: Evaluation using an LLM ("LLM as a judge")

Another way of using an LLM is to use them directly as evaluators of quality. Here, we wish the LLM to directly answer two questions related to the quality of the questions:

1) Is the question grammatical and fluent?

2) Is the question answerable from the text, and if so, is the answer according to the text consistent with the original intended answer?

Note that question (2) relies on the same information the LLM verification process was intended to measure, but here we ask the LLM to assess it directly, while in the validation case we ask the LLM to perform the task and the we interpret the results ourselves --- a different computational process.

It is interesting to note if these processes agree or disagree with each other, and the implications of this.

Like the previous one, this part should also be based on the entire set (100 pairs), and not just the 20 annotated pairs. You should compute numbers both based on the entire set, and based on the 20 pairs for which you have gold annotations.

For answering questions 1 and 2, you need to decide on some scale (is it just binary? or maybe more graded? is it numeric or categorical? etc). We leave this decision up to you, please describe it in your report.

**Output of this part:**

- A description of your procedure / prompts.
- The LLM's output. (`llm_judge_outputs.jsonl`)
- Readable graphs and/or tables with the above information (evaluation of the generated questions according to each metric).
- A brief discussion of the results and what you learn from them.

Your JSON format should include all the requested items, in a way that is understandable and clear to an external reader.

## Part 7: Manual Evaluation

Finally, we want you to perform manual evaluation. Use the 20 text-span pairs you fully annotated.

For each one, assess the different questions generated by the LLM.

First, for each question, use the exact two criteria we asked the LLM above:

1) Is the question grammatical and fluent?

2) Is the question answerable from the text, and if so, is the answer according to the text consistent with the original intended answer?

We also ask you to answer another criteria:

3) Is the question "good" (in your judgement)

Finally, we want you to evaluate the generated _set_ of questions: 

4) For each of the 20 text-span pairs, is the _set of questions_ exhaustive? Compare it to your gold annotation, are all questions covered? Are there questions in one set and not in the other? Are there repeated questions? Etc.


Again, some of these questions require deciding on a scale. Decide and describe your decision and its reasoning.

**Output of this part:**

- A description of your procedure.
- Readable graphs and/or tables with the above information (evaluation of the generated questions according to each metric).
- A brief discussion of the results and what you learn from them.

## Part 8: Wrapping it up

Write a summary of the entire process and the overall results. What did you learn from it? Focus on the correlations between the different metrics and techniques, and what we can learn from them. Discuss also the strengths and weaknesses of the different approaches, specific challenges you found, etc.

Include also a discussion of the idea to use an LLM to evaluate the outputs of the same LLM. What are your general thoughts about the idea? Is it a good idea in general? If so, why, if no, why not. Is it a good idea sometimes? If so, when, and when not. What can it measure, and what can’t it measure? Can it be used as a replacement for human evaluation? If so, when. If not, why not. Etc.


**Output of this part:**

- The concluding chapter of your report.

## What to submit:

- **A single report file in PDF format**, including your answers (tables, graphs, methods, discussions) from the different parts. Include your names and IDs clearly at the top of the report file. Make it clear which part of your report answers which section, and make clear what each graph/table/answer/... in the report represents or answers.
- The following files:
    - `annotations.jsonl`
    - `generations.jsonl`
    - `validation_outputs.jsonl`
    - `llm_judge_outputs.jsonl`

As in the previous assignments, a large part of your grade will be based on your report / essay.









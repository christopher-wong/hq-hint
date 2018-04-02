# import itertools
import re
# import time
# from collections import defaultdict

from unidecode import unidecode

import search, firebase

punctuation_to_none = str.maketrans({key: None for key in "!\"#$%&\'()*+,-.:;<=>?@[\\]^_`{|}~�"})
punctuation_to_space = str.maketrans({key: " " for key in "!\"#$%&\'()*+,-.:;<=>?@[\\]^_`{|}~�"})

class colors:
    blue = '\033[94m'
    red = "\033[1;31m"
    green = '\033[0;32m'
    end = '\033[0m'
    bold = '\033[1m'


async def answer_question(question, original_answers):
    print("Searching...")
    # start = time.time()

    # build object for firebase
    question_block = {
        "question": question,
        "ans_1": original_answers[0],
        "ans_2": original_answers[1],
        "ans_3": original_answers[2]
    }

    # sync questions without answer to the server
    firebase.sync_questions(question_block)

    question = unidecode(question)

    answers = []
    for ans in original_answers:
        ans = unidecode(ans)
        answers.append(ans.translate(punctuation_to_none))
        answers.append(ans.translate(punctuation_to_space))
    answers = list(dict.fromkeys(answers))
    # print(answers)

    question_lower = question.lower()

    reverse = "NOT" in question or\
              ("least" in question_lower and "at least" not in question_lower) or\
              "NEVER" in question

    quoted = re.findall('"([^"]*)"', question_lower)  # Get all words in quotes
    no_quote = question_lower
    for quote in quoted:
        no_quote = no_quote.replace(f"\"{quote}\"", "1placeholder1")

    question_keywords = search.find_keywords(no_quote)
    for quote in quoted:
        question_keywords[question_keywords.index("1placeholder1")] = quote

    # print(question_keywords)
    search_results = await search.search_google("+".join(question_keywords), 5)
    # print(search_results)

    search_text = [x.translate(punctuation_to_none) for x in await search.get_clean_texts(search_results)]

    best_answer, counts = await __search_method1(search_text, answers, reverse)
    if best_answer == "":
        best_answer, counts = await __search_method2(search_text, answers, reverse)

    print(colors.green + best_answer + "\n" + colors.end)

    # add the best answer to the question_block and push to the server
    results = []

    for i, ans_count in enumerate(counts.values()):
        results.append({
            "count": ans_count,
            "ans": f"ans_{i + 1}",
        })

    firebase.sync_results(question_block, results)

    with open('questions.csv', 'a') as file:
        # writes a CSV with these values to disk
        # question, answer1, answer2, answer3, predicted_answer
        file.write("\t".join([question, question_block["ans_1"], question_block["ans_2"], question_block["ans_3"], best_answer, "\n"]))
        file.close()

    # print(f"Search took {time.time() - start} seconds")
    return ""


async def __search_method1(texts, answers, reverse):
    """
    Returns the answer with the maximum/minimum number of exact occurrences in the texts.
    :param texts: List of text to analyze
    :param answers: List of answers
    :param reverse: True if the best answer occurs the least, False otherwise
    :return: Answer that occurs the most/least in the texts, empty string if there is a tie
    """
    print("Running method 1")
    counts = {answer.lower(): 0 for answer in answers}

    for text in texts:
        for answer in counts:
            counts[answer] += len(re.findall(f" {answer} ", text))

    # print(counts)

    # If not all answers have count of 0 and the best value doesn't occur more than once, return the best answer
    best_value = min(counts.values()) if reverse else max(counts.values())
    if not all(c == 0 for c in counts.values()) and list(counts.values()).count(best_value) == 1:
        return (min(counts, key=counts.get) if reverse else max(counts, key=counts.get)), counts
    return "", counts


async def __search_method2(texts, answers, reverse):
    """
    Return the answer with the maximum/minimum number of keyword occurrences in the texts.
    :param texts: List of text to analyze
    :param answers: List of answers
    :param reverse: True if the best answer occurs the least, False otherwise
    :return: Answer whose keywords occur most/least in the texts
    """
    print("Running method 2")
    counts = {answer: {keyword: 0 for keyword in search.find_keywords(answer)} for answer in answers}

    for text in texts:
        for keyword_counts in counts.values():
            for keyword in keyword_counts:
                keyword_counts[keyword] += len(re.findall(f" {keyword} ", text))

    # print(counts)
    counts_sum = {answer: sum(keyword_counts.values()) for answer, keyword_counts in counts.items()}

    if not all(c == 0 for c in counts_sum.values()):
        return (min(counts_sum, key=counts_sum.get) if reverse else max(counts_sum, key=counts_sum.get)), counts_sum
    return "", counts_sum

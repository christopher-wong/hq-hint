# import libs
import urllib.parse, requests

# import Bsoup
from bs4 import BeautifulSoup

class colors:
    blue = '\033[94m'
    red = "\033[0;31m"
    green = '\033[1;32m'
    end = '\033[0m'
    bold = '\033[1m'


def google(question, num):
    """
        given a list of queries, this function Google's them as a concatenated string.

    """

    params = {"q": question, "num": num}
    url_params = urllib.parse.urlencode(params)
    google_url = "https://www.google.com/search?" + url_params

    r = requests.get(google_url)

    soup = BeautifulSoup(r.text, "html.parser")
    spans = soup.find_all('span', {'class': 'st'})

    text = " ".join([span.get_text() for span in spans]).lower().strip()

    return text


def rank_answers(question_block):
    """
        Ranks answers based on how many times they show up in google's top 50 results.

        If the word " not " is in the question is reverses them.
        If theres a tie breaker it google the questions with the answers

    """

    # print("rankings answers...")

    question = question_block["question"]
    ans_1 = question_block["ans_1"].lower()
    ans_2 = question_block["ans_2"].lower()
    ans_3 = question_block["ans_3"].lower()

    reverse = True

    if " not " in question.lower():
        print("reversing results...")
        reverse = False

    text = google(question, 50)

    results = []

    results.append({"ans": ans_1, "count": text.count(ans_1)})
    results.append({"ans": ans_2, "count": text.count(ans_2)})
    results.append({"ans": ans_3, "count": text.count(ans_3)})

    sorted_results = []

    sorted_results.append({"ans": ans_1, "count": text.count(ans_1)})
    sorted_results.append({"ans": ans_2, "count": text.count(ans_2)})
    sorted_results.append({"ans": ans_3, "count": text.count(ans_3)})

    sorted_results.sort(key=lambda x: x["count"], reverse=reverse)

    # if there's a tie redo with answers in q

    if (sorted_results[0]["count"] == sorted_results[1]["count"]):
        # build url, get html
        # print("running tiebreaker...")

        text = google([question, ans_1, ans_2, ans_3], 50)

        results = []

        results.append({"ans": ans_1, "count": text.count(ans_1)})
        results.append({"ans": ans_2, "count": text.count(ans_2)})
        results.append({"ans": ans_3, "count": text.count(ans_3)})

    return results

def print_results(results):
    """
        Prints the results

    """

    print(colors.blue + "\n" + "-" * 15)
    print("Jake's method: \n" + colors.end)

    small = min(results, key=lambda x: x["count"])
    large = max(results, key=lambda x: x["count"])

    for (i, r) in enumerate(results):
        text = "%s - %s" % (r["ans"], r["count"])

        if r["ans"] == large["ans"]:
            print(colors.green + text + colors.end)
        elif r["ans"] == small["ans"]:
            print(colors.red + text + colors.end)
        else:
            print(text)

    print(colors.blue + "-" * 15 + colors.end)

    return large['ans'] if large['ans'] else ""

# def main():
#
#     data = {
# 		"question": "Which astronomer did NOT discover three famous laws of motion?",
# 		"ans_1": "Newton",
# 		"ans_2": "Galileo",
# 		"ans_3": "Kepler",
#     }
#
#     results = rank_answers(data)
#
#     answer = print_results(results)
#     print(answer)
#
# main()

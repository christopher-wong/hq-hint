import urllib.parse, requests
from bs4 import BeautifulSoup
from modules.colors import colors


def google(question_list, num):
    """
        given a list of queries, this function Google's them as a concatenated string.

    """

    params = {"q": " ".join(question_list), "num": num}
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

    text = google([question], 50)

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

    final_answer = ""

    if reverse:
        final_answer = max(results, key=lambda x: x["count"])
        print("{} Backup answer: {} - {}{}".format(colors.blue, final_answer["ans"], final_answer["count"], colors.end))
    else:
        final_answer = min(results, key=lambda x: x["count"])
        print("{} Backup answer: {} - {}{}".format(colors.blue, final_answer["ans"], final_answer["count"], colors.end))

    return results, "{} - {}".format(final_answer["ans"], final_answer["count"])

def print_results(results):
    """
        Prints the results

    """

    small = min(results, key=lambda x: x["count"])
    large = max(results, key=lambda x: x["count"])

    for (i, r) in enumerate(results):
        text = "%s - %s" % (r["ans"], r["count"])

        print(text)
        # if r["ans"] == large["ans"]:
        #     print(colors.green + text + colors.end)
        # elif r["ans"] == small["ans"]:
        #     print(colors.red + text + colors.end)
        # else:
        #     print(text)

    print(colors.blue + "-" * 15 + colors.end)

    return ""

# def main():
#
#     data = {
# 		"question": "What does a thermometer primarily measure?",
# 		"ans_1": "Hope",
# 		"ans_2": "Temperature",
# 		"ans_3": "Distance",
#     }
#
#     results, final_answer = rank_answers(data)
#
#
#
# main()

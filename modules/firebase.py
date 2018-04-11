import requests, json

def new_game():
    data = {
        "question": "<small style='color: gray;'>Game is live</small><br><br>Waiting for them to stop _______ ?",
        "ans_1": "Dancing",
        "ans_2": "Chirping",
        "ans_3": "Talking",
        "ans_1_count": 0,
        "ans_2_count": 100,
        "ans_3_count": 20,
        "correct_ans": "ans_2",
        "thinking": False,
        "live": True,
        "backup": "none",
    }

    url = "https://hqhint-hosted.firebaseio.com/q1.json"
    r = requests.put(url, data=json.dumps(data))
    # print(r.text)

def standby(next_show_time):
    data = {
        "question": "<small style='color: gray;'>Check back next game.</small><br><br>What does this site do?",
        "ans_1": "Nothing",
        "ans_2": "Sells your data to CA",
        "ans_3": "Predicts HQ answers",
        "ans_1_count": 0,
        "ans_2_count": 40,
        "ans_3_count": 100,
        "correct_ans": "ans_3",
        "thinking": False,
        "live": False,
        "backup": "none",
        # "next_show": next_show_time,
    }

    url = "https://hqhint-hosted.firebaseio.com/q1.json"
    r = requests.put(url, data=json.dumps(data))
    # print(r.text)

def sync_questions(question_block):
    """
        uploads question data to firebase

    """
    data = {
        "question": question_block["question"],
        "ans_1": question_block["ans_1"],
        "ans_2": question_block["ans_2"],
        "ans_3": question_block["ans_3"],
        "ans_1_count": 0,
        "ans_2_count": 0,
        "ans_3_count": 0,
        "correct_ans": "",
        "thinking": True,
        "live": True,
        "backup": question_block['backup'],
    }

    url = "https://hqhint-hosted.firebaseio.com/q1.json"
    r = requests.put(url, data=json.dumps(data))
    # print(r.text)

def sync_results(question_block, results):
    """
        uploads results data to firebase (after googling)

    """

    # print(results)

    to_check = max(results, key=lambda x: x["count"])

    if " not " in question_block["question"].lower():
        to_check = min(results, key=lambda x: x["count"])

    correct_ans = ""

    for (i, r) in enumerate(results):
        if r["ans"] == to_check["ans"]:
            correct_ans = "ans_%s" % (i + 1)

    # select_answer = False

    # for result in results:
    #     if result["count"] != 0:
    #         select_answer = True
    #         break
    #
    # if not select_answer:
    #     correct_ans = ""

    data = {
        "question": question_block["question"],
        "ans_1": question_block["ans_1"],
        "ans_2": question_block["ans_2"],
        "ans_3": question_block["ans_3"],
        "ans_1_count": results[0]["count"],
        "ans_2_count": results[1]["count"],
        "ans_3_count": results[2]["count"],
        "correct_ans": correct_ans,
        "backup": question_block["backup"],
        "thinking": False,
        "live": True,
    }

    url = "https://hqhint-hosted.firebaseio.com/q1.json"
    r = requests.put(url, data=json.dumps(data))
    # print(r.text)

# new_game()
# standby()
with open('questions.csv', 'a') as file:
    # writes a CSV with these values to disk
    # question, answer1, answer2, answer3, predicted_answer
    file.write("\t".join(["Question", "Answer1", "Answer2", "Answer3", "predicted" + "\n"]))
    file.close()
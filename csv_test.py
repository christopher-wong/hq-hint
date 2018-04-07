import csv

with open('questions.csv', 'a') as file:
    # writes a CSV with these values to disk
    # question, answer1, answer2, answer3, predicted_answer
    # file.write(delimiter="\5","\t ".join(["goose", "trator", "muffin", "garbage", "trash" + "\n"]))
    # file.close()
    writer = csv.writer(file)
    writer.writerow(["car", "baby", "doggy, dog"])

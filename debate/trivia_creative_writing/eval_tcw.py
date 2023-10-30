import json
import openai
import numpy as np
import time
import re
import os

def parse_bullets(sentence):
    bullets_preprocess = sentence.split("\n")
    bullets = []

    for bullet in bullets_preprocess:
        try:
            idx = bullet.find(next(filter(str.isalpha, bullet)))
        except:
            continue

        bullet = bullet[idx:]

        if len(bullet) != 0:
            bullets.append(bullet)

    return bullets


def test_output(output, groundtruch):
    # test whether the output includes all the answers of the trivia questions
    correct_count = 0
    question_count = len(groundtruch)
    for ans_to_question in groundtruch:
        for ans in ans_to_question:
            # compare all to lower
            if ans.lower() in output.lower():
                correct_count += 1
                break
    info = {'correct_count': correct_count, 'question_count': question_count, 'accuracy': correct_count/question_count}
    return info
    
def parse_answer(input_str):
    writings = input_str.split("\\boxed")
    concat = ""
    for sen in writings:
        sen = re.sub("{|}|", "", sen)
        concat+=sen

    return concat

if __name__ == "__main__":
    path = os.getcwd()+"/debate/trivia_creative_writing/tcw_3_2.json"
    response_dict = json.load(open(path, "r"))

    questions = list(response_dict.keys())

    accuracies = []

    for question in questions:
        responses, gt = response_dict[question]

        pred_solutions = []
        for response in responses:
            pred_solution = parse_answer(response[-1]['content'])

            pred_solutions.append(pred_solution)
            # cannot use most frequent here, so use longest
        max_len_pred = max(pred_solutions, key=len)
        accurate_info = test_output(max_len_pred, gt)
        accurate = accurate_info['accuracy']

        if accurate is not None:
            accuracies.append(float(accurate))
        else:
            import pdb
            pdb.set_trace()
            print(gt)

    print("accuracies:", np.mean(accuracies), np.std(accuracies) / (len(accuracies) ** 0.5))
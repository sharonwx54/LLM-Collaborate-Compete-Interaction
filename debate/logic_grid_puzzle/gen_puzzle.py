from glob import glob
import pandas as pd
import json
import time
import random
import openai
import os
from tqdm import tqdm
import re


def construct_message(agents, question, idx):
    if len(agents) == 0:
        return {"role": "user", "content": "Can you double check that your answer is correct. Put your final answer in the form (X) at the end of your response."}

    prefix_string = "These are the solutions to the problem from other agents: "

    for agent in agents:
        agent_response = agent[idx]["content"]
        response = "\n\n One agent solution: ```{}```".format(agent_response)

        prefix_string = prefix_string + response

    prefix_string = prefix_string + \
        """\n\n Using the reasoning from other agents as additional advice, can you give an updated answer? Examine your solution and that other agents step by step. Put your answer in the form (X) at the end of your response.""".format(
            question)
    return {"role": "user", "content": prefix_string}


def construct_assistant_message(completion):
    content = completion["choices"][0]["message"]["content"]
    return {"role": "assistant", "content": content}


def generate_answer(answer_context):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=answer_context,
            n=1)
    except:
        print("retrying due to an error......")
        time.sleep(20)
        return generate_answer(answer_context)

    return completion


def parse_question_answer(context):
    inputs = context["inputs"]
    alphabet = ["A", "B", "C", "D", "E"]
    alphabet_mapping = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E"}
    matches = re.findall(r'choice: (.*?)(\s|$)', inputs)
    choice_text = ""
    for i in range(len(matches)):
        choice_text += alphabet[i] + ") " + matches[i][0] + '\n'

    question = re.sub(r'\?[^?]*$', '?', inputs)

    question = "Can you answer the following question as accurately as possible? {}\n{}Explain your answer, putting the answer in the form (X) at the end of your response.".format(
        question, choice_text)

    answer = alphabet_mapping[context["targets"][0]]

    return question, answer


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")

    agents = 3
    rounds = 2

    data_path = "/Users/pamela/Documents/11667/LLM-Collaborate-Compete-Interaction/data/logic_grid_puzzle/logic_grid_puzzle_200.jsonl"
    with open(data_path, 'r') as f:
        question_list = [json.loads(line) for line in f]

    response_dict = {}

    # for i in tqdm(range(len(question_list))):
    for i in tqdm(range(100, 200)):
        context = question_list[i]
        question, answer = parse_question_answer(context)

        agent_contexts = [[{"role": "user", "content": question}]
                          for agent in range(agents)]

        for round in range(rounds):
            for i, agent_context in enumerate(agent_contexts):

                if round != 0:
                    agent_contexts_other = agent_contexts[:i] + \
                        agent_contexts[i+1:]
                    message = construct_message(
                        agent_contexts_other, question, 2 * round - 1)
                    agent_context.append(message)

                completion = generate_answer(agent_context)

                assistant_message = construct_assistant_message(completion)
                agent_context.append(assistant_message)
                print(completion)

        response_dict[question] = (agent_contexts, answer)

    json.dump(response_dict, open(
        "puzzle_{}_{}-100-200.json".format(agents, rounds), "w"))

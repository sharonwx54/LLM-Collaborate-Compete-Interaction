from glob import glob
import pandas as pd
import json
import time
import random
import openai
import os
from tqdm import tqdm
import sys
import path

directory = path.Path(__file__).abspath()
# setting path
sys.path.append(directory.parent.parent.parent)
from prompts.massive_multitask_language_understanding import spp_prompt


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
        # openai.api_key = ""
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=answer_context,
            n=1)
    except:
        print("retrying due to an error......")
        time.sleep(20)
        return generate_answer(answer_context)

    return completion


def parse_question_answer(data, i):

    question = data[i]["question"]
    subject = data[i]["subject"]
    answer = data[i]["answer"]

    return question, answer, subject


def get_data(data_file):
    with open(data_file, "r") as f:
        data = [json.loads(line) for line in f]
    return data


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")

    agents = 3
    rounds = 2

    data = get_data(
        "data/massive_multitask_language_understanding/massive_multitask_language_understanding.jsonl")

    random.seed(0)
    response_dict = {}

    for i in tqdm(range(len(data))):
        # for i in tqdm(range(20)):

        question, answer, subject = parse_question_answer(data, i)

        agent_contexts = [[{"role": "user", "content": spp_prompt.format(question=question, subject=subject)}]
                          for agent in range(agents)]

        print(agent_contexts)
        print(answer)

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
                print(completion["choices"][0]["message"]["content"])

        response_dict[question] = (agent_contexts, answer)

    json.dump(response_dict, open(
        "mmlu_{}_{}-200-spp-debate.json".format(agents, rounds), "w"))

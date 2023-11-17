import openai
import os
import json
import numpy as np
import random
import path
import sys 

directory = path.Path(__file__).abspath()
# setting path
sys.path.append(directory.parent.parent.parent)

from prompts.trivia_creative_writing import spp_prompt

def construct_message(agents, question, idx):
    if len(agents) == 0:
        return  {"role": "user", 
                 "content": "Can you double check that your answer is correct. Please reiterate your answer, with your final answer a single paragraph, in the form \\boxed{{answer}}."}

    prefix_string = "These are the solutions to the problem from other agents: "

    for agent in agents:
        agent_response = agent[idx]["content"]
        response = "\n\n One agent solution: ```{}```".format(agent_response)

        prefix_string = prefix_string + response

    prefix_string = prefix_string + """\n\n Using the solutions from other agents as additional information, can you provide your answer to the trivia creative writing task? \n The original trivia creative writing task is {}. Your final answer should be a single paragraph, in the form \\boxed{{answer}}, at the end of your response.""".format(question)
    return {"role": "user", "content": prefix_string}


def construct_assistant_message(completion):
    content = completion["choices"][0]["message"]["content"]
    return {"role": "assistant", "content": content}


def read_jsonl(path: str):
    with open(path) as fh:
        return [json.loads(line) for line in fh.readlines() if line]

if __name__ == "__main__":
    agents = 3
    rounds = 2
    random.seed(0)

    generated_description = {}
    # print(os.getcwd())
    questions = read_jsonl("/Users/sharonzhang/Desktop/LLM-Collaborate-Compete-Interaction/data/trivia_creative_writing/trivia_creative_writing_100_n_5.jsonl")
    random.shuffle(questions)

    for data in questions:
        topic = data['topic']
        q_list = data['questions']
        parse_q_list = " ".join(q_list)
        topic_q_list = "Write story about {} answering the following questions: ".format(topic)+parse_q_list
        ans_list = data['answers']
        numq = len(q_list)

        agent_contexts = [[{"role": "user", 
                            "content":  spp_prompt.format(topic=topic, n=numq, questions=parse_q_list)}] for agent in range(agents)]


        for round in range(rounds):
            for i, agent_context in enumerate(agent_contexts):

                if round != 0:
                    agent_contexts_other = agent_contexts[:i] + agent_contexts[i+1:]
                    message = construct_message(agent_contexts_other, topic_q_list, 2*round - 1)
                    agent_context.append(message)

                completion = openai.ChatCompletion.create(
                          model="gpt-3.5-turbo-0301",
                          messages=agent_context,
                          n=1)

                assistant_message = construct_assistant_message(completion)
                agent_context.append(assistant_message)

        generated_description[topic_q_list] = (agent_contexts, ans_list)

    json.dump(generated_description, open(
        "tcw_spp_{}_{}.json".format(agents, rounds), "w"))

    import pdb
    pdb.set_trace()
    print(ans_list)
    print(agent_context)

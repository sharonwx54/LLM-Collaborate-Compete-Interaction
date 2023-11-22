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
                 "content": "Can you double check that your writing is correct. Please reiterate your writing, with your final writing a single paragraph, in the form \\boxed{{answer}}."}

    prefix_string = "These are the writing to the problem from other agents: "

    for agent in agents:
        agent_response = agent[idx]["content"]
        response = "\n\n One agent writing: ```{}```".format(agent_response)

        prefix_string = prefix_string + response

    prefix_string = prefix_string + """\n\n Using the writing from other agents as additional information, can you provide your answer to the trivia creative writing task? \n The original trivia creative writing task is {}. Your final answer should be a single paragraph, in the form \\boxed{{answer}}, at the end of your response.""".format(question)
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
    count = 0
    for data in questions[0:5]:
        if count > 0 and count % 20 == 0:
            print ("finish {} number of tasks".format(count))
        topic = data['topic']
        q_list = data['questions']
        parse_q_list = " ".join(q_list)
        topic_q_list = "Write story about {} answering the following questions: ".format(topic)+parse_q_list
        ans_list = data['answers']
        numq = len(q_list)

        agent_contexts = [[{"role": "user", 
                            "content":  spp_prompt.format(
                                topic=topic, n=numq, questions=parse_q_list
                                )}] for agent in range(agents-1)
                        ]+[[{"role": "user", 
                            "content":  """When faced with a task, begin by identifying the participants who will contribute to solving the task. Then, initiate a multi-round collaboration process until a final solution is reached. The participants will give critical comments and detailed suggestions whenever necessary. Recall previous examples you seen. Write a short and coherent story about {topic} that incorporates the answers to the following {num} questions: {questions}. Explain your reasoning. Your final answer should be a single paragraph, in the form \\boxed{{answer}}, at the end of your response. """.format(topic=topic, num=numq, questions=parse_q_list)}
                                ]]


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
        count+=1

    json.dump(generated_description, open(
        "tcw_spp_{}_{}.json".format(agents, rounds), "w"))

    import pdb
    pdb.set_trace()
    print(ans_list)
    print(agent_context)

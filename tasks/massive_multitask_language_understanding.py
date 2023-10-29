import os
import re
from tasks.base import Task, DATA_PATH
from prompts.massive_multitask_language_understanding import spp_prompt
import json
# from models import gpt

class MMLUTask(Task):
    def __init__(self, file='massive_multitask_language_understanding.jsonl'):
        super().__init__()
        path = os.path.join(DATA_PATH, 'massive_multitask_language_understanding', file)
        with open(path, "r") as f:
            self.data = [json.loads(line) for line in f]
        
        samples=[12553,  4313,  3717,  4249,  4821, 10625,  8654,  1534,  5837,
        1819,  4466, 12334,  6575,  2334, 11926,  5798,  3018, 12676,
       13774,  6009,  6099,  5792,  5152,  2444,  6873,  8459,  7753,
       13317,   817,  7837,  4850,  2898,  3136,  5390,  3379, 11414,
       10809,  5717,    74,   826, 13878, 10723,  3018,  1209, 12861,
        6225,  8244,  8630, 12540,  1589,  4236,   931,   801,   392,
       12793,  4360,  3880,  4524,  7678, 12727,  1395,  4293,  2222,
       12456, 13338,   583,  2964,  1685,  5308,  9742,  2488,  3921,
        5317,  4500,  5871,  9967, 12147,  2396, 12114, 13947,   863,
        8524,  6800,  7113,  4434,  9672,  9703,   776,  1652,  5776,
        1002,  7834,  9198, 13146,  8851,  5107,  5028,  5000,  8293,
        2349,   756,  2261,  3695,  5290, 11560,  8578, 13184,  2917,
        5064,  7929,  4522,  5275, 10536,  1961,  8956,  4599, 11398,
        2542, 12571,  3931,  3968,  8146,  5468, 12405,  4411, 13091,
       13560,  4073, 11102,  4580,  5121,   307,  6593,  1995, 10222,
       10577,  5045,   224, 10265,  2488,  5345,   621,  8720,  2693,
        6285, 10244,  1860,  5457,  6676,   721, 11546,  3142,  9513,
        4664,  7566,   569,   700,  8774, 11200,  4116,  4863,  6439,
       10113, 13770, 10800,  7600,  5991,  8850,  7118,  8830,  1163,
        1632,  6278,  2148,   704, 12825,  4693,  9454,  6083,  8226,
       12180,  1319, 10689,  4123,  9576, 10139,  1501,  2775,  7304,
       13229,  2630,  8907, 10130,  3434,   482, 13879,  8272,  3389,
       11252, 10732]
        
        self.data = [self.data[x] for x in samples]
        print(len(self.data))

    def __len__(self) -> int:
        return len(self.data)

    def get_input(self, idx: int):
        return self.data[idx]

    def get_input_prompt(self, idx: int, method: str, **kwargs) -> str:
        datapoint = self.data[idx]
        question = datapoint["question"]
        subject = datapoint["subject"]
        
        if method == "spp":
            input_prompt = spp_prompt.format(question=question, subject=subject)
        else:
            raise NotImplementedError(f"method {method} not implemented")
        
        return input_prompt

    def test_output(self, idx: int, output: str):
        # test whether the output includes all the answers of the trivia questions
        instance = self.data[idx]
        target = instance["answer"]
        
        info = {'correct': False}

        if target.lower().strip() == output.lower().strip()[0]:
            info['correct'] = True

        return info

    @staticmethod
    def prompt_unwrap(response: str, method: str):
        '''
            response: raw genration from the model
            return:
                - str: the story
                - bool: whether the story is successfully parsed from the raw genration
        '''
        if method == "standard":
            return response, True
        
        elif method == "cot":
            if "Story:" in response:
                return response.split("Story:")[1].strip(), True
            elif "story:" in response:
                return response.split("story:")[1].strip(), True
            else:
                return response, False
        
        elif method in ["spp","spp_profile","spp_fixed_persona"]:
            if "Final answer:" in response:
                return response.split("Final answer:")[1].strip(), True
            elif "final answer:" in response:
                return response.split("final answer:")[1].strip(), True
            else:
                return response, False
        
        else:
            raise NotImplementedError(f"method {method} not implemented")
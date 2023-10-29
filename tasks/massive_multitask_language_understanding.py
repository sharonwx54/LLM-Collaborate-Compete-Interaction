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
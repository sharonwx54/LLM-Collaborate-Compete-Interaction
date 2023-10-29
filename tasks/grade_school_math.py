import os
import re
from tasks.base import Task, DATA_PATH
# from prompts.grade_school_math import standard_prompt, cot_prompt, spp_prompt, spp_prompt_profile, spp_prompt_fixed_persona
from prompts.grade_school_math import spp_prompt
import json
# from models import gpt

def parse_answer(text):
    pattern = r'\d+'

    # Use re.findall to find all matches of the pattern in the text
    matches = re.findall(pattern, text)

    # If matches are found, convert the first match to an integer and return it
    if matches:
        number = int(matches[0])
        return number
    else:
        return None
class GradeSchoolMathTask(Task):
    def __init__(self, file='grade_school_math.jsonl'):
        super().__init__()
        path = os.path.join(DATA_PATH, 'grade_school_math', file)
        with open(path, "r") as f:
            self.data = [json.loads(line) for line in f]

    def __len__(self) -> int:
        return len(self.data)

    def get_input(self, idx: int):
        return self.data[idx]

    def get_input_prompt(self, idx: int, method: str, **kwargs) -> str:
        datapoint = self.data[idx]
        question = datapoint["question"]
        # answer = datapoint["answer"]
        
        # if method == "standard":
        #     input_prompt = standard_prompt.format(question=question)
        # elif method == "cot":
        #     input_prompt = cot_prompt.format(question=question)
        if method == "spp":
            input_prompt = spp_prompt.format(question=question)
        # elif method == "spp_fixed_persona":
        #     input_prompt = spp_prompt_fixed_persona.format(question=question)
        # elif method == "spp_profile":
        #     input_prompt = spp_prompt_profile.format(question=question)
        else:
            raise NotImplementedError(f"method {method} not implemented")
        
        return input_prompt
    

    
    def test_output(self, idx: int, output: str):
        instance = self.data[idx]
        answer = instance["answer"]
        info = {'correct': False}
        print("output", parse_answer(output), answer.split("####")[1].strip())
        if str(parse_answer(output)) == answer.split("####")[1].strip():
            print("output", parse_answer(output))
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
        
        # elif method == "cot":
        #     if "Story:" in response:
        #         return response.split("Story:")[1].strip(), True
        #     elif "story:" in response:
        #         return response.split("story:")[1].strip(), True
        #     else:
        #         return response, False
        
        elif method in ["spp","spp_profile","spp_fixed_persona"]:
            if "Final answer:" in response:
                return response.split("Final answer:")[1].strip(), True
            elif "final answer:" in response:
                return response.split("final answer:")[1].strip(), True
            else:
                return response, False
        
        else:
            raise NotImplementedError(f"method {method} not implemented")
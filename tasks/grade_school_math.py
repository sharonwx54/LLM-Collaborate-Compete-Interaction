import os
import re
from tasks.base import Task, DATA_PATH
# from prompts.grade_school_math import standard_prompt, cot_prompt, spp_prompt, spp_prompt_profile, spp_prompt_fixed_persona
from prompts.grade_school_math import spp_prompt, spp_compete_prompt
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
def parse_answer_compete( input_str):
    pattern = r"\{([0-9.,$]*)\}"
    matches = re.findall(pattern, input_str)

    solution = None

    for match_str in matches[::-1]:
        solution = re.sub(r"[^0-9.]", "", match_str)
        if solution:
            break

    return solution
def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        current_frequency = List.count(i)
        if current_frequency > counter:
            counter = current_frequency
            num = i

    return num
def solve_math_problems(input_str):
    pattern = r"\d+\.?\d*"

    matches = re.findall(pattern, input_str)
    if matches:
        return matches[-1]

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
        if method == "spp_compete":
            input_prompt = spp_compete_prompt.format(question=question)
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
        # print("output", parse_answer(output), answer.split("####")[1].strip())
        if str(parse_answer(output)) == answer.split("####")[1].strip():
            # print("output", parse_answer(output))
            info['correct'] = True
        return info
    
    def test_output_compete(self, idx: int, output: list):
        instance = self.data[idx]
        answer = instance["answer"]
        output_vote = most_frequent(output)
        info = {'correct': False}
        if float(output_vote) == float(answer.split("####")[1].strip()):
            print("output", output_vote)
            info["correct"] = True
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
        elif method in ["spp_compete"]:
            
            if "Final answer:" in response:
                response =  response.split("Final answer:")[1].strip()
            elif "final answer:" in response:
                response = response.split("final answer:")[1].strip()
            # print("response test",response)
            pred_answer = parse_answer_compete(response)
            if pred_answer is None:
                pred_answer = solve_math_problems(response)
            return pred_answer, True
        else:
            raise NotImplementedError(f"method {method} not implemented")
        
    
    def construct_message(self, agents, agent_answer_idx:int, question_idx: int):
        datapoint = self.data[question_idx]
        question = datapoint["question"]
        # print("question",question)
        if len(agents) == 0:
            return {"role": "user", "content": "Can you double check that your answer is correct. Please reiterate your answer, with your final answer a single numerical number, in the form \\boxed{{answer}}."}

        prefix_string = "When faced with a task, begin by identifying the participants who will contribute to solving the task. Then, initiate a multi-round collaboration process until a final solution is reached. The participants will give critical comments and detailed suggestions whenever necessary. These are the solutions to the problem from other agents: "

        for agent in agents:
            # agent_response = agent[idx]["content"]
            agent_response = agent[agent_answer_idx]
            # print(agent_response)
            response = "\n\n One agent solution: ```{}```".format(agent_response)

            prefix_string = prefix_string + response

        prefix_string = prefix_string + """\n\n Using the solutions from other agents as additional information and identify the participants and collaboratively solve the following task step by step. Can you provide your answer to the math problem? \n The original math problem is {}. Your final answer should be a single numerical number, in the form \\boxed{{answer}}, at the end of your response.""".format(question)
        return {"role": "user", "content": prefix_string}
    
    def construct_assistant_message(self, completion):
        print("completion",completion)
        content = completion.choices[0].message.content
        return {"role": "assistant", "content": content}
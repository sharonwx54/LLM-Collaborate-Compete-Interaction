import pandas as pd
import json
import re

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

count = 0
with open ("logs/grade_school_math/grade_school_math.jsonl__method-spp_engine-gpt-3.5-turbo_temp-0.0_topp-1.0_start0-end100__with_sys_mes.jsonl", "r") as f:
    for line in f:
        result = json.loads(line)
        output = result["unwrapped_output"][0]
        correct_answer = result["task_data"]["answer"].split("####")[1].strip()
        
        if "Final Answer" in output:
            answer = output.split("Final Answer:")[1]
            digit_answer = parse_answer(answer)
            
        elif "Fianl answer" in output:  
            answer = output.split("Fianl answer:")[1]
            digit_answer = parse_answer(answer)

        elif "final answer" in output:
            answer = output.split("final answer:")[1]
            digit_answer = parse_answer(answer)
        else:
            answer = output
            try:
                digit_answer = parse_answer(answer)
            except:
                print(output)
        if str(digit_answer) == str(correct_answer):
            count += 1
    print("ACC:",count/100)
            # digit_answer = parse_answer(answer)
            # print(result['unwrapped_output'])
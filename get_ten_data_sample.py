import json

prev_log_name = "grade_school_math.jsonl__method-spp_engine-gpt-3.5-turbo_temp-0.0_topp-1.0_start0-end100__with_sys_mes.jsonl"
with open(prev_log_name, 'r') as json_file:
    json_list = list(json_file)

dataset_name = '/Users/shenmengjie/Desktop/LLM-Collaborate-Compete-Interaction/data/grade_school_math/grade_school_math.jsonl'
with open(dataset_name, 'r') as json_file:
    json_list_2 = list(json_file)

correct = []
incorrect = []
for i in range(len(json_list)):
    json_str = json_list[i]
    result = json.loads(json_str)
    # print(result)
    if not result["test_output_infos"][0]["correct"]:
        if len(incorrect) < 10:
            incorrect.append(json_list_2[i])
    else:
        if len(correct) < 10:
            correct.append(json_list_2[i])

with open("incorrect.json", "w") as outfile:
    for i in incorrect:
        outfile.write(i)

with open("correct.json", "w") as outfile:
    for i in correct:
        outfile.write(i)
    


    

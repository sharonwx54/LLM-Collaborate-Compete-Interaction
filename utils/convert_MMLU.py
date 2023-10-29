import pandas as pd
import os
import json

output_filename='massive_multitask_language_understanding.jsonl'
path = os.path.join(
            './data', 'massive_multitask_language_understanding','data','test')

subjects = sorted([f.split("_test.csv")[0] for f in os.listdir(path) if "_test.csv" in f])
print(subjects)
subjects = ['college_biology','college_computer_science','college_medicine','econometrics','high_school_european_history','high_school_physics','high_school_us_history','machine_learning','marketing','world_religions']

choices = ['A','B','C','D']

with open(output_filename, 'w') as output:
    question_id=0
    for subject in subjects:
        df = pd.read_csv(os.path.join(path, subject + "_test.csv"), header=None)[:20]
        for i in range(len(df)):
            prompt=""
            for idx, choice in enumerate(choices):
                prompt+=('\n'+choice+". "+str(df[idx+1][i]))
            prompt = df[0][i] + prompt + '\nAnswer:'
            answer = df[5][i]

            l = subject.split("_")
            s = ""
            for entry in l:
                s += " " + entry
            
            row = {'idx':question_id,'subject':s,'question':prompt,'answer':answer}
            json.dump(row,output)
            output.write("\n")
            question_id+=1

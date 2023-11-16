# MODEL="gpt4-32k" # your engine name

MODEL="gpt-3.5-turbo"

DATA_FILE="grade_school_math.jsonl"

START_IDX=0
END_IDX=100

# choose method
# METHOD="spp" # ['standard','cot','spp', 'spp_profile', 'spp_fixed_persona']
METHOD="spp_compete"
# w/ or w/o system message (spp works better w/ system message)
SYSTEM_MESSAGE="You are an AI assistant that helps people find information." # or "" (empty string)

# conda activate llms-class-hw2
# pip3 install -r requirements.txt

python3 run.py \
    --model ${MODEL} \
    --method ${METHOD} \
    --task grade_school_math_combine \
    --task_data_file ${DATA_FILE} \
    --task_start_index ${START_IDX} \
    --task_end_index ${END_IDX} \
    --system_message "${SYSTEM_MESSAGE}" \
    ${@}
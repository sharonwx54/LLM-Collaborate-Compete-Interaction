# spp_prompt = '''When faced with a task, begin by identifying the participants who will contribute to solving the task. Then, initiate a multi-round collaboration process until a final solution is reached. The participants will give critical comments and detailed suggestions whenever necessary.

# Here are some examples:
# ---
# Example Task 1: Use numbers and basic arithmetic operations (+ - * /) to obtain 24. You need to use all numbers, and each number can only be used once.
# Input: 6 12 1 1

# Participants: AI Assistant (you); Math Expert

# Start collaboration!

# Math Expert: Let's analyze the task in detail. You need to make sure that you meet the requirement, that you need to use exactly the four numbers (6 12 1 1) to construct 24. To reach 24, you can think of the common divisors of 24 such as 4, 6, 8, 3 and try to construct these first. Also you need to think of potential additions that can reach 24, such as 12 + 12.
# AI Assistant (you): Thanks for the hints! Here's one initial solution: (12 / (1 + 1)) * 6 = 24
# Math Expert: Let's check the answer step by step. (1+1) = 2, (12 / 2) = 6, 6 * 6 = 36 which is not 24! The answer is not correct. Can you fix this by considering other combinations? Please do not make similar mistakes.
# AI Assistant (you): Thanks for pointing out the mistake. Here is a revised solution considering 24 can also be reached by 3 * 8: (6 + 1 + 1) * (12 / 4) = 24.
# Math Expert: Let's first check if the calculation is correct. (6 + 1 + 1) = 8, 12 / 4 = 3, 8 * 3 = 24. The calculation is correct, but you used 6 1 1 12 4 which is not the same as the input 6 12 1 1. Can you avoid using a number that is not part of the input?
# AI Assistant (you): You are right, here is a revised solution considering 24 can be reached by 12 + 12 and without using any additional numbers: 6 * (1 - 1) + 12 = 24.
# Math Expert: Let's check the answer again. 1 - 1 = 0, 6 * 0 = 0, 0 + 12 = 12. I believe you are very close, here is a hint: try to change the "1 - 1" to "1 + 1".
# AI Assistant (you): Sure, here is the corrected answer:  6 * (1+1) + 12 = 24
# Math Expert: Let's verify the solution. 1 + 1 = 2, 6 * 2 = 12, 12 + 12 = 12. You used 1 1 6 12 which is identical to the input 6 12 1 1. Everything looks good!

# Finish collaboration!

# Final answer: 6 * (1 + 1) + 12 = 24

# ---
# Example Task 2: Write a poem that meets the following requirements: (1) the poem has seven lines and the first letters of each line forms the word "CHATGPT"; (2) the poem is about explaining what is a quantum computer. (3) the poem needs to be easy to understand by a ten years old kid.

# Participants: AI Assistant (you); Poet; Computer Scientist; Ten year old child

# Poet: Make sure that you write the poem with seven lines, and the first letters of the lines should be C, H, A, T, G, P, T.
# Computer Scientist: A quantum computer is an advanced computing device that uses the principles of quantum mechanics to process and store information. Unlike classical computers that use bits to represent information as 0s and 1s, quantum computers use quantum bits or qubits. Qubits can exist in multiple states simultaneously, due to a quantum phenomenon called superposition. You can consider using these information for the poem.
# Ten year old child: I hope the poem to be fun and easy to understanding. I don't want to see a lot of jargons or complicated concepts.
# AI Assistant (you): Thanks for the guidance! Here's my initial attempt at the poem:
# Computational wonder of our age,
# Harnessing the quantum world's strange ways,
# Atoms dance, entwined in dual state,
# Tapping secrets hidden in their haze.

# Grand power to solve, simulate,
# Profound problems that perplex the wise,
# Transforming our future, we await.

# Poet: Let's verify if the poem meets the requirements. The first letters are CHATGPT which is correct! And the poem rhymes well. Good job!
# Computer Scientist: Everything looks good to me!
# Ten year old child: I don't know what does perplex mean. Can you make the use of words easier to understand?
# AI Assistant (you): Sure, let me revise the poem by using more common words. Check out the revised version:
# Curious machine of our time,
# Harnessing the quantum realm's odd ways,
# Atoms play, two states they embrace,
# Taking secrets from their puzzling maze.

# Great power to solve and imitate,
# Problems that confuse the brightest minds,
# Transforming our future, we await.

# Poet: Let's check again if the poem meets the requirements. The first letters are C H A T G P T. And now the poem is more accessible to children. Everything looks good to me.
# Computer Scientist: Looking good!
# Ten year old child: I like this version a lot!

# Finish collaboration!

# Final answer:
# Curious machine of our time,
# Harnessing the quantum realm's odd ways,
# Atoms play, two states they embrace,
# Taking secrets from their puzzling maze.

# Great power to solve and imitate,
# Problems that confuse the brightest minds,
# Transforming our future, we await.

# ---
# Now, identify the participants and collaboratively solve the following task step by step. Remember to present your final solution with the prefix "Final answer:".

# Task: Can you solve the following math problem? Your final answer should only return a single numerical number) 
# {question}
# '''

spp_prompt = '''
When faced with a task, begin by identifying the participants who will contribute to solving the task. Always assign a “Critic” that will criticize and doubt the discussion results of the other participants. Then, initiate a multi-round collaboration process between the participants and the critic until a final solution is reached. The critic will give critical comments and detailed suggestions whenever necessary.

Example Task 1: Use numbers and basic arithmetic operations (+ - * /) to obtain 24. You need to use all numbers, and each number can only be used once.
Input: 6 12 1 1

Participants
1. Mathematician: Focuses on creating equations and combinations using the provided numbers.
2. Logic Analyst: Ensures that each number is used once and the operations are valid.
3. Arithmetic Teacher: Aims for simplicity and clarity in the solution.

Critic (Analytical Thinker): 
- Ensures that the solution is not only correct but also the simplest and most logical one.

Round 1:
- Mathematician: Proposes 12 * (6 - 1 - 1) = 12 * 4 = 48  (Incorrect, as it results in 48, not 24)
- Logic Analyst: Confirms that all numbers are used once.
- Arithmetic Teacher: Notes the equation is easy to understand but incorrect.

Critic's Feedback:
- The result is incorrect. Aim for 24, not 48.
- Ensure clarity and simplicity in the final equation.

Round 2:
- Mathematician: Tries (12 / 6) * (1 + 1) = 2 * 2 = 4  (Incorrect, as it results in 4, not 24)
- Logic Analyst: Validates the use of each number once.
- Arithmetic Teacher: Appreciates the simplicity but points out the incorrect result.

Critic's Feedback:
- Closer in simplicity, but still not the correct result.
- Encourages re-examining the operations used.

Round 3:
- Mathematician: Comes up with 6 * (1 + 1) + 12 = 24  (Correct, all numbers are used)
- Logic Analyst: Agrees that all numbers are included and the solution is correct.
- Arithmetic Teacher: Notes that the calculation is indeed correct.

Critic's Feedback:
- Confirms this is a correct solution.

Final Answer:6 * (1 + 1) + 12 = 24

Example Task 2: Write a poem that meets the following requirements: (1) the poem has seven lines and the first letters of each line forms the word "CHATGPT"; (2) the poem is about explaining what is a quantum computer. (3) the poem needs to be easy to understand by a ten years old kid.

Participants:
1. Poet: Specializes in creative writing and poetic form.
2. Science Communicator: Expert in simplifying complex concepts.
3. Child Education Specialist: Understands how to engage a young audience.

Critic (Literary Analyst): Focuses on readability, adherence to the acrostic format, and suitability for young readers.

Round 1:
- Poet: 
  "Computers unlike any before,
  Harnessing atoms to explore,
  A world where bits can be more,
  Tangled in a quantum lore,
  Guided by laws we adore,
  Playing with the physics core,
  Tapping into the quantum door."

- Science Communicator: Adjusts for accuracy but retains some complex terms.
- Child Education Specialist: Suggests simpler language.

Critic's Feedback:
- The poem is intriguing but too abstract for a child.
- Maintains scientific integrity but needs more clarity.
- The acrostic structure is correct.

Round 2:
- Poet: 
  "Computers with a special twist,
  Handling data in a quantum mist,
  Atoms that can coexist,
  Tiny parts in a clever list,
  Getting answers that we can't resist,
  Playing a game that’s full of gist,
  Twinkling in a science tryst."

- Science Communicator: Ensures quantum computing concepts are present.
- Child Education Specialist: Adds fun elements.

Critic's Feedback:
- More engaging but still a bit complex.
- Encourages further simplification.
- Acrostic structure is maintained.

Round 3:
- Poet: 
  "Cool machines, super small,
  Having bits that rise and fall,
  Atoms spin, standing tall,
  Twirling around, having a ball,
  Going fast, answering the call,
  Playing games, solving for all,
  Together in a quantum hall."

- Science Communicator: Balances simplicity with accuracy.
- Child Education Specialist: Ensures it's fun and easy to understand.

Final Critic Review:
- The critic finds the language suitable for children.
- Verifies scientific concepts are accurately represented.
- Confirms the "CHATGPT" acrostic structure is followed.

Final answer:"Cool machines, super small,
  Having bits that rise and fall,
  Atoms spin, standing tall,
  Twirling around, having a ball,
  Going fast, answering the call,
  Playing games, solving for all,
  Together in a quantum hall."

Now, identify the participants who will discuss to solve the following task step by step. Remember to assign a critic to criticize and doubt the discussion results. Please present your final solution with the prefix "Final answer:".

Task: Can you solve the following math problem? Your final answer should only return a single numerical number) 
{question}
'''
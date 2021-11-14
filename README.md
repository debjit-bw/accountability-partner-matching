# Overview

To make a matching algorithm to pair up accountability partners. It ingests data points and outputs a list of matches (users).

<u><b>User</b></u>: One who has enrolled in the program and is waiting for matches.


&nbsp;
## How the matching algorithm works

### Find similar people:
- Actively filters the sample space based on gender preference (M, F, Any)
- Groups people into 2 categories:
    - C1: Age bracket (+-) 5 years [Value 5 may be changed for edge cases]
    - C2: Other people
- Score each category based on passion_vector similarity
- For C1, express passion similarity out of 100 and scale it by 3/2 for people with occupation match
- For C2, express passion similarity out of 100 and allow only those with an occupation match and halve score for others
- Sort all users based on score

### Find different people:
- Actively filters the sample space based on gender preference (M, F, Any)
- Groups people into 2 categories:
    - C1: Age bracket (+-) 5 years [Value 5 may be changed for edge cases]
    - C2: Other people
- Score each category based on 100 minus passion_vector similarity
- For C1, express passion similarity out of 100 and scale it by 3/2 for people with occupation match
- For C2, express passion similarity out of 100 and allow only those with an occupation match and halve score for others
- Sort all users based on score

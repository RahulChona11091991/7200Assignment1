# 720 Assignment 1

This project has 3 main components.

# Question1.py File
# Data Folder
  - allPosts.tsv
  - allPosts-metadata.tsv
  - askerAnswerer.tsv
  - asker-answerer-giant.tsv
  # RCommands Folder
    - 720 Assignment1 .R file
    
In "Question1.py" file, you will find complete implementation of quering stackoverflow using StackOverflow API with some filters as per assignment requirements for extracted 1000 Questions and all their answers.

# EndPoint Used: https://api.stackexchange.com/2.2


# Data Folder
# allPosts.tsv file contains
  - All questions and answers as "post"
  - Attributes of the file
    - poster_user_id
    - post_type
    - question_id
    - is_answered
    - question_title
    - answer_count
    - view_count
    - answer_id
    - answer_creation_date
    - is_accepted
    - question_creation_date
    
# Assumption
- 'na' represnts not applicable.
- '0' represnts not applicable.

---------------------------------------------------------------------------------------------------------

# allPosts-metadata.tsv file contains
  - Metadata about all questions and answers (as "post")
  - Attributes of the file
    - user_id
    - question_id
    - post_type
    - answer_id
    
# Assumption
- 'na' represnts not applicable.
- '0' represnts not applicable.

---------------------------------------------------------------------------------------------------------

# askerAnswerer.tsv
- Contains edges from Question Asker to Answerer user
- Attributes of the file
    - asker_uid
    - answerer_uid
    - question_id

# Assumption
- 'na' represnts not applicable.
- '0' represnts not applicable.

---------------------------------------------------------------------------------------------------------  
  
# asker-answerer-giant.tsv
- Contains giant components of the graph
- Attributes of the file
    - asker_uid
    - answerer_uid
  
---------------------------------------------------------------------------------------------------------    
  
# RCommands Folder
- File name: 720 Assignment1 .R
- This folder contains implementation 
  - Importing data fetched from StackOverflow using API mentioned above
  - Generating Network Graph 
  - Extracting Components
  - Extracting Giant Components out of network graph.
  - Ploting Network Graph and its Giant Component seperately.
  

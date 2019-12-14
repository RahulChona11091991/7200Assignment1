import pandas as pd
import csv


###
### PRUNING CONSTANTS
### modify to change pruning behaviour
###

PRUNE_REMOVE_NON_ANSWERED_QUESTIONS = True
PRUNE_MIN_QUESTION_TOTAL_UPVOTE_COUNT = 2
PRUNE_MIN_USER_ANSWERS = 2




def loadFile(file):
  return pd.read_csv(file, sep='\t')


### LOAD DATA

# Load questions
df_questions = loadFile('./data/allPosts.tsv')

post_type = df_questions["post_type"].values
df_questions = df_questions[ post_type=='question' ]


# Load answers
df_answers = loadFile('./data/allPosts.tsv')
post_type = df_answers["post_type"].values
df_answers = df_answers[ post_type=='answer' ]


# Load users
df_users = loadFile('./data/allUsers.tsv')



### PRUNE DATA


# Prune users
# Keep only users that have posted at least one question, or
# have posted no questions, but have posted at least 2 answers
total_questions = df_users["total_questions"].values
total_answers = df_users["total_answers"].values
df_users = df_users[ ((total_questions > 0) | ((total_questions == 0) & (total_answers >= PRUNE_MIN_USER_ANSWERS))) ]

# Write to file
df_users.to_csv('./data/allUsers_pruned.tsv',sep='\t', quoting=csv.QUOTE_NONE, index=False)


# Prune questions
# Keep only questions with:
#   1) is_answered = yes
#   2) question_max_answer_upvote >= 2

# Keep only is_answered=yes
if PRUNE_REMOVE_NON_ANSWERED_QUESTIONS:
    is_answered = df_questions["is_answered"].values
    df_questions = df_questions[ is_answered=='yes' ]

# Keep only question_total_answer_upvote >= 2
df_questions["question_total_answer_upvote"] = pd.to_numeric(df_questions["question_total_answer_upvote"])
question_total_answer_upvote = df_questions["question_total_answer_upvote"].values
df_questions = df_questions[ question_total_answer_upvote >= PRUNE_MIN_QUESTION_TOTAL_UPVOTE_COUNT ]
# 1621 remaining


# Add answers to above dataframe (only if not pruned)
for index, answer in df_answers.iterrows():
    question_id = answer['question_id']
    user_id = answer['user_id']
    if question_id in df_questions['question_id'].values and user_id in df_users['user_id'].values:
        df_questions = df_questions.append(answer, ignore_index=True)


# Write to file
df_questions.to_csv('./data/allPosts_pruned.tsv',sep='\t', quoting=csv.QUOTE_NONE, index=False)

# Write to metaData file:
df_questions = df_questions[['user_id', 'post_type', 'question_id', 'answer_id']]
df_questions.to_csv('./data/allPosts-metaData_pruned.tsv',sep='\t', quoting=csv.QUOTE_NONE, index=False)

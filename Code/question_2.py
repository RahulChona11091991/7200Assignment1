import pandas as pd



### Clear output files and write headers
with open('./data/1-ARN.tsv', 'w+') as output:
    # output.write('asker_uid\tanswerer_uid\tquestion_id\t\n')
    output.write('from\tto\n')

with open('./data/2-ABAN.tsv', 'w+') as output:
    # output.write('askerId\tbestAnswererId\tquestionId\tbestAnswerId\tmaxUpvoteCount\n')
    output.write('from\tto\n')

with open('./data/3-CBEN.tsv', 'w+') as output:
    # output.write('nonBestAnswererId\tbestAnswererId\tquestionId\tbestAnswerId\tmaxUpvoteCount\n')
    output.write('from\tto\n')

with open('./data/4-VBEN.tsv', 'w+') as output:
    # output.write('nonBestAnswererId\tbestAnswererId\tanswerersEdgeWeight\tquestionId\tbestAnswerId\tmaxUpvoteCount\n')
    output.write('from\tto\tweight\n')

with open('./data/5-VBEN2.tsv', 'w+') as output:
    # output.write('askerId\tanswererId\taskerAnswererEdgeWeight\tnonBestAnswererId\tbestAnswererId\taskerAnswererEdgeWeight\tquestionId\tbestAnswerId\tmaxUpvoteCount\n')
    output.write('from\tto\tweight\n')


# Load data
def loadFile(file):
    return pd.read_csv(file, sep='\t')



# Load posts
df_posts = loadFile('./data/allPosts_pruned.tsv')


for index, post in df_posts.iterrows():
    user_id = post['user_id']
    post_type = post['post_type']
    question_id = post['question_id']
    answer_id = post['answer_id']

    if post_type == 'answer':
        answer_max_upvote = post['answer_max_upvote']
        answer_up_vote_count = post['answer_up_vote_count']

        asker_id = df_posts['user_id'][ (df_posts['question_id'] == question_id) & (df_posts['post_type'] == 'question') ].values[0]
        question_up_vote_count = df_posts['question_up_vote_count'][ (df_posts['question_id'] == question_id) & (df_posts['post_type'] == 'question') ].values[0]

        with open('./data/1-ARN.tsv', 'a+') as output:
            output.write('{}\t{}\n'.format(
                asker_id,
                user_id,
            ))

        # Best answerer (highest upvote value)
        if answer_max_upvote == 'yes':
            with open('./data/2-ABAN.tsv', 'a+') as output:
                output.write('{}\t{}\n'.format(
                    asker_id,
                    user_id,
                ))

        # Non-best answerer (not highest upvote value)
        else:
            # Determine if there is any best answerer
            best_answerer_id = df_posts['user_id'][ (df_posts['question_id'] == question_id) & (df_posts['post_type'] == 'answer') & (df_posts['answer_max_upvote'] == 'yes') ].values

            if len(best_answerer_id) > 0:
                best_answerer_id = best_answerer_id[0]

                with open('./data/3-CBEN.tsv', 'a+') as output:
                    output.write('{}\t{}\n'.format(
                        user_id,
                        best_answerer_id,
                    ))

        # Check for other answers for this question, with lower scores
        asker_ids = df_posts['user_id'][ (df_posts['question_id'] == question_id) & (df_posts['post_type'] == 'answer') & (df_posts['answer_up_vote_count'] < answer_up_vote_count) & (df_posts['user_id'] != user_id) ].values

        for user in asker_ids:
            other_answer_up_vote_count = df_posts['answer_up_vote_count'][ (df_posts['question_id'] == question_id) & (df_posts['post_type'] == 'answer') & (df_posts['user_id'] == user) ].values[0]

            with open('./data/4-VBEN.tsv', 'a+') as output:
                output.write('{}\t{}\t{}\n'.format(
                    user,
                    user_id,
                    (answer_up_vote_count-other_answer_up_vote_count)
                ))

            with open('./data/5-VBEN2.tsv', 'a+') as output:
                output.write('{}\t{}\t{}\n'.format(
                    user,
                    user_id,
                    (answer_up_vote_count-other_answer_up_vote_count)
                ))

        # Check if question_up_vote_count > answer_up_vote_count
        if question_up_vote_count < answer_up_vote_count:
            with open('./data/5-VBEN2.tsv', 'a+') as output:
                output.write('{}\t{}\t{}\n'.format(
                    asker_id,
                    user_id,
                    (answer_up_vote_count-question_up_vote_count)
                ))

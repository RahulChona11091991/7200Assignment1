import requests
from pandas import read_csv
import numpy as np

# write file header
with open('./allPosts.tsv', 'w+') as output:
    output.write('poster_user_id\tpost_type\tquestion_id\tis_answered\tquestion_title\tanswer_count\tview_count\tanswer_id\tanswer_creation_date\tis_accepted\tquestion_creation_date\n')

with open ('./allPosts-metadata.tsv', 'w+') as output:
    output.write('user_id\tquestion_id\tpost_type\tanswer_id\n')


#Assignment 2 - Start
with open ('./ARN.tsv', 'w+') as output:
    # output.write('asker_uid\tanswerer_uid\tquestion_id\t\n')
    output.write('from\tto\n')

with open ('./ABAN.tsv', 'w+') as output:
    # output.write('askerId\tbestAnswererId\tquestionId\tbestAnswerId\tmaxUpvoteCount\n')
    output.write('from\tto\n')

with open ('./CBEN.tsv', 'w+') as output:
    # output.write('nonBestAnswererId\tbestAnswererId\tquestionId\tbestAnswerId\tmaxUpvoteCount\n')
    output.write('from\tto\n')

with open ('./VBEN.tsv', 'w+') as output:
    # output.write('nonBestAnswererId\tbestAnswererId\tanswerersEdgeWeight\tquestionId\tbestAnswerId\tmaxUpvoteCount\n')
    output.write('from\tto\tweight\n')

with open ('./VBEN2.tsv', 'w+') as output:
    # output.write('askerId\tanswererId\taskerAnswererEdgeWeight\tnonBestAnswererId\tbestAnswererId\taskerAnswererEdgeWeight\tquestionId\tbestAnswerId\tmaxUpvoteCount\n')
    output.write('from\tto\tweight\n')

#Assignment 2 - Complete

# Fetch Questions and answers
for index in range(5):
    url = 'https://api.stackexchange.com//2.2/questions?page={}&pagesize=100&fromdate=1514764800&todate=1569801600&order=desc&sort=activity&tagged=python&site=stackoverflow&filter=!BHrIhNpdLSrQDA*mgWaaqI0fLxig0y'.format(index+1)

    print('URL: {}'.format(url))
    requestObj = requests.get(url = url)
    data = requestObj.json()
    print data
    for i2 in data['items']:

        # check if answer exists, then execute
        if i2['answer_count'] > 0:

            maxUpvoteCount = 0
            askerId = ''
            bestAnswererId = ''
            questionId = ''
            bestAnswerId = ''

            for answerItem in i2['answers']:

                if maxUpvoteCount < answerItem['up_vote_count']:
                    maxUpvoteCount = answerItem['up_vote_count']
                    questionId = answerItem['question_id']
                    askerId = i2['owner']['user_id'] if i2['owner']['user_type'] == 'registered' else i2['owner']['display_name']
                    bestAnswerId = answerItem['answer_id']
                    bestAnswererId = answerItem['owner']['user_id'] if answerItem['owner']['user_type'] == 'registered' else (answerItem['owner']['display_name'] + str(i2['question_id']))


                with open('./allPosts-metadata.tsv', 'a+') as output:
                    output.write('{}\t{}\t{}\t{}\n'.format(

                        answerItem['owner']['user_id'] if answerItem['owner']['user_type'] == 'registered' else (answerItem['owner']['display_name'] + str(i2['question_id'])),
                        answerItem['question_id'],
                        'answer',
                        answerItem['answer_id'],
                    ))

                is_accepted = 'no'
                if answerItem['is_accepted']:
                    is_accepted = 'yes'

                with open('./allPosts.tsv', 'a+') as output:
                    output.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                        # Who posted question
                        answerItem['owner']['user_id'] if answerItem['owner']['user_type'] == 'registered' else (answerItem['owner']['display_name'] + str(i2['question_id'])),
                        'answer',
                        answerItem['question_id'],
                        'na', # 'na' represents not applicable.
                        'na', # 'na' represents not applicable.
                        'na', # 'na' represents not applicable.
                        'na', # 'na' represents not applicable.
                        answerItem['answer_id'],
                        answerItem['creation_date'],
                        is_accepted,
                        'na', # 'na' represents not applicable.
                    ))
            # Pruning - If number of upvotes are greater than 4 then save the data
            if maxUpvoteCount > 4:

                with open('./ARN.tsv', 'a+') as output:
                    output.write('{}\t{}\n'.format(

                        i2['owner']['user_id'] if i2['owner']['user_type'] == 'registered' else
                        i2['owner']['display_name'],
                        answerItem['owner']['user_id'] if answerItem['owner']['user_type'] == 'registered' else
                        (answerItem['owner']['display_name'] + str(i2['question_id'])),
                        # answerItem['question_id'],
                ))

                with open('./ABAN.tsv', 'a+') as output:
                    output.write('{}\t{}\n'.format(
                        askerId,
                        bestAnswererId,
                        # questionId,
                        # bestAnswerId,
                        # maxUpvoteCount
                ))

                for answerItem in i2['answers']:
                    nonBestAnswererId = answerItem['owner']['user_id'] if answerItem['owner']['user_type'] == 'registered' else (answerItem['owner']['display_name'] + str(i2['question_id']))
                    if bestAnswererId != nonBestAnswererId :
                        with open('./CBEN.tsv', 'a+') as output:
                            output.write('{}\t{}\n'.format(
                                nonBestAnswererId,
                                bestAnswererId,
                                # questionId,
                                # bestAnswerId,
                                # maxUpvoteCount
                        ))
                        nonBestAnswerVoteCount = answerItem['up_vote_count']
                        edgeWeight = float(float(nonBestAnswerVoteCount)/float(maxUpvoteCount))
                        # print edgeWeight
                        with open('./VBEN.tsv', 'a+') as output:
                            output.write('{}\t{}\t{}\n'.format(
                                nonBestAnswererId,
                                bestAnswererId,
                                edgeWeight,
                                # questionId,
                                # bestAnswerId,
                                # maxUpvoteCount
                        ))

                    answererId = answerItem['owner']['user_id'] if answerItem['owner']['user_type'] == 'registered' else (answerItem['owner']['display_name'] + str(i2['question_id']))
                    questionVoteCount = i2['up_vote_count']
                    answerVoteCount = answerItem['up_vote_count']
                    upvoteDiffBtwQuestionAnswer = 0.0
                    upvoteDiffBtwQuestionAnswer = answerVoteCount - questionVoteCount

                    if upvoteDiffBtwQuestionAnswer > 0:
                        # print upvoteDiffBtwQuestionAnswer
                        with open('./VBEN2.tsv', 'a+') as output:
                            output.write('{}\t{}\t{}\n'.format(
                                askerId,
                                answererId,
                                upvoteDiffBtwQuestionAnswer,
                                # nonBestAnswererId,
                                # bestAnswererId,
                                # edgeWeight,
                                # questionId,
                                # bestAnswerId,
                                # maxUpvoteCount
                            ))


        # Question
        is_answered = 'no'
        if bool(i2['is_answered']):
            is_answered = 'yes'

        question_body = i2['title']
        question_body = i2['title'].encode('utf-8').replace('\t', ' ')
        question_body = question_body.replace('\n', '.')

        with open('./allPosts.tsv', 'a+') as output:
            output.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                # Who posted question
                i2['owner']['user_id'] if i2['owner']['user_type'] == 'registered' else (i2['owner']['display_name'] + str(i2['question_id'])),
                'question',
                i2['question_id'],
                i2['is_answered'],
                question_body,
                i2['answer_count'],
                i2['view_count'],
                '0', # '0' represents not applicable.
                '0', # '0' represents not applicable.
                'na', # 'na' represents not applicable.
                i2['creation_date'],
            ))

        with open('./allPosts-metadata.tsv', 'a+') as output:
            output.write('{}\t{}\t{}\t{}\n'.format(
                # Who posted question
                i2['owner']['user_id'] if i2['owner']['user_type'] == 'registered' else (i2['owner']['display_name'] + str(i2['question_id'])),
                i2['question_id'],
                'question',
                'na',  # 'na' represents not applicable.
            ))


file_content = read_csv('./allPosts-metadata.tsv')
print file_content



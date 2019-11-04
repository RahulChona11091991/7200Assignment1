import requests
from pandas import read_csv
import numpy as np

# write file header
with open('./allPosts.tsv', 'w+') as output:
    output.write('poster_user_id\tpost_type\tquestion_id\tis_answered\tquestion_title\tanswer_count\tview_count\tanswer_id\tanswer_creation_date\tis_accepted\tquestion_creation_date\n')
with open ('./askerAnswerer.tsv', 'w+') as output:
    #output.write('asker_uid\tanswerer_uid\tquestion_id\t\n')
    output.write('')
with open ('./allPosts-metadata.tsv', 'w+') as output:
    output.write('user_id\tquestion_id\tpost_type\tanswer_id\n')


# Fetch Questions and answers
for index in range(10):
    url = 'https://api.stackexchange.com//2.2/questions?page={}&pagesize=100&order=desc&sort=activity&tagged=python&site=stackoverflow&filter=!9Z(-wsa)x'.format(index+1)

    print('URL: {}'.format(url))
    requestObj = requests.get(url = url)
    data = requestObj.json()
    print data
    for i2 in data['items']:

        # check if answer exists, then execute
        if i2['answer_count'] > 0:
            for answerItem in i2['answers']:

                with open('./askerAnswerer.tsv', 'a+') as output:
                    output.write('{}\t{}\t{}\n'.format(

                        i2['owner']['user_id'] if i2['owner']['user_type'] == 'registered' else
                        i2['owner']['display_name'],
                        answerItem['owner']['user_id'] if answerItem['owner']['user_type'] == 'registered' else
                        (answerItem['owner']['display_name'] + str(i2['question_id'])),
                        answerItem['question_id'],
                    ))

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
                        'na', # 'na' represnts not applicable.
                        'na', # 'na' represnts not applicable.
                        'na', # 'na' represnts not applicable.
                        'na', # 'na' represnts not applicable.
                        answerItem['answer_id'],
                        answerItem['creation_date'],
                        is_accepted,
                        'na', # 'na' represnts not applicable.
                    ))

        # Question
        is_answered = 'no'
        if bool(i2['is_answered']):
            is_answered = 'yes'

        question_body = i2['title']
        question_body = str(i2['title']).replace('\t', ' ')
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
                '0', # '0' represnts not applicable.
                '0', # '0' represents not applicable.
                'na', # 'na' represents not applucable.
                i2['creation_date'],
            ))

        with open('./allPosts-metadata.tsv', 'a+') as output:
            output.write('{}\t{}\t{}\t{}\n'.format(
                # Who posted question
                i2['owner']['user_id'] if i2['owner']['user_type'] == 'registered' else (i2['owner']['display_name'] + str(i2['question_id'])),
                i2['question_id'],
                'question',
                'na',  # 'na' represents not applucable.
            ))


file_content = read_csv('./allPosts-metadata.tsv')
print file_content



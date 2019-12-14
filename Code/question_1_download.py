import requests
import time


# Store Stack Overflow URL
SO_URL = lambda page: 'https://api.stackexchange.com/2.2/questions?page={}&pagesize=100&order=desc&sort=activity&tagged=python;deep-learning&site=stackoverflow&todate=1575183600&filter=!BHrIhNpdLSrQDA*mgWaaqI0fLxig0y'.format(page)



# Clear files and write headers
with open('./data/allPosts.tsv', 'w+') as output:
    output.write('user_id\tpost_type\ttitle\tbody\tquestion_id\tis_answered\tquestion_score\t' \
        'answer_count\tquestion_comment_count\tquestion_down_vote_count\tquestion_up_vote_count\tview_count\t' \
        'link\tquestion_tags\tquestion_creation_date\tquestion_last_activity_date\tquestion_last_edit_date\tquestion_max_answer_upvote\tquestion_total_answer_upvote\t' \
        'answer_id\tis_accepted\tanswer_score\tanswer_comment_count\tanswer_down_vote_count\tanswer_up_vote_count\t' \
        'answer_tags\tanswer_creation_date\tanswer_last_activity_date\tanswer_last_edit_date\tanswer_max_upvote\n')

with open('./data/allPosts-metaData.tsv', 'w+') as output:
    output.write('user_id\tpost_type\tquestion_id\tanswer_id\n')

with open('./data/allUsers.tsv', 'w+') as output:
    output.write('user_id\tuser_type\tdisplay_name\treputation\tlink\tprofile_image\t' \
        'total_questions\ttotal_answers\ttotal_answered_questions\ttotal_accepted_answers\t' \
        'total_max_upvote\ttotal_answer_upvote\ttotal_question_upvote\ttotal_upvote_score\n')

def addUser(users, user, is_asker, is_answerer, is_answered, is_accepted, max_upvote, total_answer_upvote, total_question_upvote):

    i = user['user_id'] if (user['user_type'] == 'registered' or user['user_type'] == 'moderator') else user['display_name']

    if (user['user_type'] == 'registered' or user['user_type'] == 'moderator') and i not in users:
        users[i] = {
            'user_id': user['user_id'],
            'user_type': user['user_type'],
            'display_name': user['display_name'],
            'reputation': user['reputation'],
            'link': user['link'],
            'profile_image': user['profile_image'],
            'total_questions': 0,
            'total_answers': 0,
            'total_answered_questions': 0,
            'total_accepted_answers': 0,
            'total_max_upvote': 0,
            'total_answer_upvote': 0,
            'total_question_upvote': 0,
        }
    elif (user['user_type'] == 'unregistered' or user['user_type'] == 'does_not_exist') and i not in users:
        users[i] = {
            'user_id': user['display_name'],
            'user_type': user['user_type'],
            'display_name': user['display_name'],
            'reputation': '',
            'link': '',
            'profile_image': '',
            'total_questions': 0,
            'total_answers': 0,
            'total_answered_questions': 0,
            'total_accepted_answers': 0,
            'total_max_upvote': 0,
            'total_answer_upvote': 0,
            'total_question_upvote': 0,
        }

    if is_asker:
        users[i]['total_questions'] += 1
    if is_answerer:
        users[i]['total_answers'] += 1
    if is_answered:
        users[i]['total_answered_questions'] += 1
    if is_accepted:
        users[i]['total_accepted_answers'] += 1
    if max_upvote:
        users[i]['total_max_upvote'] += 1

    users[i]['total_answer_upvote'] += total_answer_upvote
    users[i]['total_question_upvote'] += total_question_upvote

    return users

def checkQuota(data):
    if 'quota_max' in data and 'quota_remaining' in data:
        print('Quota: {}/{}\n'.format(data['quota_remaining'], data['quota_max']))



users = {}

page = 1

# Fetch Questions and answers (all pages)
while True:

    # Get paginated URL
    url = SO_URL(page)
    print('Retrieving data from URL: {}'.format(url))

    # Retrieve data
    response = requests.get(url = url)


    # Success: 200 status
    if response.status_code >= 200 and response.status_code < 300:
        data = response.json()

        #print(data)
        checkQuota(data)

        # Loop over posts in response
        for post in data['items']:

            answer_count = post['answer_count']
            question_id = post['question_id']
            is_answered = 'yes' if post['is_answered'] else 'no'
            question_title = post['title'].replace('\t', '\\t').replace('\n', '\\n')
            question_body = post['body'].replace('\t', '\\t').replace('\r\n', '\\n').replace('\n', '\\n')
            asker_id = post['owner']['user_id'] if (post['owner']['user_type'] == 'registered' or post['owner']['user_type'] == 'moderator') else post['owner']['display_name']
            answer_count = post['answer_count']
            view_count = post['view_count']
            question_creation_date = time.ctime(post['creation_date'])
            question_last_activity_date = time.ctime(post['last_activity_date'])
            question_last_edit_date = time.ctime(post['last_edit_date']) if 'last_edit_date' in post else ''

            question_comment_count = post['comment_count']
            question_down_vote_count = post['down_vote_count']
            question_up_vote_count = post['up_vote_count']
            question_score = post['score']
            link = post['link']
            question_tags = ';'.join(post['tags'])

            users = addUser(users, post['owner'], True, False, post['is_answered'], False, False, 0, 0)

            question_max_answer_upvote = None
            question_total_answer_upvote = None

            # Loop over answers
            if answer_count > 0 and 'answers' in post:
                # Determine max upvote answer first
                max_answer_id = post['answers'][0]['answer_id']
                max_up_vote_count = post['answers'][0]['up_vote_count']
                max_user_id = post['answers'][0]['owner']['user_id'] if post['answers'][0]['owner']['user_type'] == 'registered' else post['answers'][0]['owner']['display_name']
                total_upvote_count = 0

                for answer in post['answers']:
                    answer_up_vote_count = answer['up_vote_count']
                    answerer_id = answer['owner']['user_id'] if (answer['owner']['user_type'] == 'registered' or answer['owner']['user_type'] == 'moderator') else answer['owner']['display_name']
                    total_upvote_count += answer_up_vote_count

                    if answer_up_vote_count > max_up_vote_count:
                        max_up_vote_count = answer_up_vote_count
                        max_answer_id = answer['answer_id']
                        max_user_id = answerer_id

                # Not found
                if max_up_vote_count == 0:
                    max_up_vote_count = None
                    max_user_id = None
                    max_answer_id = None

                question_max_answer_upvote = max_up_vote_count
                question_total_answer_upvote = total_upvote_count

                for answer in post['answers']:

                    answer_id = answer['answer_id']
                    up_vote_count = answer['up_vote_count']
                    answerer_id = answer['owner']['user_id'] if (answer['owner']['user_type'] == 'registered' or answer['owner']['user_type'] == 'moderator') else answer['owner']['display_name']
                    answer_creation_date = time.ctime(answer['creation_date'])
                    answer_last_activity_date = time.ctime(answer['last_activity_date'])
                    answer_last_edit_date = time.ctime(answer['last_edit_date']) if 'last_edit_date' in answer else ''
                    is_accepted = 'yes' if answer['is_accepted'] else 'no'
                    answer_title = answer['title'].replace('\t', '\\t').replace('\n', '\\n')
                    answer_body = answer['body'].replace('\t', '\\t').replace('\r\n', '\\n').replace('\n', '\\n')
                    answer_score = answer['score']
                    answer_comment_count = answer['comment_count']
                    answer_down_vote_count = answer['down_vote_count']
                    answer_up_vote_count = answer['up_vote_count']
                    answer_tags = ';'.join(answer['tags']) if 'tags' in answer else ''

                    is_max_upvote = answer_id == max_answer_id if max_answer_id is not None else False,

                    is_max_upvote_str = 'yes' if is_max_upvote[0] else 'no'

                    users = addUser(users, answer['owner'], False, True, False, answer['is_accepted'], is_max_upvote[0] if max_answer_id is not None else False, answer_up_vote_count, total_upvote_count)

                    ### WRITE TO allPosts.tsv & allPosts-metaData.tsv

                    # user_id
                    # question_id
                    # post_type
                    # answer_id
                    with open('./data/allPosts-metadata.tsv', 'a+') as output:
                        output.write('{}\t{}\t{}\t{}\n'.format(
                            answerer_id,
                            'answer',
                            question_id,
                            answer_id,
                        ))

                    # user_id
                    # post_type
                    # title
                    # body

                    # question_id
                    # is_answered
                    # question_score
                    # answer_count
                    # question_comment_count
                    # question_down_vote_count
                    # question_up_vote_count
                    # view_count
                    # link
                    # question_tags
                    # question_creation_date
                    # question_last_activity_date
                    # question_last_edit_date
                    # question_max_answer_upvote
                    # question_total_answer_upvote

                    # answer_id
                    # is_accepted
                    # answer_score
                    # answer_comment_count
                    # answer_down_vote_count
                    # answer_up_vote_count
                    # answer_tags
                    # answer_creation_date
                    # answer_last_activity_date
                    # answer_last_edit_date
                    # answer_max_upvote
                    with open('./data/allPosts.tsv', 'a+') as output:
                        output.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                            answerer_id,
                            'answer',
                            answer_title,
                            answer_body,

                            question_id,
                            '', # is_answered
                            '', # question_score
                            '', # answer_count
                            '', # question_comment_count
                            '', # question_down_vote_count
                            '', # question_up_vote_count
                            '', # view_count
                            '', # link
                            '', # question_tags
                            '', # question_creation_date
                            '', # question_last_activity_date
                            '', # question_last_edit_date
                            '', # question_max_answer_upvote
                            '', # question_total_answer_upvote

                            answer_id,
                            is_accepted,
                            answer_score,
                            answer_comment_count,
                            answer_down_vote_count,
                            answer_up_vote_count,
                            answer_tags,
                            answer_creation_date,
                            answer_last_activity_date,
                            answer_last_edit_date,
                            is_max_upvote_str,
                        ))


            ### WRITE TO allPosts.tsv & allPosts-metaData.tsv

            # user_id
            # post_type
            # title
            # body

            # question_id
            # is_answered
            # question_score
            # answer_count
            # question_comment_count
            # question_down_vote_count
            # question_up_vote_count
            # view_count
            # link
            # question_tags
            # question_creation_date
            # question_last_activity_date
            # question_last_edit_date
            # question_max_answer_upvote
            # question_total_answer_upvote

            # answer_id
            # is_accepted
            # answer_score
            # answer_comment_count
            # answer_down_vote_count
            # answer_up_vote_count
            # answer_tags
            # answer_creation_date
            # answer_last_activity_date
            # answer_last_edit_date
            # answer_max_upvote
            with open('./data/allPosts.tsv', 'a+') as output:
                output.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                    asker_id,
                    'question',
                    question_title,
                    question_body,

                    question_id,
                    is_answered,
                    question_score,
                    answer_count,
                    question_comment_count,
                    question_down_vote_count,
                    question_up_vote_count,
                    view_count,
                    link,
                    question_tags,
                    question_creation_date,
                    question_last_activity_date,
                    question_last_edit_date,
                    question_max_answer_upvote if question_max_answer_upvote is not None else '',
                    question_total_answer_upvote,

                    # Ignore 10 columns for answers
                ))

            # user_id
            # question_id
            # post_type
            # answer_id
            with open('./data/allPosts-metaData.tsv', 'a+') as output:
                output.write('{}\t{}\t{}\t{}\n'.format(
                    # Who posted question
                    asker_id,
                    'question',
                    question_id,
                    '',
                ))



        # Look for additional pages
        if not data['has_more']:
            break
        else:
            page += 1


# Save users
with open('./data/allUsers.tsv', 'a+') as output:
    for user_id in users:
        user = users[user_id]

        user_type = user['user_type']
        display_name = user['display_name']
        reputation = user['reputation']
        link = user['link']
        profile_image = user['profile_image']
        total_questions = user['total_questions']
        total_answers = user['total_answers']
        total_answered_questions = user['total_answered_questions']
        total_accepted_answers = user['total_accepted_answers']
        total_max_upvote = user['total_max_upvote']
        total_answer_upvote = user['total_answer_upvote']
        total_question_upvote = user['total_question_upvote']

        output.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            user_id,
            user_type,
            display_name,
            reputation,
            link,
            profile_image,
            total_questions,
            total_answers,
            total_answered_questions,
            total_accepted_answers,
            total_max_upvote,
            total_answer_upvote,
            total_question_upvote,
            total_answer_upvote/total_question_upvote if total_question_upvote > 0 else '',
        ))
        
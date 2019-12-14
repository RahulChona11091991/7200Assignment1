import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def loadFile(file):
  return pd.read_csv(file, sep='\t')

df1 = loadFile('./data/allPosts.tsv')
df1["question_creation_date"] = df1["question_creation_date"].astype("datetime64")
df1 = df1['question_creation_date'].to_frame()


fig, ax = plt.subplots(figsize=(24,8))

df1.groupby([df1["question_creation_date"].dt.year, df1["question_creation_date"].dt.month]).count().plot(kind="bar", ax=ax)
#df.plot.bar(x='question_creation_date', rot=0)

plt.legend().remove()
plt.grid()
fig.subplots_adjust(bottom=0.2)
plt.savefig('./Results/posts_creation_dates', dpi=300)




df2 = loadFile('./data/allPosts.tsv')

# question_max_answer_upvote = df2["question_max_answer_upvote"].values

# print('Num questions: {}'.format(np.sum( post_type=='question' )))
# print('Num answers: {}'.format(np.sum( post_type=='answer' )))

# Num questions: 6056
# Num answers: 5946

# question_max_answer_upvote = question_max_answer_upvote[ post_type=='question' ]

post_type = df2["post_type"].values
df2 = df2[ post_type=='question' ]


question_max_answer_upvote = df2["question_max_answer_upvote"].values
df2 = df2[ question_max_answer_upvote == question_max_answer_upvote ] # Remove NaN

df2 = df2['question_max_answer_upvote'].to_frame()

fig, ax = plt.subplots(figsize=(24,8))


df2.plot.bar()


ax = df2[['question_max_answer_upvote']].plot(kind='bar', title ="V comp", figsize=(24,8), legend=False, fontsize=12)



plt.legend().remove()
plt.grid()
fig.subplots_adjust(bottom=0.2)
plt.savefig('./Results/question_max_answer_upvote', dpi=300)


#plt.show()


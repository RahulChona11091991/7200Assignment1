import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def loadFile(file):
  return pd.read_csv(file, sep='\t', dtype={'from': str, 'to': str, 'weight': float})

def createGraph(df, weights=False):
  if weights:
    return nx.from_pandas_edgelist(df, 'from', 'to', ['weight'])
  else:
    return nx.from_pandas_edgelist(df, 'from', 'to')

def getPageRank(g, weights=False):
  if weights:
    rank = nx.pagerank(g, weight='weight')
  else:
    rank = nx.pagerank(g)
  return sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:10]

def getHits(g):
  (hubs,authorities) = nx.hits(g, max_iter=10000)
  return sorted(authorities.items(), key=lambda x: x[1], reverse=True)[0:10]


# 1-ARN.tsv
df_arn = loadFile('./data/1-ARN.tsv')
g_arn = createGraph(df_arn)
rank_arn = getPageRank(g_arn)
hits_arn = getHits(g_arn)

# 2-ABAN.tsv
df_aban = loadFile('./data/2-ABAN.tsv')
g_aban = createGraph(df_aban)
rank_aban = getPageRank(g_aban)
hits_aban = getHits(g_aban)

# 3-CBEN.tsv
df_cben = loadFile('./data/3-CBEN.tsv')
g_cben = createGraph(df_cben)
rank_cben = getPageRank(g_cben)
hits_cben = getHits(g_cben)

# 4-VBEN.tsv
df_vben = loadFile('./data/4-VBEN.tsv')
g_vben = createGraph(df_vben, weights=True)
rank_vben = getPageRank(g_vben, weights=True)
hits_vben = getHits(g_vben)

# 5-VBEN2.tsv
df_vben2 = loadFile('./data/5-VBEN2.tsv')
g_vben2 = createGraph(df_vben2, weights=True)
rank_vben2 = getPageRank(g_vben2, weights=True)
hits_vben2 = getHits(g_vben2)


# Combine/union ranks
ranks = {}

for (userId, rank) in np.concatenate((rank_arn, rank_aban, rank_cben, rank_vben, rank_vben2)):
  ranks[userId] = {
    'Rank1ARN': '',
    'Rank2ABAN': '',
    'Rank3CBEN': '',
    'Rank4VBEN': '',
    'Rank5VBEN2': '',
  }



# 1-ARN.tsv
for (userId, rank) in rank_arn:
  ranks[userId]['Rank1ARN'] = rank

# 2-ABAN.tsv
for (userId, rank) in rank_aban:
  ranks[userId]['Rank2ABAN'] = rank

# 3-CBEN.tsv
for (userId, rank) in rank_cben:
  ranks[userId]['Rank3CBEN'] = rank

# 4-VBEN.tsv
for (userId, rank) in rank_vben:
  ranks[userId]['Rank4VBEN'] = rank

# 5-VBEN2.tsv
for (userId, rank) in rank_vben2:
  ranks[userId]['Rank5VBEN2'] = rank

with open('./data/RANKS.tsv', 'w') as file:
  file.write('userId\tdisplayName\tProfileLink\tRank1ARN\tRank2ABAN\tRank3CBEN\tRank4VBEN\tRank5VBEN2\n')
  for userId in ranks:
    r = ranks[userId]
    file.write(f"{userId}\t{''}\t{''}\t{r['Rank1ARN']}\t{r['Rank2ABAN']}\t{r['Rank3CBEN']}\t{r['Rank4VBEN']}\t{r['Rank5VBEN2']}\n")


# Combine/union HITS
hits = {}

for (userId, rank) in np.concatenate((hits_arn, hits_aban, hits_cben, hits_vben, hits_vben2)):
  hits[userId] = {
    'Rank1ARN': '',
    'Rank2ABAN': '',
    'Rank3CBEN': '',
    'Rank4VBEN': '',
    'Rank5VBEN2': '',
  }

# 1-ARN.tsv
for (userId, rank) in hits_arn:
  hits[userId]['Rank1ARN'] = rank

# 2-ABAN.tsv
for (userId, rank) in hits_aban:
  hits[userId]['Rank2ABAN'] = rank

# 3-CBEN.tsv
for (userId, rank) in hits_cben:
  hits[userId]['Rank3CBEN'] = rank

# 4-VBEN.tsv
for (userId, rank) in hits_vben:
  hits[userId]['Rank4VBEN'] = rank

# 5-VBEN2.tsv
for (userId, rank) in hits_vben2:
  hits[userId]['Rank5VBEN2'] = rank

with open('./data/RANKS_HITS.tsv', 'w') as file:
  file.write('userId\tdisplayName\tProfileLink\tRank1ARN\tRank2ABAN\tRank3CBEN\tRank4VBEN\tRank5VBEN2\n')
  for userId in hits:
    r = hits[userId]
    file.write(f"{userId}\t{''}\t{''}\t{r['Rank1ARN']}\t{r['Rank2ABAN']}\t{r['Rank3CBEN']}\t{r['Rank4VBEN']}\t{r['Rank5VBEN2']}\n")


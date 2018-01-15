import numpy as np
import pandas as pd
import datetime
import json

DRY_RUN = True

day_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def time_marker(text=''):
    print('[{}] {}'.format(datetime.datetime.now().time(), text.title()))

def unpack(df, column, fillna=None):
    ret = None
    if fillna is None:
        ret = pd.concat([df, pd.DataFrame((d for idx, d in df[column].iteritems()))], axis=1)
        del ret[column]
    else:
        ret = pd.concat([df, pd.DataFrame((d for idx, d in df[column].iteritems())).fillna(fillna)], axis=1)
        del ret[column]
    return ret


#-------------------------------------------------------------------------------
time_marker(text='Loading User Data...')

data = pd.DataFrame()
source_data_file = '../source_data/users.json'

biz_list = []
for line in open(source_data_file, 'r'):
    user_list.append(json.loads(line))

time_marker(text='creating dataframe...')
users = pd.DataFrame(user_list)

time_marker(text='fixing datatype...')
users.yelping_since = pd.to_datetime(users.yelping_since)



#-------------------------------------------------------------------------------
time_marker(text='Split out friends...')
friends = users[['user_id', 'friends']].copy()
friends.columns = ['user_id', 'friends_list']


#-------------------------------------------------------------------------------
time_marker(text='Writing Friends dataframe to files...')
friends.reset_index(inplace=True, drop=True)
file_name = '../clean_data/users/user_friends_clean.csv'
if DRY_RUN:
    time_marker(text='DRY RUN - Not Writing {}'.format(file_name))
else:
    time_marker(text='Writing {}'.format(file_name))
    friends.to_csv(file_name, encoding='utf-8')




#-------------------------------------------------------------------------------
time_marker(text='Calculating friend count...')
users['friend_count'] = users['friends'].apply(lambda x: len(x))
users.drop(['friends'], axis=1, inplace=True)


#-------------------------------------------------------------------------------
time_marker(text='calculate yelper_age friend count...')
users['yelper_age'] = users.apply(lambda row: (users.yelping_since.max() - row.yelping_since).days,axis=1)


#-------------------------------------------------------------------------------
time_marker(text='One hot encoding elite status...')

# get number of years of elite status
tmp = pd.DataFrame(users.elite.values.tolist(), index= users.index)
num_elite_years = int(tmp.max().max()) - int(tmp.min().min()) + 1


from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()
users = users.join(pd.DataFrame(mlb.fit_transform(user_df.pop('elite')),
                                columns=mlb.classes_,
                                index=users.index))

#-------------------------------------------------------------------------------
time_marker(text='correcting elite status columns...')
elite_cols = list(users.columns[-num_elite_years:])
orig_columns = list(users.columns)[:-num_elite_years]
users.columns = orig_columns + ['elite_{}'.format(x) for x in elite_cols]



#-------------------------------------------------------------------------------
time_marker(text='Writing to files...')

for rating in biz_df.stars.unique():
    df = users[users.stars == rating].copy()
    df.reset_index(inplace=True, drop=True)

    file_name = '../clean_data/users/{}_star_business_clean.csv'.format(rating)

    if DRY_RUN:
        time_marker(text='DRY RUN - Not Writing {}'.format(file_name))
    else:
        time_marker(text='Writing {}'.format(file_name))
        df.to_csv(file_name, encoding='utf-8')


#-------------------------------------------------------------------------------
time_marker(text='Complete!')

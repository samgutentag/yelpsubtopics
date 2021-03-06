import numpy as np
import pandas as pd
import datetime
import json

DRY_RUN = False

def time_marker(text=''):
    print('[{}] {}'.format(datetime.datetime.now().time(), text.lower()))

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
source_data_file = '../source_data/user.json'

user_list = []
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
time_marker('append user_id prefix column')
friends['uid_prefix'] = friends.user_id.apply(lambda x: x[:1])


#-------------------------------------------------------------------------------
time_marker(text='Writing Friends dataframe to files...')
for i, prefix in enumerate(sorted(friends.uid_prefix.unique())):

    # take subset of busineses and trim business_id_refix column
    df = friends[friends.uid_prefix == prefix].iloc[:,:-1].copy()

    df.reset_index(inplace=True, drop=True)
    file_name = '../clean_data/friends/{}_{}_friends_clean.csv'.format(str(i).zfill(2), prefix)
    time_marker(text='Writing {:d} records to file {}'.format(df.shape[0], file_name))
    if DRY_RUN:
        pass
    else:
        df.to_csv(file_name, encoding='utf-8')
time_marker(text='Done!')


#-------------------------------------------------------------------------------
time_marker(text='Calculating friend count...')
users['friend_count'] = users['friends'].apply(lambda x: len(x))
users.drop(['friends'], axis=1, inplace=True)


#-------------------------------------------------------------------------------
time_marker(text='calculate yelper_age column...')
min_age = users.yelping_since.max()
if DRY_RUN:
    print('\tYoungest Yelper Birthday {}'.format(min_age))

users['yelper_age'] = users.apply(lambda row: (min_age - row.yelping_since).days,axis=1)
if DRY_RUN:
    print('\Oldest Yelper Age {}'.format(users.yelper_age.min()))


#-------------------------------------------------------------------------------
time_marker(text='One hot encoding elite status...')
# get number of years of elite status
tmp = pd.DataFrame(users.elite.values.tolist(), index= users.index)
num_elite_years = int(tmp.max().max()) - int(tmp.min().min()) + 1


from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()
users = users.join(pd.DataFrame(mlb.fit_transform(users.pop('elite')),
                                columns=mlb.classes_,
                                index=users.index))

#-------------------------------------------------------------------------------
time_marker(text='correcting elite status columns...')
elite_cols = list(users.columns[-num_elite_years:])
orig_columns = list(users.columns)[:-num_elite_years]
users.columns = orig_columns + ['elite_{}'.format(x) for x in elite_cols]


#-------------------------------------------------------------------------------
time_marker('append user_id prefix column')
users['uid_prefix'] = users.user_id.apply(lambda x: x[:1])


#-------------------------------------------------------------------------------
time_marker(text='Writing Friends dataframe to files...')
for i, prefix in enumerate(sorted(users.uid_prefix.unique())):

    # take subset of busineses and trim business_id_refix column
    df = users[users.uid_prefix == prefix].iloc[:,:-1].copy()

    df.reset_index(inplace=True, drop=True)
    file_name = '../clean_data/users/{}_{}_users_clean.csv'.format(str(i).zfill(2), prefix)
    time_marker(text='Writing {:d} records to file {}'.format(df.shape[0], file_name))
    if DRY_RUN:
        pass
    else:
        df.to_csv(file_name, encoding='utf-8')
time_marker(text='Done!')


#-------------------------------------------------------------------------------
time_marker(text='Complete!')

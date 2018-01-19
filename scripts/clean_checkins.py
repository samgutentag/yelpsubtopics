import pandas as pd
import datetime
import json
import numpy as np

DRY_RUN = False

day_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

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
time_marker(text='Loading Check Ins Data...')

data = pd.DataFrame()
source_data_file = '../source_data/checkin.json'

checkins_list = []
for line in open(source_data_file, 'r'):
    checkins_list.append(json.loads(line))

time_marker(text='creating dataframe...')
checkins_df = pd.DataFrame(checkins_list)


#-------------------------------------------------------------------------------
time_marker(text='collecting business IDs...')
business_ids = checkins_df.business_id.to_frame()


#-------------------------------------------------------------------------------
time_marker(text='unpacking daily check in counts...')
checkins_df = unpack(checkins_df, 'time')


#-------------------------------------------------------------------------------
if DRY_RUN:
    checkins_df = checkins_df[:20].copy()


#-------------------------------------------------------------------------------
time_marker(text='splitting daily counts into hourly columns...')
chunks = []

for day in checkins_df.columns[1:]:
    time_marker('unstacking {}...'.format(day))
    data = checkins_df[day].copy().to_frame()

    # fill missing daily checkin dicts with empty dict
    data=data.applymap(lambda x: {} if pd.isnull(x) else x)

    # unpack dict to hourly
    chunk = data[day].apply(pd.Series)

    chunk.columns = [int(str(x).split(':')[0]) for x in chunk.columns]

    # fill in missing hours
    for n in range(0, 24, 1):
        if n not in chunk.columns:
            chunk[n] = np.nan
    chunk['day'] = day

    chunks.append(chunk)

checkins_df = pd.concat(chunks)
checkins_df.fillna(0, inplace=True)


#-------------------------------------------------------------------------------
time_marker('appending numerical dayofweek to each row...')
checkins_df['dayofweek'] = checkins_df.apply(lambda row: day_labels.index(row.day.title()), axis=1)
checkins_df.drop('day', axis=1, inplace=True)


#-------------------------------------------------------------------------------
time_marker(text='appending business_id columns to hourly records...')
checkins_clean = checkins_df.merge(business_ids, left_index=True, right_index=True, how='left')


#-------------------------------------------------------------------------------
time_marker(text='cleaning up and reset index...')
time_marker(text='cleaning up and reset index...')
checkins_clean.fillna(0, inplace=True)

checkins_clean.sort_values(['business_id', 'dayofweek'], inplace=True)

checkins_clean.reset_index(inplace=True, drop=True)


#-------------------------------------------------------------------------------
time_marker('group by business_id....')
checkins_clean = checkins_clean.groupby(['business_id', 'dayofweek']).sum().unstack()

# relabel columns day_hour
time_marker('relabeling columns...')
corrected_columns = ['d{:d}_h{:d}'.format(day, hour)for hour in range(0, 24) for day in range(0, 7)]
checkins_clean.columns = corrected_columns

# sort columns
time_marker('sorting columns...')
sorted_columns = ['d{:d}_h{:d}'.format(day, hour) for day in range(0, 7) for hour in range(0, 24)]

# apply sort
checkins_clean = checkins_clean[sorted_columns]

# add sum column for sorting
time_marker('collecting total count of checkins for business...')
checkins_clean['total_checkins'] = checkins_clean.apply(lambda row: row.sum(), axis=1)

checkins_clean.sort_values(['total_checkins'], ascending=False, inplace=True)
checkins_clean.reset_index(inplace=True)


#-------------------------------------------------------------------------------
time_marker('appending bid_prefix column...')
checkins_clean['bid_prefix'] = checkins_clean.business_id.apply(lambda x: x[:1])


#-------------------------------------------------------------------------------
time_marker(text='Writing to files...')
file_count = len(checkins_clean.bid_prefix.unique())

for i, prefix in enumerate(sorted(checkins_clean.bid_prefix.unique())):
    df = checkins_clean[checkins_clean.bid_prefix == prefix].iloc[:,:-1].copy()
    df.reset_index(inplace=True, drop=True)
    file_name = '../clean_data/checkins/{}_{}_checkins_clean.csv'.format(str(i).zfill(2), prefix)
    time_marker(text='Writing {:d} records to file {}'.format(df.shape[0], file_name))
    if DRY_RUN:
        pass
    else:
        df.to_csv(file_name, encoding='utf-8')


#-------------------------------------------------------------------------------
time_marker(text='Complete!')

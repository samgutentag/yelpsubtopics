import numpy as np
import pandas as pd
import datetime
import json

DRY_RUN = False

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

#-------------------------------------------------------------------------------
time_marker(text='splitting daily counts into hourly columns...')
chunks = []

for day in checkins_df.columns[1:]:
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
time_marker(text='appending business_id columns to hourly records...')
checkins_clean = checkins_df.merge(business_ids, left_index=True, right_index=True, how='left')


#-------------------------------------------------------------------------------
time_marker(text='cleaning up and reset index...')
checkins_clean.fillna(0, inplace=True)
checkins_clean.reset_index(inplace=True, drop=True)


#-------------------------------------------------------------------------------
time_marker(text='Writing to files...')
day_count = len(checkins_clean.day.unique())
for i, day in enumerate(checkins_clean.day.unique()):
    df = checkins_clean[checkins_clean.day == day].copy()
    df.reset_index(inplace=True, drop=True)

    file_name = '../clean_data/checkins/{}_{}_checkins_clean.csv'.format(str(i).zfill(2), day.lower())
    time_marker(text='Writing {} records file...'.format(day))
    if DRY_RUN:
        pass
    else:
        df.to_csv(file_name, encoding='utf-8')


#-------------------------------------------------------------------------------
time_marker(text='Complete!')

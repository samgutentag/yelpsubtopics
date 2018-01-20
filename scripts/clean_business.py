import numpy as np
import pandas as pd
import datetime
import json

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
time_marker(text='Loading Business Info Data...')

data = pd.DataFrame()
source_data_file = '../source_data/business.json'

biz_list = []
for line in open(source_data_file, 'r'):
    biz_list.append(json.loads(line))

time_marker(text='creating dataframe...')
data = pd.DataFrame(biz_list)

time_marker(text='set index to business_id...')
data.set_index('business_id', inplace=True, drop=True)


#-------------------------------------------------------------------------------
if DRY_RUN:
    data = data[:200].copy()


#-------------------------------------------------------------------------------
time_marker(text='collecting business Hours...')
hours = data[['hours']].copy()

time_marker('splitting hours into individual columns...')
hours = pd.concat([hours.drop(['hours'], axis=1), hours['hours'].apply(pd.Series)], axis=1)

time_marker(text='Split hours into open and close...')
# split daily hours columns into '{DAY}_open' and '{DAY}_close'
for col in hours.columns:

    # split hours column of [11:00-19:00] into '{original_name}_open' and '{original_name}_close' columns
    hours['{}_open'.format(col.lower())]  = pd.to_datetime(hours[col].str.split('-', 1).str[0], format='%H:%M').dt.time
    hours['{}_close'.format(col.lower())] = pd.to_datetime(hours[col].str.split('-', 1).str[1], format='%H:%M').dt.time

    # drop original day columns
    hours.drop(col, axis=1, inplace=True)

time_marker('sorting day columns order...')
cols = [['{}_open'.format(x.lower()), '{}_close'.format(x.lower())] for x in day_labels]
ordered_cols = list()
for day in cols:
    for time in day:
        ordered_cols.append(time)

hours = hours[ordered_cols].copy()

# merge back to original data frame
time_marker(text='merge open and close hours to business data...')
data = data.merge(hours, left_index=True, right_index=True)

data.drop(['hours'], axis=1, inplace=True)


#-------------------------------------------------------------------------------
time_marker('collecting attributes columns...')
attributes_df = data['attributes'].apply(pd.Series)
attributes_df.columns = [str(x).lower() for x in attributes_df.columns]
time_marker('done')

time_marker('expanding attributes...')
expandable_cols = ['businessparking','goodformeal','ambience','hairspecializesin','music','bestnights','dietaryrestrictions']

for excol in [col for col in attributes_df.columns if col != 0]:
    time_marker('\texpanding "{}"...'.format(excol))
    df = attributes_df[excol].apply(pd.Series)
    df.columns = ['{}_{}'.format(excol, str(x).lower()) for x in df.columns]

    # append to attributes_df
    attributes_df = attributes_df.merge(df, left_index=True, right_index=True)

    # drop original column
    attributes_df.drop([excol], axis=1, inplace=True)

# if attribute column ends in '_0', trim it
time_marker('trimming odd columns...')
col_names = list()
for col in attributes_df.columns:
    if col.endswith('_0'):
        col_names.append(col[:-2])
    else:
        col_names.append(col)
# correct collumn names
attributes_df.columns = col_names

time_marker('dropping columns of all nan...')
attributes_df=attributes_df.dropna(axis=1,how='all')


#-------------------------------------------------------------------------------
time_marker('merging attributes to main business dataframe...')
data = data.merge(attributes_df, left_index=True, right_index=True)
data.drop(['attributes'], axis=1, inplace=True)
time_marker('done')
data.head(3)



#-------------------------------------------------------------------------------
time_marker(text='one hot encode categories...')
from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()

time_marker('one hot encoding of categories started...')
data = data.join(pd.DataFrame(mlb.fit_transform(data.pop('categories')),
                          columns=mlb.classes_,
                          index=data.index))
time_marker('complete!')


#-------------------------------------------------------------------------------
time_marker(text='cleaning up and reset index...')
data.columns = [str(x).lower().replace(' ', '_') for x in data.columns]
data.reset_index(inplace=True)


#-------------------------------------------------------------------------------
time_marker('append business_id prefix column')
data['bid_prefix'] = data.business_id.apply(lambda x: x[:1])


#-------------------------------------------------------------------------------
time_marker(text='Writing to file...')
for i, prefix in enumerate(sorted(data.bid_prefix.unique())):

    # take subset of busineses and trim business_id_refix column
    df = data[data.bid_prefix == prefix].iloc[:,:-1].copy()

    df.reset_index(inplace=True, drop=True)
    file_name = '../clean_data/business/{}_{}_business_clean.csv'.format(str(i).zfill(2), prefix)
    time_marker(text='Writing {:d} records to file {}'.format(df.shape[0], file_name))
    if DRY_RUN:
        print(df.head(5))
    else:
        df.to_csv(file_name, encoding='utf-8')
time_marker(text='Done!')


#-------------------------------------------------------------------------------
time_marker(text='Complete!')

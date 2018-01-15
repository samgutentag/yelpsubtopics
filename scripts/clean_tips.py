import pandas as pd
import datetime
import json


def time_marker(text=''):
    print('[{}] {}'.format(datetime.datetime.now().time(), text.title()))


#-------------------------------------------------------------------------------
time_marker(text='Loading Tips Data...')

data = pd.DataFrame()
source_data_file = '../source_data/tip.json'

tips_list = []
for line in open(source_data_file, 'r'):
    tips_list.append(json.loads(line))

#-------------------------------------------------------------------------------
time_marker(text='creating dataframe...')
tips_df = pd.DataFrame(tips_list)

#-------------------------------------------------------------------------------
time_marker(text='data type cleanup...')
tips_df.date        = pd.to_datetime(tips_df.date)
tips_df.likes       = tips_df.likes.astype('int')

#-------------------------------------------------------------------------------
time_marker(text='Calculating tip string length...')
tips_df['tip_len'] = tips_df.text.str.len()

#-------------------------------------------------------------------------------
print('')
max_col_length = 0
for col in tips_df.columns:
    if len(col) > max_col_length:
        max_col_length = len(col)

for col in tips_df.columns:
    print('\tNumber of Unique {} - {}'.format(col.ljust(max_col_length), str(len(tips_df[col].unique())).rjust(10)))
print('')
#-------------------------------------------------------------------------------
time_marker(text='Writing to file...')
tips_df.to_csv('../clean_data/tips_clean.csv')

#-------------------------------------------------------------------------------
time_marker(text='Complete!')

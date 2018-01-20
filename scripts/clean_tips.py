import pandas as pd
import datetime
import json

DRY_RUN = False

def time_marker(text=''):
    print('[{}] {}'.format(datetime.datetime.now().time(), text.lower()))


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
time_marker(text='sanitizing trip text...')
import string
translator = str.maketrans('','', string.punctuation)
tips_df['text'] = tips_df['text'].apply(lambda text: text.translate(translator).lower())


#-------------------------------------------------------------------------------
time_marker('append business_id prefix column')
tips_df['bid_prefix'] = tips_df.business_id.apply(lambda x: x[:1])


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
for i, prefix in enumerate(sorted(tips_df.bid_prefix.unique())):

    # take subset of busineses and trim business_id_refix column
    df = tips_df[tips_df.bid_prefix == prefix].iloc[:,:-1].copy()

    df.reset_index(inplace=True, drop=True)
    file_name = '../clean_data/tips/{}_{}_tips_clean.csv'.format(str(i).zfill(2), prefix)
    time_marker(text='Writing {:d} records to file {}'.format(df.shape[0], file_name))
    if DRY_RUN:
        pass
    else:
        df.to_csv(file_name, encoding='utf-8')
time_marker(text='Done!')

#-------------------------------------------------------------------------------
time_marker(text='Complete!')

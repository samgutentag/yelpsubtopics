

import pandas as pd
import datetime
from glob import glob

def time_marker(text=''):
    print('[{}] {}'.format(datetime.datetime.now().time(), text.title()))

time_marker('Loading Yelp Review Data from US Restaurants Only...')

try:
    file_path_slug = '../clean_data/_analysis/restaurant_reviews_united_states.csv'
    file_list = glob(file_path_slug)

    df_import = pd.DataFrame()
    chunks = []
    for c, file in enumerate(file_list):
        for chunk in pd.read_csv(file, chunksize=10000, iterator=True, index_col=0, parse_dates=['date']):
            chunks.append(chunk)
        if c % 10 == 0 or c == len(file_list):
            time_marker('\tFinished file! (%d of %d)' % (c+1, len(file_list)))
    df_import = pd.concat(chunks)
    df_import.reset_index(inplace=True, drop=True)

    time_marker('Data Loaded Successfully!')
except:
    time_marker('oops... something went wrong importing the data :(')


business_ids = sorted(df_import.business_id.unique())

destination_file = '../clean_data/_analysis/us_restaurant_bids.txt'
for bid in business_ids:
    with open(destination_file, 'a') as text_file:
        print('{}'.format(bid), file=text_file)
time_marker('Finished writing to file at {}'.format(destination_file))

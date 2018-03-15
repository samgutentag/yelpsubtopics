

import datetime
import pandas as pd
from glob import glob

import itertools
from collections import Counter

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from math import ceil

import seaborn as sns
sns.set()

SUP_TITLE_FONT_SIZE = 25
TITLE_FONT_SIZE = 25
LABEL_FONT_SIZE = 15
TICK_FONT_SIZE  = 15

FIG_SIZE = (15,10)

DO_WRITE_CHARTS = True



def csv_chunk_importer(file_path_slug='', column_labels=[], chunk_size=10000, drop_dups=False):
    """Load a collection of files in chunks

    Parameters
    ----------
    file_path_slug : string (required)
        file path to be searched, case use wildcards or single files

    column_labels : list (optional)
        a list of column names to replace the columns derived from the csv file
        will not rename columns if column counts do not match

    chunk_size : int (optional)
        the line size of each chunk being loaded
        defaults to 10000

    drop_dups : bool (optional)
        drop duplicate rows
        defaults to False


    Returns
    ----------
    df : pandas.DataFrame
        a data frame object of the loaded csv data

    """

    time_marker('Started Loading Data...')
    file_list = glob(file_path_slug)

    file_count = len(file_list)

    df = pd.DataFrame()

    # counter = 1
    chunks = []

    for ii, file in enumerate(file_list):

        for chunk in pd.read_csv(file, chunksize=10000, iterator=True):

            if len(column_labels) == len(chunk.columns):
                chunk.columns = column_labels

            chunks.append(chunk)

        if file_count < 50:
            time_marker('\tFinished file! ({:d} of {:d})'.format(ii+1, len(file_list)))
        elif file_count >= 50 and file_count < 1000:
            if ii % 100 == 0 or ii == 0 or ii == file_count:
                time_marker('\tFinished file! ({:d} of {:d})'.format(ii+1, len(file_list)))
        else:
            if ii % 1000 == 0 or ii == 0 or ii == file_count:
                time_marker('\tFinished file! ({:d} of {:d})'.format(ii+1, len(file_list)))

    time_marker('concatenating chunks...')
    df = pd.concat(chunks)

    if drop_dups:
        df.drop_duplicates(inplace=True)

    df.reset_index(inplace=True, drop=True)
    time_marker('Data Loaded Successfully!')

    return df

def time_marker(text=''):
    """Pretty print a time stamp with string

    Parameters
    ----------
    text : string (optional)
        string to be printed

    Returns
    ----------
    DOES NOT RETURN

    """
    print('[{}] {}'.format(datetime.datetime.now().time(), text.strip()))


#-----------------------------------------------------------------------------#
#                                                                             #
#               Plotting Tools!                                               #
#                                                                             #
#-----------------------------------------------------------------------------#

def get_business_information(df, business_id):
    ''' Get dict of business attributes from a given business_id '''
    business_information = df[df.business_id == business_id].transpose().to_dict()
    results = list(business_information.values())[0]

    # convert categories from string to list
    results['categories'] = results['categories'].split("'")[1::2]

    return results

def compare_to_chain(df, bid, biz_subtopics, min_reviews=10, min_biz=5, show=True):
    '''
        when passed a dataframe of reviews, collect ratings from all other businesses with the same name.
        Plot in red dots, the reviews in each Sub Topic for each location.
    '''

    business_information = get_business_information(biz_subtopics, bid)
    business_address = '{} {} AZ'.format(business_information['address'], business_information['city'])
    if df[df.business_id == bid].shape[0] < min_reviews:
        print('Skipping {} at {}, not enough reviews at this location {:d}'.format(business_information['name'], business_address,  df[df.business_id == bid].shape[0]))
        return False

    # all locations with the same name
    chain_reviews = df[df.name == business_information['name']].copy()
    chain_reviews = chain_reviews.groupby('business_id').mean()

    # only generate report if the number of other locations is greater than min_biz
    if chain_reviews.shape[0] < min_biz:
        print('Skipping {}, not enough other businesses {:d}'.format(business_information['name'], chain_reviews.shape[0]))
        return False

    # get count of reviews from each location
    review_countss = df[df.name == business_information['name']].groupby('business_id').count()['name'].to_frame()

    # select only businesses with more than min_reviews reviews
    location_review_counts = review_countss[review_countss.name > min_reviews].copy()

    # subset chain reviews to include only those with more than min_reviews reviews
    chain_reviews = chain_reviews[chain_reviews.index.isin(location_review_counts.index)].copy()


    # Plotting!
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_SIZE)


    ax1 = plt.subplot(1, 10, (1,9))

    # plot the specific bid with lines
    sample_location_ratings = chain_reviews[chain_reviews.index == bid].mean()[-9:].values

    for ii, val in enumerate(sample_location_ratings):
        ax1.axhline(val, xmin=ii/9+0.005, xmax=(ii+1)/9-0.005, color='r', linewidth=5)


    # melt data frame for seaborn boxplot
    chain_melt = chain_reviews[chain_reviews.index != bid].iloc[:,-9:].melt()


    # strip plot of subtopic reviews
    sns.stripplot(x='variable', y='value', data=chain_melt,
                  color='k', size=10, alpha=.2,
                  jitter=True, edgecolor='none', ax=ax1)


    # formatting title and axis
    plt.suptitle('{} at {}'.format(business_information['name'], business_address), size=SUP_TITLE_FONT_SIZE, weight='bold', y=0.95)
    ax1.set_title('Compared to all other {} Restaurants'.format(business_information['name']), size=LABEL_FONT_SIZE)

    ax1.set_ylabel('Rating', size=LABEL_FONT_SIZE)
    ax1.set_xlabel('Review Sub Topic', size=LABEL_FONT_SIZE)
    ax1.set_xticklabels([x.replace('_', ' ').title() for x in biz_subtopics.columns[-9:]], size=12)
    ax1.set_yticks([(x/2)+1 for x in range(0, 9)])


    # draw faint lines to deliniate Sub Ratings
    for y in range(1, 9):
        ax1.axvline(y-0.5, linestyle='-', alpha=1, color='w')


    # plot overall review scores
    ax2 = plt.subplot(1, 10, 10)
    ax2.axhline(business_information['stars'], color='r', linewidth=5)

    chain_stars = chain_reviews.groupby('business_id').mean()['stars'].to_frame().melt()
    sns.stripplot(x='variable', y='value', data=chain_stars,
                  color='k', size=10, alpha=.2,
                  jitter=True, edgecolor='none', ax=ax2)

    ax2.set_xlabel('')
    ax2.set_ylabel('')
    ax2.set_ylim(0.75,5.25)
    ax2.set_yticklabels([])
    ax2.set_xticklabels(['Yelp Stars'], size=12, weight='bold')

    file_path = '../charts/reports/{}_{}_chain_comparison.png'.format(business_information['chain_name'].replace('_',''), bid)
    if DO_WRITE_CHARTS:
        plt.savefig(file_path)
    if show:
        plt.show()
    plt.close()

    return file_path

def compare_to_zipcode(df, bid, biz_subtopics, min_reviews=10, min_biz=5, show=True):

    business_information = get_business_information(biz_subtopics, bid)


    business_address = '{} {} AZ'.format(business_information['address'], business_information['city'])
    if df[df.business_id == bid].shape[0] < min_reviews:
        print('Skipping {} at {}, not enough reviews at this location {:d}'.format(business_information['name'], business_address,  df[df.business_id == bid].shape[0]))
        return False

    # all locations with the same zipcode

    bids_in_zipcode = biz_subtopics[biz_subtopics.postal_code == business_information['postal_code']].business_id.unique()


    zipcode_reviews = df[df.business_id.isin(bids_in_zipcode)].copy()
    zipcode_reviews = zipcode_reviews.groupby('business_id').mean()

    # only generate report if the number of other locations is greater than min_biz
    if zipcode_reviews.shape[0] < min_biz:
        print('Skipping {}, not enough other businesses {:d}'.format(business_information['name'], zipcode_reviews.shape[0]))
        return False


    # get count of reviews from each location
    review_counts = df[df.business_id.isin(bids_in_zipcode)].groupby('business_id').count()['name'].to_frame()

    # select only businesses with more than min_reviews reviews
    review_counts = review_counts[review_counts.name > min_reviews].copy()

    # subset zipcode reviews to include only those with more than min_reviews reviews
    zipcode_reviews = zipcode_reviews[zipcode_reviews.index.isin(review_counts.index)].copy()


    # Plotting!
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_SIZE)


    ax1 = plt.subplot(1, 10, (1,9))

    # plot the specific bid with lines
    sample_location_ratings = zipcode_reviews[zipcode_reviews.index == bid].mean()[-9:].values

    for ii, val in enumerate(sample_location_ratings):
        ax1.axhline(val, xmin=ii/9+0.005, xmax=(ii+1)/9-0.005, color='r', linewidth=5)


    # melt data frame for seaborn boxplot
    zipcode_melt = zipcode_reviews[zipcode_reviews.index != bid].iloc[:,-9:].melt()


    # strip plot of subtopic reviews
    sns.stripplot(x='variable', y='value', data=zipcode_melt,
                  color='k', size=10, alpha=.2,
                  jitter=True, edgecolor='none', ax=ax1)


    # formatting title and axis
    plt.suptitle('{} at {}'.format(business_information['name'], business_address), size=SUP_TITLE_FONT_SIZE, weight='bold', y=0.95)
    ax1.set_title('Compared to all other Restaurants in Zip Code {}'.format(int(business_information['postal_code'])), size=LABEL_FONT_SIZE)

    ax1.set_ylabel('Rating', size=LABEL_FONT_SIZE)
    ax1.set_xlabel('Review Sub Topic', size=LABEL_FONT_SIZE)
    ax1.set_xticklabels([x.replace('_', ' ').title() for x in biz_subtopics.columns[-9:]], size=12)
    ax1.set_yticks([(x/2)+1 for x in range(0, 9)])


    # draw faint lines to deliniate Sub Ratings
    for y in range(1, 9):
        ax1.axvline(y-0.5, linestyle='-', alpha=1, color='w')


    # plot overall review scores
    ax2 = plt.subplot(1, 10, 10)
    ax2.axhline(business_information['stars'], color='r', linewidth=5)

    zipcode_stars = zipcode_reviews.groupby('business_id').mean()['stars'].to_frame().melt()
    sns.stripplot(x='variable', y='value', data=zipcode_stars,
                  color='k', size=10, alpha=.2,
                  jitter=True, edgecolor='none', ax=ax2)

    ax2.set_xlabel('')
    ax2.set_ylabel('')
    ax2.set_ylim(0.75,5.25)
    ax2.set_yticklabels([])
    ax2.set_xticklabels(['Yelp Stars'], size=12, weight='bold')

    file_path = '../charts/reports/{}_{}_zipcode_comparison.png'.format(business_information['chain_name'].replace('_',''), bid)
    if DO_WRITE_CHARTS:
        plt.savefig(file_path)

    if show:
        plt.show()
    plt.close()

    return file_path

def compare_to_cuisine(df, cuisine, bid, bid_df, biz_subtopics, min_reviews=10, min_biz=5, show=True, file_suffix=''):

    business_information = get_business_information(biz_subtopics, bid)

    business_address = '{} {} AZ'.format(business_information['address'], business_information['city'])
    if bid_df[bid_df.business_id == bid].shape[0] < min_reviews:
        print('Skipping {} at {}, not enough reviews at this location {:d}'.format(business_information['name'], business_address,  df[df.business_id == bid].shape[0]))
        return False

    # all restaurants with same cuisine
    cuisine_restaurant_bids = biz_subtopics[biz_subtopics['categories'].apply(lambda x: cuisine in x )].business_id.unique()

    # get all reviews for restaurants, groupby by business_id
    cuisine_reviews = df[df.business_id.isin(cuisine_restaurant_bids)].copy()
    cuisine_reviews = cuisine_reviews.groupby('business_id').mean()


    # only generate report if the number of other locations is greater than min_biz
    if cuisine_reviews.shape[0] < min_biz:
        print('Skipping {}, not enough other businesses {:d}'.format(business_information['name'], cuisine_reviews.shape[0]))
        return False


    # get count of reviews
    review_counts = df[df.business_id.isin(cuisine_restaurant_bids)].groupby('business_id').count()

    # select only businesses with more than min_reviews reviews
    review_counts = review_counts[review_counts.name > min_reviews].copy()

    # subset zipcode reviews to include only those with more than min_reviews reviews
    cuisine_reviews = cuisine_reviews[cuisine_reviews.index.isin(review_counts.index)].copy()


    # Plotting!
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_SIZE)


    ax1 = plt.subplot(1, 10, (1,9))

    # plot the specific bid with lines
    sample_location_ratings = bid_df[bid_df.business_id == bid].mean()[-9:].values

    for ii, val in enumerate(sample_location_ratings):
        ax1.axhline(val, xmin=ii/9+0.005, xmax=(ii+1)/9-0.005, color='r', linewidth=5)


    # melt data frame for seaborn boxplot
    df_melt = cuisine_reviews[cuisine_reviews.index != bid].iloc[:,-9:].melt()

    # strip plot of subtopic reviews
    sns.stripplot(x='variable', y='value', data=df_melt,
                  color='k', size=10, alpha=.2,
                  jitter=True, edgecolor='none', ax=ax1)

    # formatting title and axis
    plt.suptitle('{} at {}'.format(business_information['name'], business_address), size=SUP_TITLE_FONT_SIZE, weight='bold', y=0.95)
    ax1.set_title('Compared to all other Restaurants serving {} Cuisine'.format(cuisine.replace('_', ' ').title()), size=LABEL_FONT_SIZE)

    if file_suffix == 'nff':
        ax1.set_title('Compared to all other Non Fast Food Restaurants serving {} Cuisine'.format(cuisine.replace('_', ' ').title()), size=LABEL_FONT_SIZE)

    if file_suffix == 'ff':
        ax1.set_title('Compared to all other Fast Food Restaurants serving {} Cuisine'.format(cuisine.replace('_', ' ').title()), size=LABEL_FONT_SIZE)

    ax1.set_ylabel('Rating', size=LABEL_FONT_SIZE)
    ax1.set_xlabel('Review Sub Topic', size=LABEL_FONT_SIZE)
    ax1.set_xticklabels([x.replace('_', ' ').title() for x in biz_subtopics.columns[-9:]], size=12)
    ax1.set_yticks([(x/2)+1 for x in range(0, 9)])


    # draw faint lines to deliniate Sub Ratings
    for y in range(1, 9):
        ax1.axvline(y-0.5, linestyle='-', alpha=1, color='w')


    # plot overall review scores
    ax2 = plt.subplot(1, 10, 10)
    ax2.axhline(business_information['stars'], color='r', linewidth=5)

    stars = df.groupby('business_id').mean()['stars'].to_frame().melt()

    sns.stripplot(x='variable', y='value', data=stars,
                  color='k', size=10, alpha=.2,
                  jitter=True, edgecolor='none', ax=ax2)

    ax2.set_xlabel('')
    ax2.set_ylabel('')
    ax2.set_ylim(0.75,5.25)
    ax2.set_yticklabels([])
    ax2.set_xticklabels(['Yelp Stars'], size=12, weight='bold')

    file_path = '../charts/reports/{}_{}_cuisine_comparison_{}.png'.format(business_information['chain_name'].replace('_',''), bid, file_suffix).replace('_.png', '.png')
    if DO_WRITE_CHARTS:
        plt.savefig(file_path)

    if show:
        plt.show()
    plt.close()

    return file_path

def plot_suptopic_comparisons(df, palette='Reds_r', title_prefix='', show=True):

    nrows = 3
    ncols = 3
    size = 6

    subtopic_labels = list(df.columns[-9:])

    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*size, nrows*size))

    for rr, row in enumerate(ax):
        for cc, col in enumerate(row):
            subtopic_label = subtopic_labels[rr*ncols + cc]

            ax = plt.subplot(nrows, ncols, rr*ncols + cc+1)
            ax = sns.boxplot(x="stars", y=df[subtopic_label], data=df, palette=palette)


            ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c=".3")

            ax.set_xlabel('Restaurant Star Rating', size=LABEL_FONT_SIZE)
            ax.set_ylabel('{} Rating'.format(subtopic_label).replace('_', ' ').title(), weight='bold',  size=LABEL_FONT_SIZE)

            ax.set_yticks([x/4 for x in range(4, 21)])


    plt.suptitle('{} Subtopic Rating Review'.format(title_prefix.title().title()), size=25, weight='bold', y=0.90)

    if DO_WRITE_CHARTS:
        plt.savefig('../charts/reports/subtopic_review_{}.png'.format(title_prefix.replace(' ', '_').lower()))
    if show:
        plt.show()
    plt.close()

def yelp_star_rounding(stars):
    '''
        Yelp review stars are calculated by rounding the
        average review scroe up to the nearest 0.5 so here
        we use the same method for subtopic review stars.
    '''

    if stars > 0:
        result = ceil(stars*4)/4
    else:
        result = np.nan

    return result



# EOF

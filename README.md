# Extracting Sub Topic Ratings from Yelp Review Text
This project leverages Latent Dirichlet Allocation (LDA) from the `gensim` library  to extract topics from the 496,000 Yelp Reviews given to 7066 Restaurants in the State of Arizona.

# Results
The best Sub Topic Groupings were generated using an Online Latent Dirichlet Allocation model provided by `genesis`.  This Model was trained to identify 50 Topics, with 10 Terms per topic, and given 50 Passes to process the review texts.

Text was tokenized and lemmatized, so that we retained complete English readable words (vs stemming).  The corpus was restricted to only tokens appearing more frequently than the 10,000th most frequently token.  Example	 if the 10,000th token appeared just 3 times, only tokens occurring 4 or more times were kept.

This processing took nearly 13 hours to complete on a 2010 MacBook Pro, so please take that into consideration when attempting to recreate these results.

## Identified Sub Topics
The following 50 topics were identified by the LDA model.  Topics Highlighted were selected as Most important and used to define Sub Topic Review Categories.

 0 ['dessert', 'wine', 'ice', 'cream', 'cake', 'entree', 'meal', 'chocolate', 'course', 'appetizer']
::1 ['time', 'back', 'first', 'try', 'place', 'went', 'definitely', 'go', 'next', 'great']::
2 ['u', 'table', 'came', 'server', 'food', 'drink', 'waitress', 'asked', 'ordered', 'minute']
::3 ['dish', 'flavor', 'sauce', 'like', 'taste', 'menu', 'one', 'would', 'bit', 'meat']::
4 ['pizza', 'crust', 'slice', 'topping', 'cheese', 'pie', 'thin', 'good', 'sauce', 'pepperoni']
5 ['crab', 'leg', 'shell', 'pound', 'coworker', 'saving', 'panini', 'hub', 'e', 'angry']
6 ['chicken', 'rice', 'chinese', 'fried', 'food', 'beef', 'soup', 'egg', 'orange', 'sour']
::7 ['wait', 'minute', 'time', 'food', 'get', 'order', 'long', 'line', 'hour', 'waiting']::
::8 ['great', 'nice', 'patio', 'atmosphere', 'outside', 'place', 'cool', 'fun', 'inside', 'food']::
::9 ['order', 'ordered', 'called', 'delivery', 'extra', 'got', 'time', 'get', 'card', 'call']::
10 ['tempe', 'school', 'opening', 'mill', 'w', 'college', 'b', 'asu', 'high', 'grand']
11 ['fresh', 'ingredient', 'olive', 'tomato', 'salad', 'oil', 'made', 'bianco', 'mozzarella', 'basil']
12 ['best', 'year', 'place', 'restaurant', 'phoenix', 'one', 'ever', 'food', 'valley', 'family']
::13 ['table', 'dirty', 'clean', 'bathroom', 'floor', 'plate', 'hand', 'cup', 'paper', 'chair']::
14 ['chicken', 'fried', 'waffle', 'deep', 'breast', 'piece', 'cajun', 'tender', 'catfish', 'crispy']
15 ['mouth', 'smell', 'taste', 'word', 'world', 'heaven', 'bud', 'holy', 'win', 'watering']
16 ['always', 'love', 'place', 'get', 'time', 'food', 'go', 'favorite', 'great', 'never']
17 ['food', 'experience', 'service', 'great', 'server', 'u', 'staff', 'friendly', 'restaurant', 'made']
18 ['sushi', 'roll', 'tuna', 'fresh', 'chef', 'salmon', 'japanese', 'spicy', 'tempura', 'fish']
::19 ['option', 'menu', 'free', 'gyro', 'meat', 'vegetarian', 'veggie', 'choose', 'vegan', 'choice']::
::20 ['food', 'like', 'place', 'ordered', 'tasted', 'bad', 'even', 'back', 'cold', 'taste']::
::21 ['good', 'food', 'place', 'price', 'pretty', 'service', 'better', 'like', 'would', 'really']::
22 ['burger', 'fry', 'onion', 'bun', 'shake', 'ring', 'cheese', 'french', 'bacon', 'patty']
23 ['bowl', 'pho', 'soup', 'noodle', 'roll', 'spring', 'broth', 'vietnamese', 'beef', 'rice']
24 ['star', 'review', 'give', 'yelp', 'five', 'reason', 'rating', 'giving', 'based', 'shot']
25 ['location', 'drive', 'employee', 'thru', 'window', 'car', 'fast', 'chipotle', 'dont', 'im']
26 ['restaurant', 'parking', 'menu', 'lunch', 'small', 'lot', 'area', 'find', 'little', 'place']
::27 ['great', 'food', 'service', 'place', 'friendly', 'good', 'recommend', 'staff', 'delicious', 'price']::
28 ['wing', 'pasta', 'sauce', 'italian', 'garlic', 'bread', 'meatball', 'spaghetti', 'dish', 'ranch']
29 ['steak', 'cooked', 'potato', 'perfectly', 'well', 'medium', 'rare', 'filet', 'mashed', 'perfection']
30 ['bar', 'room', 'dining', 'bartender', 'area', 'sit', 'drink', 'airport', 'sat', 'table']
31 ['breakfast', 'egg', 'coffee', 'pancake', 'bacon', 'morning', 'toast', 'brunch', 'biscuit', 'gravy']
32 ['fish', 'shrimp', 'ramen', 'chip', 'fried', 'sea', 'ceviche', 'ahi', 'sauce', 'mahi']
33 ['hot', 'dog', 'chicago', 'beef', 'chili', 'piping', 'italian', 'slider', 'wendy', 'pepper']
34 ['place', 'like', 'get', 'know', 'go', 'one', 'say', 'want', 'make', 'really']
::35 ['good', 'really', 'got', 'ordered', 'little', 'nice', 'pretty', 'came', 'portion', 'also']::
36 ['sandwich', 'bread', 'sub', 'cheese', 'turkey', 'meat', 'subway', 'shop', 'lunch', 'philly']
37 ['seafood', 'lobster', 'shrimp', 'pot', 'calamari', 'chop', 'sum', 'duck', 'dim', 'clam']
38 ['taco', 'mexican', 'salsa', 'burrito', 'chip', 'bean', 'tortilla', 'food', 'carne', 'asada']
39 ['bbq', 'pork', 'rib', 'meat', 'brisket', 'sauce', 'pulled', 'side', 'good', 'corn']
40 ['salad', 'chicken', 'pita', 'dressing', 'greek', 'hummus', 'lettuce', 'wrap', 'fresh', 'lunch']
41 ['kid', 'music', 'loud', 'wall', 'game', 'child', 'hole', 'playing', 'play', 'family']
42 ['cheese', 'sweet', 'delicious', 'sauce', 'perfect', 'mac', 'onion', 'green', 'potato', 'pepper']
43 ['happy', 'hour', 'beer', 'drink', 'selection', 'great', 'menu', 'special', 'price', 'deal']
::44 ['customer', 'manager', 'service', 'back', 'food', 'said', 'time', 'asked', 'one', 'would']::
45 ['buffet', 'indian', 'food', 'lamb', 'chicken', 'dish', 'naan', 'rice', 'masala', 'restaurant']
46 ['son', 'sister', 'mother', 'brother', 'http', 'father', 'c', 'buck', 'law', 'wallet']
47 ['night', 'dinner', 'last', 'party', 'friday', 'went', 'reservation', 'birthday', 'group', 'saturday']
48 ['thai', 'tea', 'spicy', 'curry', 'pad', 'tofu', 'iced', 'dish', 'spice', 'rice']
49 ['grill', 'cookie', 'hawaiian', 'cooky', 'mini', 'macaroni', 'island', 'paradise', 'scoop', 'nugget']



![Subtopic Ratings](charts/subtopic_review_all_restaurants.png)



# Reproduce my Work
Few simple steps to get started and reproduce my work.

## Getting Started
Clone this repo to get started.  From there, if you are using `conda` to manage your virtual environment, run the following command to setup the environment and install the needed packages.  Be sure to pass the included `environment.yml` file.

```
# conda env create environment.yml
```

## Prerequisites
There are a few steps involved in getting `nltk` and `spacy`  up and running.

Run the following commands from the command line to install the NLTK and spaCy package resources needed.  For more documentation on spaCy, follow [this link](https://spacy.io/usage/)

```
# python -m nltk.downloader all
# python -m spacy download en
```

Lastly, the data used for this project is supplied by the [Yelp Open Dataset](https://www.yelp.com/dataset).  You will need to download a copy of the source data and store it in a directory called `source_data` to run these notebooks without making changes to any code.

Specifically, you will need to copy over `business.json` and `review.json` from the downloaded data set to the `source_data` directory.

The starter directory structure should look like this:

```
yelpsubtopics
| -README.md
| -environment.yml
| -.gitignore
| -models
| -clean_data
| -source_data
|   |- business.json
|   |- review.json
| -documents
| -DataWrangling
|   |- 00_Business_Data_Wrangling.ipynb
|   |- 01_Review_Wrangling.ipynb
| -TopicModelling
|   |- model_03a_all_reviews_nouns.ipynb
|   |- model_05_all_reviews.ipynb
|   |- model_02_nff_reviews.ipynb
|   |- MODEL_SUMMARY.ipynb
|   |- model_01_ff_reviews.ipynb
|   |- model_04_all_reviews_nouns_verbs.ipynb
| -SubTopicReviews
|   |- SubTopicTagging_Model5.ipynb
|   |- SubTopic_Investigation.ipynb
|   |- plottingtools
|       |- init__.py
| -scripts
|   |- clean_checkins.py
|   |- clean_users.py
| -charts
|   |- reports
```

## Order of Operations
To successfully reproduce my results, run the notebooks in the following order:

1. DataWrangling/00_Business_Data_Wrangling.ipynb
2. DataWrangling/01_Review_Wrangling.ipynb
3. TopicModelling/model_05_all_reviews.ipynb
4. SubTopicReviews/SubTopicTagging_Model5.ipynb
5. SubTopicReviews/SubTopic_Investigation.ipynb

There are several additional notebooks in the `TopicModelling` directory that can be run and include additional output lda models.  The final results of this project use the model generated by the `model_05_all_reviews.ipynb` notebook.

# Additional Information
## Built With
* [pandas](https://pandas.pydata.org) - Python Data Analysis Library
* [matplotlib](https://matplotlib.org) - Python Plotting Library
* [seaborn](https://seaborn.pydata.org) - statistical data visualization
* [nltk](http://www.nltk.org/) - a suite of libraries and programs for symbolic and statistical natural language processing for English text
* [gensim](https://rometools.github.io/rome/) - Topic Modeling for humans
* [spaCy](https://spacy.io) - Industrial-Strength Natural Language Processing

## Authors
* **Sam Gutentag** - *Initial work* - [samgutentag](www.samgutentag.com)

See other projects by Sam on [Github](https://github.com/samgutentag)

## Acknowledgments
* The [Yelp Open Data Set](https://www.yelp.com/dataset)
* [Simon Worgan](https://www.linkedin.com/in/simon-worgan-44613138/)
* [Springboard](www.springboard.com)

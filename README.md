# Extracting Sub Topic Ratings from Yelp Review Text
This project leverages Latent Dirichlet Allocation (LDA) from the `gensim` library  to extract topics from the 496,000 Yelp Reviews given to 7066 Restaurants in the State of Arizona.

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

## Results



Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

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

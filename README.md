# Sandvik Data Science Take Home

This is my solution to Sandvik's data science take home assignment, which involves
building a model to classify the gender of a speakers voice, given a set of recordings of
sentences in English. You can read all of the details of the assignment here;

https://github.com/sandvikcode/data-science-take-home

In this readme I'll describe how I approached the problem. I had relatively little free time to spend on
the assignment, whilst also completing assignments for other interview processes, so I decided to use this
assignment to demonstrate my ability to tackle a problem end to end, rather than my ability to meticulously explore
all possibly feature sets or models and hyperparameter optimisations. As such, I just followed my intuition of what would work well for this problem.

I should also point out that my experience with time series is relatively limited, and I took a more or less
"pure data science" approach to the problem, using half remembered signal processing knowledge, but following
the smell of the data rather than anything particularly sophisticated time series techniques.

The rough workflow of how to use the files in this repo is the following;

* *get_data.py* - Downloads all of the raw (compressed) data via the internet
* *extract_data.py* - Decompresses all of the raw data files
* *extract_metadata.py* - Runs through all of the data directories, and assembles some metadata about them
* *extract_features.py* - Contains the method that processes a wav file into a feature vector, and code for running this on all the raw data
* *model_training.ipynb* - Make some plots and train the model.

## Feature Engineering

Intuitively, the main characterising features of the gender of a voice are it's volume and frequency, so
I decided to try and filter the time series into something that kept this information, but was obviously
of much lower dimensionality than the hundreds of thousands of samples in the time series.

I'm not a huge fan of just taking random summary statistics and throwing them into a feature vector, and
I wasn't convinced that that approach would be the best one to carry forward. I instead decided to keep 
a slightly richer data structure around for each recording; the Power Spectral Density (PSD).

The PSD gives a representation of how much 'power per frequency' there is in the time series, and thus
makes sense from an intuition sense. Plus if we smooth it enough, it can be fairly low dimensional.

I ended up smoothing it down to representing the power in frequencies in the human vocal range using around 40 numbers,
which is small enough to use with more or less any ML algorithm.

Plotting these features for a handful of samples shows that our intuition is broadly correct, that females tend to have less power in
lower frequencies. It was surprising to me that (by eye), males seem to have frequencies fairly evenly represented across the human
vocal range.

![Power Spectral Density]('/psd.png')

## Data Cleaning 

Before training the models, we had to clean up the labels a little bit. There was a bunch of different ways
that gender was actually represented in the data (different languages, upper case/lower case, punctuation etc). Fortunately
there was little enough variety that i could clean these by hand, and throw away any samples that don't have a clear gender.

## Results

I tried a few different out of the box models from the `sklearn` Python library, but ultimately settled on
the gradient boosted decision trees classifier as the most performant. I evaluated the models by randomly splitting
the sample into a training and testing set of samples, and then simply 
inpsected their `classification_report` on the performance of the model on the testing set 

The `classification_report` is is a collection of single number metrics one can use to 
evaluate models, including precision, recall and f1-score. Boosted decision trees were visibly more performant
than any of the other methods, just by eyeballing the numbers.

The classification performance, following taking all of the intuitive choices in building the features and the model, is the
following. With more time, I would certainly explore other ML models, and do hyperparameter searches on the decision tree.


              precision    recall  f1-score   support

        Male       0.99      0.99      0.99     16004
      Female       0.92      0.94      0.93      2939

    accuracy                           0.98     18943
   macro avg       0.95      0.96      0.96     18943
weighted avg       0.98      0.98      0.98     18943
from collections import defaultdict
import nltk
from nltk.stem import PorterStemmer
from django.core.management.base import BaseCommand

try:
    from progressbar import ProgressBar, Bar, Percentage
except ImportError:
    ProgressBar = None

from twap.twitter.models import Tweet

class Command(BaseCommand):
    '''Train an NLTK classifier based on the NLTK chat corpus, and
apply it to the tweets in the database.  Reports on the current
classifier accuracy, and then outputs total numbers by type.
    
NOTE: requires NLTK; install progressbar to view percent complete'''
    help = __doc__
    
    v_normal = 1
    
    def handle(self, verbosity=1, **options):
        total = Tweet.objects.count()
        if verbosity >= self.v_normal:
            print 'Analyzing %d tweets' % total

        if verbosity >= self.v_normal:
            print 'Training the classifier...'
        classifier = train_classifier()


        if ProgressBar:
            pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=total).start()
        else:
            pbar = None

        # iterate through all the tweets and analyze the text
        i = 0
        dialog_acts = defaultdict(int)
        for t in Tweet.objects.all():
            #print t.text
            speech_type = classifier.classify(dialogue_act_features(t.text))
            #print speech_type
            dialog_acts[speech_type] += 1

            i += 1
            if pbar:
                pbar.update(i)
                
        pbar.finish()

        print '\nTotals by type:'
        for type, count in dialog_acts.iteritems():
            print '%s:  %d' % (type.rjust(10), count)


def average(values):
    return sum(values, 0.0) / len(values)


# based on nltk book, chapter 6
# http://nltk.googlecode.com/svn/trunk/doc/book/ch06.html

def dialogue_act_features(post):
    words = nltk.word_tokenize(post)
    sentences = nltk.sent_tokenize(post)
    features = {
        'word_diversity': len(words)/len(set(words)),
    }

    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem_word(w) for w in words]
        
    # words
    for word in set(stemmed_words):
         features['contains(%s)' % word.lower()] = True

    # check for presence/absence of specific words
    check_words = [
        'who', 'what', 'where', 'why', 'how',    # question words
        'love', 'hate', 'despis',		 # emotional words (?)
        ] 

    for word in check_words:
        features['contains(%s)' % word] = word in stemmed_words
         
    # punctuation
    for punctuation in ['?', '!', '!!', '?!', '"', '...', '.']:
        features['punctuation_count(%s)' % punctuation] = post.count(punctuation)

    # skip parts of speech for now - slow, not helping much
    return features

    # get counts for parts of speech
    pos_count = defaultdict(int)
    for sentence in sentences:
        # tokenize the sentence into words and tag parts of speech
        sentence_words = nltk.word_tokenize(sentence)
        # - using the nltk parts-of-speech tagger for now
        #  (other options may be faster/more accurate)
        pos_sentence = nltk.pos_tag(sentence_words)
        for word, pos in pos_sentence:
            pos_count['pos_%s' % pos] += 1

    # include final counts by part of speech in the features
    features.update(pos_count)

    return features

def train_classifier():
    # train a classifier, check its accuracy, and return it
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]
    featuresets = [(dialogue_act_features(post.text), post.get('class'))
                   for post in posts]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print 'Classifier accuracy: %10s%%' % nltk.classify.accuracy(classifier, test_set)
    # uncomment when working on improving the classifier
    #classifier.show_most_informative_features(15)
    return classifier

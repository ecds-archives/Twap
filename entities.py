from collections import defaultdict
import nltk
from operator import itemgetter


# super-simple named-entity extraction based on nltk default
# parts-of-speech tagger and named-entity chunker

named_entity_summary = {
    'LOCATION': defaultdict(int),
    'PERSON': defaultdict(int),
    'ORGANIZATION': defaultdict(int)
}


def extract_named_entities(text, named_entities=None):
    # expects raw text passed in,
    # optional dictionary to aggregate counts (i.e., return value from previous call)
    
    if named_entities is None:
        named_entities = named_entity_summary.copy()

    # tokenize the entire text into sentences
    for sentence in nltk.sent_tokenize(text):
        # tokenize the sentence into words and tag parts of speech
        sentence_words = nltk.word_tokenize(sentence)
        # - using the nltk parts-of-speech tagger for now
        #  (other options may be faster/more accurate)
        pos_sentence = nltk.pos_tag(sentence_words)        

        # use the nltk named-entity extractor
        tagged_tokens = nltk.ne_chunk(pos_sentence)
        # also availabe: batch_ne_chunk (tags tagged sentences)
        for tok in tagged_tokens.subtrees():
            # capture & tally any named entities
            if tok.node in named_entities.keys():
                val = ' '.join([val for val, type in tok.leaves()])
                named_entities[tok.node][val] += 1

        return named_entities


def show_named_entities(named_entities, threshold=1):
    # output any entities found & the count for each
    for ne_type in named_entities.keys():
        # skip any categories where no entities were found
        if not named_entities[ne_type]:
            continue
        
        print '\n%s:' % ne_type
        for name, count in sorted(named_entities[ne_type].iteritems(),
                                  key=itemgetter(1), reverse=True):
            if count >= threshold:
                print '%d\t%s' % (count, name)


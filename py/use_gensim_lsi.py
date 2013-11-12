import nltk
import sys
import gensim
from nltk.corpus import wordnet
from gensim import corpora, models, similarities

stopwords = nltk.corpus.stopwords.words('english')
doc_fh = open('../data/reverb_out.txt','r')

documents = []
for line in doc_fh:
    confidence = float(line.split('\t')[11])
    if confidence < 0.5:
        continue
    sent = line.split('\t')
    documents.append(sent[12])

texts = [[word for word in document.lower().split() if ((word not in stopwords) & (wordnet.synsets(word) != []))] for document in documents]

#all_tokens = ''.join(texts)
all_tokens = sum(texts, [])

tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once] for text in texts]
dictionary = corpora.Dictionary(texts)
#dictionary.save('../data/corpus_2/merged_dictionary.dict')
corpus = [dictionary.doc2bow(text) for text in texts]

#corpora.MmCorpus.serialize('../data/corpus_2/merged_corpus.mm', corpus)

#id2word = gensim.corpora.Dictionary.load_from_text('../data/corpus_2/merged_dictionary.dict')
id2word = dictionary
#print dictionary
#mm = gensim.corpora.MmCorpus('../data/corpus_2/merged_corpus.mm')
mm = corpus
#print mm
lsi = gensim.models.lsimodel.LsiModel(corpus=mm, id2word=id2word, num_topics=20)
#print str(lsi)
lsi_topic_words = lsi.show_topics(15, 5)
for word in lsi_topic_words:
    print str(word)

lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=20, update_every=1, chunksize=10000, passes=1)
lda_topic_words = lda.show_topics(15, 5)

for word in lda_topic_words:
    print str(word)

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
doc_ctr = 0
for doc in corpus_tfidf:
    print doc
    if doc_ctr > 20:
        break
    doc_ctr = doc_ctr + 1

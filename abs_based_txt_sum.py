'''
STEPS
----------
1.Data Collection

2.Data clean-up like removing special characters, numeric values, stop words, etc.

3.Tokenization - Creation of tokens (Word tokens and Sentence tokens)

4.Calculate the word frequency for each word

5.Calculate the weighted frequency for each sentence

6.Creation of summary choosing 30% of top weighted sentence

'''

import re
import nltk

article_text = '''Computer science, the study of computers and computing, including their theoretical and algorithmic foundations, hardware and software, and their uses for processing information. The discipline of computer science includes the study of algorithms and data structures, computer and network design, modeling data and information processes, and artificial intelligence. Computer science draws some of its foundations from mathematics and engineering and therefore incorporates techniques from areas such as queueing theory, probability and statistics, and electronic circuit design. Computer science also makes heavy use of hypothesis testing and experimentation during the conceptualization, design, measurement, and refinement of new algorithms, information structures, and computer architectures.

Computer science is considered as part of a family of five separate yet interrelated disciplines: computer engineering, computer science, information systems, information technology, and software engineering. This family has come to be known collectively as the discipline of computing. These five disciplines are interrelated in the sense that computing is their object of study, but they are separate since each has its own research perspective and curricular focus. (Since 1991 the Association for Computing Machinery [ACM], the IEEE Computer Society [IEEE-CS], and the Association for Information Systems [AIS] have collaborated to develop and update the taxonomy of these five interrelated disciplines and the guidelines that educational institutions worldwide use for their undergraduate, graduate, and research programs.)

The major subfields of computer science include the traditional study of computer architecture, programming languages, and software development. However, they also include computational science (the use of algorithmic techniques for modeling scientific data), graphics and visualization, human-computer interaction, databases and information systems, networks, and the social and professional issues that are unique to the practice of computer science. As may be evident, some of these subfields overlap in their activities with other modern fields, such as bioinformatics and computational chemistry. These overlaps are the consequence of a tendency among computer scientists to recognize and act upon their field’s many interdisciplinary connections.'''

article_text = article_text.lower()

#clean the text
clean_text = re.sub('[^a-zA-Z]',' ',article_text)
clean_text = re.sub('\s+',' ',clean_text)
#print(clean_text)

#Run this for once to download stopwords
#import nltk
#nltk.download('stopwords')
#nltk.download('punkt')

#split into sentence list
sentence_list = nltk.sent_tokenize(article_text)
#print(sentence_list)

stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(clean_text):
    if word not in stopwords:
        if word not in word_frequencies:
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequency = max(word_frequencies.values())

#normalizing the frequencies
for word in word_frequencies:
    word_frequencies[word] = round(word_frequencies[word] / maximum_frequency,3)

sentence_scores = {}

for sentence in sentence_list:
    for word in nltk.word_tokenize(sentence):
        if word in word_frequencies and len(sentence.split(' ')) < 30 :
            if sentence not in sentence_scores :
                sentence_scores[sentence] = word_frequencies[word]
            else:
                sentence_scores[sentence] += word_frequencies[word]


#print(word_frequencies)
#print(sentence_scores)

#get top 5 sentences
import heapq
summary = heapq.nlargest(5,sentence_scores, key=sentence_scores.get)

summary_text = " ".join(summary)

print('Article text lenght: ',len(article_text))
print('Summary text length: ',len(summary_text))
print(summary_text)

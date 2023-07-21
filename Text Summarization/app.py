from flask import Flask , render_template ,request
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text="""In Harry’s world fate works not only through powers and objects such as prophecies, the Sorting Hat, wands, and the Goblet of Fire, but also through people. 
Repeatedly, other characters decide Harry’s future for him, depriving him of freedom and choice. For example, before his eleventh birthday, the Dursleys control
Harry’s life, keeping from him knowledge of his past and understanding of his identity (Sorcerer’s 49). In Harry Potter and the Chamber of Secrets, Dobby 
repeatedly assumes control over events by intercepting Ron’s and Hermione’s letters during the summer; by sealing the barrier to Platform 93⁄4,causing Harry 
to miss the Hogwarts Express; and by sending a Bludger after Harry in a Quidditch match, breaking his wrist. Yet again, in Harry Potter and the Prisoner of 
Azkaban, many adults intercede while attempting to protect Harry from perceived danger, as Snape observes:“Everyone from the Minister of Magic downward has 
been trying to keep famous Harry Potter safe from Sirius Black” (284). All these characters, as enactors of fate, unknowingly drive Harry toward his destiny by
attempting to control or to direct his life, while themselves controlled and directed by fate."""
def summarizer(rawdocs):
    stopwords=list( STOP_WORDS)
    # print(stopwords)

    nlp= spacy.load('en_core_web_sm')
    # smallest module of spacy
    doc= nlp(rawdocs)
    # printing the inputted text
    # print(doc)

    tokens=[token.text for token in doc]
    # same as stop words
    # print(tokens)
    word_freq ={} # word frequency
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1
    #print(word_freq)

    max_freq=max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    #print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores ={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys(): 
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]

    select_length = int(len(sent_tokens)*0.2)

    summary = nlargest(select_length, sent_scores ,key = sent_scores.get) 
    # print(summary)
    final_summ = [word.text for word in summary]
    summary = ' '.join(final_summ)
    # print(summary)
    # print("Length of the Original text ",len(text.split(' ')))
    # print("Length of the Summarized text ",len(summary.split(' ')))

    return summary , doc , len(rawdocs.split(' ')),len(summary.split(' '))


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze',methods=['GET','POST'])
def analyze():
       if request.method=='POST':
            rawtext = request.form['rawtext']
            summary , original_txt ,len_orig_txt,len_summary = summarizer(rawtext)

       return render_template('summary.html' , summary=summary , original_txt=original_txt , len_orig_txt=len_orig_txt , len_summary=len_summary)

if __name__=="__main__":
    app.run(debug=True)

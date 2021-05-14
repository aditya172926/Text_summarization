import spacy
import pickle
import random
import sys
import fitz

def NamedEntityReco(docu):
    test = spacy.load('en_core_web_sm')
    # sent = "Apple is looking at buying U.K. startup for $1 billion"

    # ts = test(sent)
    # for ent in ts.ents:
    #     print(ent.text, ent.label_)

    fname = docu
    doc = fitz.open(fname)
    cv = ""
    for page in doc:
        cv = cv + str(page.getText())
    # print(cv)

    ts = test(" ".join(cv.split('\n')))
    # for ent in ts.ents:
    #     print(ent.text, ent.label_)

    # there are multiple errors in identifing the NERs. So we train the model

    # train_data = pickle.load(open('train_data.pkl', 'rb'))
    # print(len(train_data))

    # print(train_data[0])

    # nlp = spacy.blank('en')

    # Creating a function to train the model
    def train_model(train_data):
        if 'ner' not in nlp.pipe_names: # Checking if NER is present in pipeline
            ner = nlp.create_pipe('ner') # creating NER pipe if not present
            nlp.add_pipe(ner, last=True) # adding NER pipe in the end

        for _, annotations in train_data: # Getting 1 resume at a time from our training data of 200 resumes
            for ent in annotations['entities']: # Getting each tuple at a time from 'entities' key in dictionary at index[1] i.e.,(0, 15, 'Name') and so on
                ner.add_label(ent[2]) # here we are adding only labels of each tuple from entities key dict, eg:- 'Name' label of (0, 15, 'Name')
            
        # In above for loop we finally added all custom NER from training data.

        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner'] # getting all other pipes except NER.
        with nlp.disable_pipes(*other_pipes): # Disabling other pipe's as we want to train only NER.
            optimizer = nlp.begin_training()

            for itn in range(10): # trainig model for 10 iteraion
                print('Starting iteration ' + str(itn))
                random.shuffle(train_data) # shuffling data in every iteration 
                losses = {}
                for text, annotations in train_data:
                    try:
                        nlp.update(
                            [text],
                            [annotations],
                            drop=0.2,
                            sgd=optimizer,
                            losses=losses
                        )
                        print(losses)
                    except Exception as e:
                        print('Pass')
                        pass

    # train_model(train_data)

    # Saving our trained model to re-use.
    # nlp.to_disk('nlp_model')
    nlp_model = spacy.load('Text_Summarization/nlp_model')
    # Checking all the custom NER created
    print(nlp_model)

    doc = nlp_model(" ".join(cv.split('\n')))
    ner_text = ''
    for ent in doc.ents:
        print('a')
        print(f'{ent.label_.upper():{20}} - {ent.text}')
        ner_text += str(ent.label_.upper()) + ': -' + str(ent.text) + '\n'
    with open('ner.txt', 'w') as n:
        n.write(ner_text.strip())
    print("NERs stored in ner.txt file")
    return ner_text

# NamedEntityReco()
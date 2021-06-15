# Text_summarization
## Extractive Methodology summary generation
Clone the project and then move into the project directory.
Check out the requirements.txt file in the updateddev branch and use pip3 install -r requirements.txt or pip install -r requirements.txt to install.

Download the GloVe (Global Vectors For Word Representation) unsupervised learning algorithm for getting the vector representation of words, using this link
https://nlp.stanford.edu/projects/glove/

Place the GloVe text file downloaded in an embeddings folder in the Text_summarization directory, just make sure the paths are correct.
Use python app.py or python3 app.py to run the project.

Note:
You can use the inbuilt NER pipeline provided by spacy for Named Entity Recognition, or train your own. This project trains its own NER specifically for getting entities from Resumes. The training dataset is train_data.plk form, provided in the Text_Summarization folder.

Expected outcome using GloVe is 20% of the text size of the original input.
Other methods of NLP and Spacy in addition to GloVe are used to create a meaningful summary, for additional comparison. 
Directly articles can fetched using web scraping, just provide the link of the webpage when prompted.

A detailed report and presentation is provided in ML Mini Project report.pdf and Mini Project Presentation Review presentation respectively.

# ML for Good Hackathon (Team 18)

### Team Members are:
- Dilip Vishwakarma
- Jayant Rane

### This project consists of 2 parts:
- Using NLP to extract and analyse Text Data (incomplete. Now it only gets terms which are crucial for getting info from data)
- Using ML Algo to find categorize the worriness of candidate surveyed and it's relation to other factor.

## How we created this project:
### Library used:
- spacy and it's plugins for NLP
- sklearn and it's supporting library for ML

## Text Analysis
To find out the meaningful terms from the given text, we followed this steps:
- We took ```large english corpus``` of spacy.
- Then we got a list of sentences and from this, we got part of speech and other attributes.
- Then we took terms like
```
    "parent",
    "child",
    "family",

    "school",
    "classes",
    "tuition",
    "friends",
    "office",
    "office work",
    "online",
    "offline",
    "online class",

    "teenage",
    "senior",
    "junior",
    "young",
    "old",

    "health",
    "environment",
    "vaccination",
    "hospital",
    "mortal",

    "social media",
    "communication",
    "meeting",
    "home",

    "clean",
    "wash",

    "problem",
    "issue",
    "income",
    "money",
    "entertainment",
    # "time",
    "government",
    "security",
    "safety",

    "pandemic",
    "disease",
    "healthcare",

    "death",
    "retire",
    "layoff",

    "spend",
    "economic",
    "political",
    "social",

    "spread",
    "virus",
    "symptoms",
    "cause",
    "ill",

    "science",
    "location",

    "employment",
    "recruitment",
    "employ",
    "recruit",
    "job",
    "internship",

    "apartment",
    "physical",
    "mental",
    "psychological",

    "teacher",
```
- and found synonyms of above texts and added in spacy matcher to match all lexical word matching.
- From this, we can get all terms categoried in English.
- Then we found sentiment of the sentence and it's subjectivity. 
- Taking all this, we can find if the given statement from ```crisislogger```
  - given statement is about what.
  - from all statement, i.e. the aggregate of all results, we can find out what overall people are feeling or their views.

### How to Execute:
- nlp project is in directory ```nlp_demo```.
- add requirements using ```pip install -r requirments.txt``` 
- run ```spacy_trial.py```.
- in the last, you will see the terms, it's counts, it's sentiment.

## Chat Data Analysis (Incomplete implementation)
- we can also analyse chat data using web panel, created using streamlit python library.
- In this, we just need to upload chat data and it will allow us to go through and look at the each chat with it's analyzed terms as we did above.

### How to Execute
- just run ```streamlit run nlp_demo/streamlit_trial.py```
- and then open ```http://localhost:8501/```
- then upload ```FocusGroups``` data (chat data)
- then read the chat using button and check the result below.

Here we were going to show the terms and it's analysis by entity like parent1/2/3/4/5.  (This is still incomplete).


## Categorization of Data (```ProlificAcademic```)
Description and analysis is given in ```Adult Mental Health.pynb``` jupyter Notebook file.

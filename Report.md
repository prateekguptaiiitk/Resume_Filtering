
# Summer Internship Report - 2019

```
                              Resume Filtering Using Machine Learning
```

```
1. Project Introduction
2. Overview
3. Data Collection
4. Training Word2Vec model
5. Extracting Sections
6. Assigning Scores
7. Suggestions for Subsequent Work
8. Conclusion
9. Resources
```

---

## Project Introduction

```
This project searches the entire resume database to select and display the resumes which fit the best for the provided 
job description(JD).
```
This is, in its current form, achieved by assigning a score to each CV by intelligently comparing them against the corresponding Job Description.  This reduces the window to a fraction of an original size of applicants. Resumes in the final window can be manually checked for further analysis.

---

## Overview

- Mainly three datasets were required.
- The Word2Vec Model using the StackOverflow data dump.
- Extracted sections from the CVs like Education, Experience etc.
- Finally, the CVs were awarded scores against each Job Descriptions available.

---

## Data Collection

Mainly three datasets were required:

#### **StackExchange Network Posts**

- This dataset was required to trains the word2vec model. Fortunately, StackExchange network dumps it's data in xml format under Creative Commons License. One can find a download link for the dataset(44 GB) [on Internet Archive.](https://archive.org/details/stackexchange)

- This is an anonymized dump of all user-contributed content on the Stack Exchange network. Each site is formatted as a separate archive consisting of XML files zipped via 7-zip using bzip2 compression. The following sites were included:

![alt text](https://github.com/prateekguptaiiitk/Resume_Classifier/blob/develop/stackexchange%20tree.png)

- All the zip files were extracted using [extract.py](https://github.com/prateekguptaiiitk/Resume_Classifier/blob/develop/Section%20Extraction/extract.py).
- This colection of sites is referenced as ```stackechange/``` folder from hereafter.
- Each site archive includes Posts, Users, Votes, Comments, PostHistory and PostLinks (all in .xml files). The ```README.md``` file of the dataset is given below:

### **Resume Dataset**

- This dataset was required to test the trained word2vec model. Among these resumes, best matching resumes should be filtered out.

### ***Job Description Dataset**

- This dataset was required to test the trained word2vec model. These job descriptions would be the basis of resume filtering.

### README.md
---
- Format: 7zipped
- Files:
  - **badges**.xml
      - UserId, e.g.: "420"
      - Name, e.g.: "Teacher"
      - Date, e.g.: "2008-09-15T08:55:03.923"
  - **comments**.xml
      - Id
      - PostId
      - Score
      - Text, e.g.: "@Stu Thompson: Seems possible to me - why not try it?"
      - CreationDate, e.g.:"2008-09-06T08:07:10.730"
      - UserId
  - **posts**.xml
      - Id
      - PostTypeId
         - 1: Question
         - 2: Answer
      - ParentID (only present if PostTypeId is 2)
      - AcceptedAnswerId (only present if PostTypeId is 1)
      - CreationDate
      - Score
      - ViewCount
      - Body
      - OwnerUserId
      - LastEditorUserId
      - LastEditorDisplayName="Jeff Atwood"
      - LastEditDate="2009-03-05T22:28:34.823"
      - LastActivityDate="2009-03-11T12:51:01.480"
      - CommunityOwnedDate="2009-03-11T12:51:01.480"
      - ClosedDate="2009-03-11T12:51:01.480"
      - Title=
      - Tags=
      - AnswerCount
      - CommentCount
      - FavoriteCount
  - **posthistory**.xml
    - Id
    - PostHistoryTypeId
     - 1: Initial Title - The first title a question is asked with.
     - 2: Initial Body - The first raw body text a post is submitted with.
     - 3: Initial Tags - The first tags a question is asked with.
     - 4: Edit Title - A question's title has been changed.
     - 5: Edit Body - A post's body has been changed, the raw text is stored here as markdown.
     - 6: Edit Tags - A question's tags have been changed.
     - 7: Rollback Title - A question's title has reverted to a previous version.
     - 8: Rollback Body - A post's body has reverted to a previous version - the raw text is stored here.
     - 9: Rollback Tags - A question's tags have reverted to a previous version.
     - 10: Post Closed - A post was voted to be closed.
     - 11: Post Reopened - A post was voted to be reopened.
     - 12: Post Deleted - A post was voted to be removed.
     - 13: Post Undeleted - A post was voted to be restored.
     - 14: Post Locked - A post was locked by a moderator.
     - 15: Post Unlocked - A post was unlocked by a moderator.
     - 16: Community Owned - A post has become community owned.
     - 17: Post Migrated - A post was migrated.
     - 18: Question Merged - A question has had another, deleted question merged into itself.
     - 19: Question Protected - A question was protected by a moderator
     - 20: Question Unprotected - A question was unprotected by a moderator
     - 21: Post Disassociated - An admin removes the OwnerUserId from a post.
     - 22: Question Unmerged - A previously merged question has had its answers and votes restored.
   - PostId
   - RevisionGUID: At times more than one type of history record can be recorded by a single action.  All of these will be grouped using the same RevisionGUID
   - CreationDate: "2009-03-05T22:28:34.823"
   - UserId
   - UserDisplayName: populated if a user has been removed and no longer referenced by user Id
   - Comment: This field will contain the comment made by the user who edited a post
   - Text: A raw version of the new value for a given revision
     - If PostHistoryTypeId = 10, 11, 12, 13, 14, or 15  this column will contain a JSON encoded string with all users who have voted for the PostHistoryTypeId
     - If PostHistoryTypeId = 17 this column will contain migration details of either "from <url>" or "to <url>"
   - CloseReasonId
     - 1: Exact Duplicate - This question covers exactly the same ground as earlier questions on this topic; its answers may be merged with another identical question.
     - 2: off-topic
     - 3: subjective
     - 4: not a real question
     - 7: too localized
  - **postlinks**.xml
    - Id
    - CreationDate
    - PostId
    - RelatedPostId
    - PostLinkTypeId
      - 1: Linked
      - 3: Duplicate
  - **users**.xml
    - Id
    - Reputation
    - CreationDate
    - DisplayName
    - EmailHash
    - LastAccessDate
    - WebsiteUrl
    - Location
    - Age
    - AboutMe
    - Views
    - UpVotes
    - DownVotes
  - **votes**.xml
    - Id
    - PostId
    - VoteTypeId
       - ` 1`: AcceptedByOriginator
       - ` 2`: UpMod
       - ` 3`: DownMod
       - ` 4`: Offensive
       - ` 5`: Favorite - if VoteTypeId = 5 UserId will be populated
       - ` 6`: Close
       - ` 7`: Reopen
       - ` 8`: BountyStart
       - ` 9`: BountyClose
       - `10`: Deletion
       - `11`: Undeletion
       - `12`: Spam
       - `13`: InformModerator
    - CreationDate
    - UserId (only for VoteTypeId 5)
    - BountyAmount (only for VoteTypeId 9)
---


#### **Job Descriptions**

- A [Kaggle dataset](https://www.kaggle.com/c/job-salary-prediction/data) containing Job Descriptions for several job openings was used.
- Used NLP to filter out the Job Descriptions related to IT industry.
- Finally, 5000+ JDs including JDs for positions like 'Web devloper', 'C++ software developer', 'Software developer', 'Enbedded Software Engineer' were filtered out and saved as ***jd.csv***.

#### **Resumes**

- No open source dataset for Resumes was found.
- Resumes were needed in text format. Since extracting proper text from PDF files is a complex problem on it's own.
- [Indeed.com](http://www.indeed.com) was the only site which displayed the resumes openly.
- So, a Python Script(collectCV.py) was used to collect around 300 resumes of applicants for positions like 'Software Developer' , 'Data Scientist', 'Web Developer' etc.

---

# Training Word2Vec Model

Word2Vec models are shallow, two-layer neural networks that are trained to reconstruct linguistic contexts of words. Word2vec takes as its input a large corpus of text and produces a vector space, typically of several hundred dimensions, with each unique word in the corpus being assigned a corresponding vector in the space. Word vectors are positioned in the vector space such that words that share common contexts in the corpus are located in close proximity to one another in the space

## Requirement of training our own models
- There are pre-trained models available both in ```gensim``` and ```spaCy``` packages in Python. These models are trained over Google News Data. This implies that they are not suitable for the technically aware context distinction required for this project. For e.g. HTML and Ruby may have higher similarity value in these models than the model we trained.

- Therefore,a dataset was required which was both technically aware and also has sufficient amount of unique words present for the non-technical functioning of the model.
 ```  
 The dataset used to train Word2Vec model becomes more crucial considering the fact
 that Word2Vec models can be retrained over and over, however,
 new Vocabulary cannot be added to the model.
 ```

- Therefore, ```stackexchange/``` network data was used.
- Used the ```gensim``` implementation (in Python) of Word2Vec to train our model.

## Cleaning and Extracting data

- From the ```stackexchange/``` dataset the ```Posts.xml``` for each site was used to extract each Post irrespective of whether it's a Question or an Answer. These Posts were extracted as HTML para tags and saved as ```paras.txt``` in the corresponding subfolder of the site.

- At this stage, each subdirectory of ```StackExchange/``` which corresponds to the site under StackExchange network, has a new file called ```paras.txt```.

- For training the Word2Vec model, we required a sequence of sentences to be streamed from the disk. Each sentence is represented as a list i.e. each element of this list is the word of the sentence.

- So, the ```paras.txt``` files were used to extract sentences using BeautifulSoup(a Python Library), and saved into ```sentences.txt``` (for each site), such that the final result is free of formatting and mathematics, code etc.

- These sentences were streamed into the Word2Vec train method for training the model.

## Generated Word2Vec Word Embeddings

- Each word is represented as a ```300-sized``` numpy array (vector).

- Collected **1237328 unique words** from a **corpus of 565919447 raw words** and **32701720 sentences.**

-  Running time for the training was around 3hrs.

---
# Extracting sections

- Had some collection of words that are usually the heading in the resumes. For example 'education', 'academic', 'school', 'study', etc will mark the start of the education section

- Iterated over all lines of all resumes, one by one.

- For each line, first, removed all the blank lines or the lines containing just symbols. Some resumes have a line denoted to just asterisks or dashes.

- Next, categorized each line into one of the four sections. This is done by calculating its similarity to the existing words. If the similarity is higher than the threshold, we update the section and mark that point, on the other hand, if the similarity if below the threshold, we continue with the previous section.

- This enables to separate the sections with good enough accuracy.

- Finally, wrote each section of a resume in a .csv file after removing the stop words and doing lemmatization.

---
# Assigning scores

- For a given Job Description, removed all the stop words and do lemmatization, to get a selected few keywords.

- For each keyword found, found `5` similar words and their corresponding similarity.

- Now, found `tf-idf` for each word, that was got in step 2.

- The score of the CV is the sum of `tf-idf * similarity` for all words that were generated in step 2.

---
# Suggestions for Subsequent Work

This section describes some suggestions for the next iteration of the development:

## Identifying Sections in Resumes
- After the first iteration, we have enough resumes to create a training dataset. That is, from the resumes, we can extract sentences and assign them labels according to the section they are in. For eg. 'MS from Cambridge' will be labeled as 'Education'.
- This is possible because most of the resumes have similar structure since they share the source.
- This training set can be used to train a sentence classification algorithm (SVM is recommended).
- This algorithm can be used to classify sentences of resumes into different sections.

## Word Embeddings
- Word2Vec has two popular implementations:
  - The C Google implementation
  - The Python Gensim implementation
  The vectors can not be retrained in C implementation. The vectors in Python implementation can be retrained but the Vocabulary can't be added to the model.

- So, the gensim implementation of Doc2Vec should be used instead. It is similar but more flexible. The model can be retrained and Vocabulary can be added to the model as well. Further, vectors for Phrases can be generated more easily since the averaging algorithm is inbuilt.

- Better Tokenization while training model. For eg. Identification of common phrases and generating a single token for it instead of individual words. Like 'New York' is better tokenized as 'new_york' than 'new' and 'york'.  This can be achieved by using gensim implementation of Phrases or spaCy.

## Scoring Algorithm

- The division of section can be improved by using the currently sorted sections, that is, we can use them for classifying the lines.

- Instead of considering each word individually, we can take phrases together. Like 'software developer' should be treated as a single entity instead of two.

- We give a higher value to words 'python', 'java', etc. over words like 'knowledge', 'experience' etc in keywords of the job description. This can be done by extracting the tags from the `stackoverflow/` data.

- The Algorithm can use any meta-data (if available) about any preferences for the candidates.
---

# Conclusion

 However, there is definitely room for improvements, the result is satisfactory enough for the first iteration of the project. Further, most of the pivotal improvements have been mentioned in the previous section. We have learned a lot during the project and hopefully, the project will serve it's purpose in SkyBits as well. The filtering up of CVs has always been subjective process, although, the use of Machine Learning can certainly reduce the unnecessary amount of human effort.

---

# Resources

- spaCy Documentation: https://spacy.io/
- spaCy GitHub Issue Page: https://github.com/explosion/spaCy/issues
- Gensim Word2Vec Documentation: http://radimrehurek.com/gensim/models/word2vec.html
- Gensim Word2Vec GitHub repository: [link](https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/word2vec.ipynb)
- Google Word2Vec: https://code.google.com/archive/p/word2vec/
- GitHub Repository for Doc2Vec Illustration: https://github.com/linanqiu/word2vec-sentiments
---

# Contributors

- Prateek Gupta
- Sidharth Goutam Karji
- Pasumarthi Mukesh Gupta
- Gourav Sharma
- Aman Jaiswal
- Praveen Kumar


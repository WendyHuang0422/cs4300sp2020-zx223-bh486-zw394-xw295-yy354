final version: https://twittedfacts.herokuapp.com 

version1: https://twittedfactv1.herokuapp.com 
version2: https://twittedfactsv2.herokuapp.com

Project Description: This app automatically relates a celebrity’s tweets to the relevant news pages to help users fact-check claims made by the celebrity and show whether there is a disagreement between the news page and the celebrity’s claim.

Description of Baseline Method : The current version of the project has 2 major ways of implementations and three main components for each implementation. The two implementations are respectively ad-hoc retrieval-matching and database retrieval-matching. The major differences between the two implementations lie in the ways tweets are matched to the news sources. In the database version, the full-texts of news are retrieved using newspaper3k and converted into inverted index matrices (that are stored in the DB) in order to perform cosine similarity search later. In contrast, ad-hoc search uses boolean search based on the generated keywords for each cluster of tweets which are related in topics to find relevant news (due to our lack of access to the full text, we can only rely on the in_built boolean search provided by the API).





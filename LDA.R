#install.packages("topicmodels", repos = "http://cran.us.r-project.org")
#install.packages("tm", repos = "http://cran.us.r-project.org")
#install.packages("SnowballC", repos = "http://cran.us.r-project.org")
#Data <- read.csv(file="totalData.csv", header=TRUE, sep=",")
#corpus <- Corpus(VectorSource(Data))
#corp_dtm <- DocumentTermMatrix(corpus) 
#rowTotals <- apply(corp_dtm , 1, sum)
#corp_dtm.new   <- corp_dtm[rowTotals> 0, ] 
library(tm)
library(topicmodels)
library(SnowballC)
library(tm)
library(Matrix)
#Here Reading only top 1000 lines from the totalData.csv
#There are 999 patients, first line is header and 2230 CUIs
#IN general, 999 documents, 2230 terms
a <- read.csv("~/Downloads/totalData_m.csv")
#Convert CSV to sparse matrix, this will optimize memory
#Plus facilitate conversion later
a_m <- Matrix(as.matrix(a),sparse=TRUE)
a_mt <- as.DocumentTermMatrix(a_m, weighting = weightTf)
a_mt
#This should yield 999 documents and 2230 terms
ldafit_gibbs <- LDA(corp_dtm.new, k=10, method="Gibbs", control=list(alpha=0.5)) 
posterior(ldafit_gibbs)$terms


corp <- Corpus(DirSource("/Users/christopherpan 1/wiki_input_mysql"),readerControl = list(language="en"))

summary(corp)

#dtm <- DocumentTermMatrix(a)

corp <- tm_map(corp, removeNumbers)
corp <- tm_map(corp, removePunctuation)
corp <- tm_map(corp, stripWhitespace)
corp <- tm_map(corp, tolower)
corp <- tm_map(corp, removeWords, stopwords("english"))
corp <- tm_map(corp, stemDocument, language = "english")

corp_dtm <- DocumentTermMatrix(corp)
corp_dtm <- removeSparseTerms(corp_dtm, 0.75)

#Note that alpha is a hyperparameter
#LDA in R selects alpha = 50/k if not specified
#LDA in Python Gensim selects alpha = 1/k
#Basically smaller the alpha documents contain mixture of fewer topics (sparse solutions favored)
#Full documentation is available at: https://cran.r-project.org/web/packages/topicmodels/topicmodels.pdf 

ldafit_gibbs <- LDA(corp_dtm, k=2, method="Gibbs", control=list(alpha=0.5)) 
posterior(ldafit_gibbs)$topics
posterior(ldafit_gibbs)$terms

ldafit_vem <- LDA(corp_dtm, k=10, method="VEM")
posterior(ldafit_vem)$topics
posterior(ldafit_vem)$terms

ldafit_ctm_vem <- LDA(corp_dtm.new, k=10, method="VEM")
posterior(ldafit_ctm_vem)$topics
posterior(ldafit_ctm_vem)$terms 

# topic-modeling-harvard
Healthcare research project utilizing Natural Language Processing techniques to classify large volume corpora of patient files into categories of diseases. 
Experimented with regression and a novel approach to boost traditional Latent Dirichlet Allocation (LDA) algorithm performance by using expert knowledge and prior probability on relevant concepts. Prior probability was trained from public domain data including Medline, Medscape, Merck Manual and Wikipedia. Large scale pre-processing of > 50,000 medical articles representing > 1.5MM Concept Unique Identifiers was used to identify concepts that best describe each disease. Inverse probability sampling (based on correlation to the main disease) was used to construct training samples. Fifty-fold cross validation with Elastic LASSO augmented with hyperparameter optimization was used to select relevant concepts and train weights.

from .replicate_embeddings import ReplicateEmbeddings
from nltk.cluster import KMeansClusterer
import nltk
from typing import Any
from scipy.spatial import distance_matrix
import pandas as pd
import numpy as np
from .sections import introduction, discussion

class Summarizer:
    def _distance_from_centroid(self,row) -> Any:
        #type of emb and centroid is different, hence using tolist below 
        return distance_matrix([row['embeddings']], [row['centroid'].tolist()])[0][0]
    
    def summarize_text(self,text) -> str:
        """Summarization takes place in 4 steps:
        * Embedding the sentences using ReplicateEmbeddings.
        * Clustering them acccording to their embedding vectors. We are using cosine_distance as a measure to determine the distance/similarity between 2 vectors.
        * Computing the distance between the sentence vector and the centroid (also called mean) vector.
        * Sorting the sentences based on their sequence in the original text.
        """
        #nltk.download('punkt')
        # Embedding
        tokenized_text = nltk.sent_tokenize(text)
        sentences = [sentence.strip() for sentence in tokenized_text]
        cluster_count= 10 if len(sentences) > 9 else len(sentences)
        iterations=25
        embedding = ReplicateEmbeddings()
        embdedded_text = embedding.embed_texts(sentences)

        # Clustering
        df = pd.DataFrame({'sentence': sentences, 'embeddings': embdedded_text})
        X = np.array(df['embeddings'].tolist())
        kclusterer = KMeansClusterer(
                cluster_count, distance=nltk.cluster.util.cosine_distance,
                repeats=iterations,avoid_empty_clusters=True)
        assigned_clusters = kclusterer.cluster(X, assign_clusters=True)

        # Computing distance 
        df['cluster']=pd.Series(assigned_clusters, index=df.index)
        df['centroid']=df['cluster'].apply(lambda x: kclusterer.means()[x])
        df['distance_from_centroid'] = df.apply(self._distance_from_centroid, axis=1)

        # Sorting sentences
        summary=' '.join(df.sort_values('distance_from_centroid',ascending = True).groupby('cluster').head(1).sort_index()['sentence'].tolist())
        return summary
    
    def demo():
        sections = [introduction,discussion]
        summarizer = Summarizer()

        for section in sections:
            summmary = summarizer.summarize_text(section)
            print(f"{summmary} \n")

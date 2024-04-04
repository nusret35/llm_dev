from dotenv import load_dotenv
from typing import Dict, List
import replicate


class ReplicateEmbeddings:
    """Sends request to Replicate's endpoint for MPNet Base v2, 
    the model that is dedicated for generating text embeddings.
    Model can run slow in the first calls, since it cold boots regularly. 
    """

    model_name:str = "replicate/all-mpnet-base-v2:b6b7585c9640cd7a9572c6e129c9549d79c9c31f0d3fdce7baac7c67ca38f305"

    def _get_embeddings(self,text_batch:List[str]) -> List[Dict]:
        load_dotenv()
        output = replicate.run(self.model_name,
                      input={
                          "text_batch":str(text_batch).replace("'",'"')
                      })
        
        return output

    def embed_texts(self, texts:List[str]) -> List[List[float]]:
        """Embed a list of texts using the all-mpnet-base-v2 model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """

        embeddings = self._get_embeddings(texts)
        embeddings_list = [instance["embedding"] for instance in embeddings]
        return embeddings_list
    


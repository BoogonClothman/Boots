# Core/Memory/rag.py
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os

class MemoryManager:
    """Manager of memory."""
    def __init__(
            self,
            ragmodel_path: str,
            device: str,
            cache_dir: str,
            local_file_only: bool,
            index_path: str,
            pickle_path: str,
            txts_dir: str
            ):
        """
        Constructor of MemoryManager.
        
        Args:
            ragmodel_path (str): Path to RAG model.
            device (str): Device to run the model.
            cache_dir (str): Path to cache directory.
            local_file_only (bool): Whether to use local files only. If True, the model will not be downloaded, and the downloaded cache will be used.
            index_path (str): Path to index file.
            pickle_path (str): Path to pickle file.
            txts_dir (str): Path to directory of texts.
            
        Attributes:
            ragmodel (SentenceTransformer): RAG model.
            index (str): Path to index file.
            pickle (str): Path to pickle file.
            doc_dir (str): Path to directory of documents.
        """
        self.ragmodel = SentenceTransformer(
            model_name_or_path=ragmodel_path,
            device=device,
            cache_folder=cache_dir,
            local_files_only=local_file_only
        )
        self.index = index_path
        self.pickle = pickle_path
        self.doc_dir = txts_dir
    
    def create_index(self):
        """Create index and pickle files."""
        def load_texts(directory):
            texts = []
            for filename in os.listdir(directory):
                if filename.endswith(".txt"):
                    with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                        texts.append(f.read())
            return texts
        texts = load_texts(self.doc_dir)
        embedding = self.ragmodel.encode(texts, normalize_embeddings=True).astype("float32")
        dimension = embedding.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embedding)
        # Generate index.faiss and texts.pkl
        faiss.write_index(index, self.index)
        print(f"[MemoryManager.create_index] Index \"{self.index}\" has been created.")
        with open(self.pickle, "wb") as f:
            pickle.dump(texts, f)
        print(f"[MemoryManager.create_index] Pickle \"{self.pickle}\" has been created.")

    def query(
            self,
            key: str,
            top_k: int,
            similarity_threshold: float
            ):
        """
        Query the memory with a key.

        Args:
            key (str): Key to query.
            top_k (int): Number of results to return.
            similarity_threshold (float): Threshold of similarity score.

        Returns:
            results (list): List of results.
        """
        query_embedding = self.ragmodel.encode([key], normalize_embeddings=True).astype("float32")
        index = faiss.read_index(self.index)
        D, I = index.search(query_embedding, top_k)
        with open(self.pickle, "rb") as f:
            texts = pickle.load(f)
        results = []
        for i in range(top_k):
            similarity_score = D[0][i]
            text = texts[I[0][i]]
            print(f"[MemoryManager.query] result {i}: {text} -- {similarity_score:.4f}")
            if similarity_threshold is None or similarity_score >= similarity_threshold:
                results.append(text)
        print(f"[MemoryManager.query] results: {results}")
        return results

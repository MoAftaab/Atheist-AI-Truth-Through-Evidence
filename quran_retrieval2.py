"""
Quran Retrieval Module

A reusable FAISS-based semantic search system for the Quran.
Provides class-based interface for building and querying the index.
"""

import json
import os
import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import faiss


def format_result(result: dict) -> str:
    """
    Format a search result into a nicely formatted multiline string.
    
    Args:
        result: Dictionary containing ayah data with score
        
    Returns:
        Formatted string representation
    """
    lines = [
        f"Surah {result['surah_number']} ({result['surah_name_english']}), Ayah {result['ayah_number']}",
        f"Arabic: {result['text_simple']}",
        f"Translation: {result['translation_en_yusufali']}",
        f"Score: {result.get('score', 0.0):.4f}"
    ]
    return "\n".join(lines)


class QuranRetrieval:
    """
    A reusable FAISS-based retrieval system for Quran verses.
    
    Provides lazy loading of models and indices, automatic index building,
    and semantic search capabilities.
    """
    
    def __init__(self,
                 json_path: str = "quran_full_formatted.json",
                 index_path: str = "quran_faiss.index",
                 metadata_path: str = "quran_metadata.json",
                 texts_path: str = "quran_texts.json",
                 model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the QuranRetrieval system.
        
        Args:
            json_path: Path to the Quran JSON file
            index_path: Path to save/load FAISS index
            metadata_path: Path to save/load metadata JSON
            texts_path: Path to save/load texts JSON (optional)
            model_name: Sentence transformer model name
        """
        self.json_path = json_path
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.texts_path = texts_path
        self.model_name = model_name
        
        # Lazy-loaded attributes
        self._model: Optional[SentenceTransformer] = None
        self._index: Optional[faiss.Index] = None
        self._metadata: Optional[List[Dict[str, Any]]] = None
    
    def _load_model(self) -> SentenceTransformer:
        """Lazily load the sentence transformer model."""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model
    
    def _load_index(self) -> faiss.Index:
        """Lazily load the FAISS index, building it if necessary."""
        if self._index is None:
            if not os.path.exists(self.index_path):
                print("FAISS index not found. Building index...")
                self.build_index()
            
            self._index = faiss.read_index(self.index_path)
        return self._index
    
    def _load_metadata(self) -> List[Dict[str, Any]]:
        """Lazily load metadata, building index if necessary."""
        if self._metadata is None:
            if not os.path.exists(self.metadata_path):
                print("Metadata not found. Building index...")
                self.build_index()
            
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self._metadata = json.load(f)
        return self._metadata
    
    def _load_quran_data(self) -> List[Dict[str, Any]]:
        """
        Load Quran JSON file and flatten into ayah-level records.
        
        Returns:
            List of ayah-level dictionaries
        """
        # Try to find JSON file in common locations if not found
        if not os.path.exists(self.json_path):
            possible_paths = [
                "quran_full_formatted.json",
                "Downloads/quran_full_formatted.json",
                "../Downloads/quran_full_formatted.json",
                os.path.join(os.path.expanduser("~"), "Downloads", "quran_full_formatted.json")
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.json_path = path
                    break
            else:
                raise FileNotFoundError(
                    f"Quran JSON file not found at {self.json_path}. "
                    f"Please provide a valid path."
                )
        
        print(f"Loading Quran data from {self.json_path}...")
        
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        ayah_records = []
        
        for surah in data["quran"]:
            surah_number = surah["surah_number"]
            surah_name_english = surah["surah_name_english"]
            total_ayahs = surah["total_ayahs"]
            
            for ayah in surah["ayahs"]:
                # Create ayah-level record
                record = {
                    "surah_number": surah_number,
                    "surah_name_english": surah_name_english,
                    "total_ayahs": total_ayahs,
                    "ayah_number": ayah["ayah_number"],
                    "text_simple": ayah["text_simple"],
                    "translation_en_yusufali": ayah["translation_en_yusufali"]
                }
                
                # Create searchable text string for embeddings
                searchable_text = (
                    f"Surah {surah_number} {surah_name_english}, "
                    f"Ayah {ayah['ayah_number']}: {ayah['translation_en_yusufali']} | {ayah['text_simple']}"
                )
                record["searchable_text"] = searchable_text
                
                ayah_records.append(record)
        
        print(f"✓ Loaded {len(ayah_records)} ayahs from {len(data['quran'])} surahs")
        return ayah_records
    
    def _create_embeddings(self, ayah_records: List[Dict[str, Any]]) -> np.ndarray:
        """
        Create sentence embeddings for all ayah texts.
        
        Args:
            ayah_records: List of ayah-level dictionaries
            
        Returns:
            NumPy array of embeddings (shape: [num_ayahs, embedding_dim])
        """
        model = self._load_model()
        
        print("Creating embeddings for all ayahs...")
        texts = [record["searchable_text"] for record in ayah_records]
        embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        
        # Ensure float32 for FAISS
        embeddings = embeddings.astype(np.float32)
        
        print(f"✓ Created embeddings: shape {embeddings.shape}")
        return embeddings
    
    def _build_faiss_index(self, embeddings: np.ndarray) -> faiss.Index:
        """
        Build and save a FAISS index from embeddings.
        
        Args:
            embeddings: NumPy array of embeddings
            
        Returns:
            FAISS index object
        """
        print("Building FAISS index...")
        
        # Get embedding dimension
        embedding_dim = embeddings.shape[1]
        
        # Create FAISS index (using Inner Product for cosine similarity)
        # Normalize embeddings for cosine similarity with Inner Product
        embeddings_copy = embeddings.copy()
        faiss.normalize_L2(embeddings_copy)
        index = faiss.IndexFlatIP(embedding_dim)
        
        # Add embeddings to index
        index.add(embeddings_copy)
        
        # Save index to disk
        print(f"Saving FAISS index to {self.index_path}...")
        faiss.write_index(index, self.index_path)
        
        print(f"✓ FAISS index built and saved: {index.ntotal} vectors")
        return index
    
    def _save_metadata(self, ayah_records: List[Dict[str, Any]]):
        """
        Save metadata and searchable texts to JSON files.
        
        Args:
            ayah_records: List of ayah-level dictionaries
        """
        print(f"Saving metadata to {self.metadata_path}...")
        
        # Prepare metadata (exclude searchable_text from metadata)
        metadata = []
        texts = []
        
        for record in ayah_records:
            metadata_record = {
                "surah_number": record["surah_number"],
                "surah_name_english": record["surah_name_english"],
                "total_ayahs": record["total_ayahs"],
                "ayah_number": record["ayah_number"],
                "text_simple": record["text_simple"],
                "translation_en_yusufali": record["translation_en_yusufali"]
            }
            metadata.append(metadata_record)
            texts.append(record["searchable_text"])
        
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        with open(self.texts_path, "w", encoding="utf-8") as f:
            json.dump(texts, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Metadata and texts saved")
    
    def build_index(self) -> None:
        """
        Builds FAISS index and saves metadata if not already built.
        
        This method will:
        1. Load the Quran JSON file
        2. Flatten into ayah-level records
        3. Create embeddings using the sentence transformer
        4. Build and save the FAISS index
        5. Save metadata to JSON files
        """
        # Load and flatten data
        ayah_records = self._load_quran_data()
        
        # Create embeddings
        embeddings = self._create_embeddings(ayah_records)
        
        # Build FAISS index
        self._build_faiss_index(embeddings)
        
        # Save metadata
        self._save_metadata(ayah_records)
        
        # Reset lazy-loaded attributes to force reload
        self._index = None
        self._metadata = None
        
        print("\n✓ Index building complete!")
    
    def search(self, 
               query: str, 
               k: int = 5,
               score_threshold: float | None = None,
               return_no_answer: bool = True) -> List[Dict[str, Any]]:
        """
        Search for similar ayahs using semantic search.
        
        Args:
            query: Search query string
            k: Number of top results to return
            score_threshold: Minimum similarity score (None = no threshold)
            return_no_answer: If True, return empty list when no results meet threshold.
                            If False, return best-effort results even if below threshold.
            
        Returns:
            List of dictionaries containing search results with scores.
            Each result includes:
            - surah_number
            - surah_name_english
            - ayah_number
            - text_simple
            - translation_en_yusufali
            - score (similarity score)
        """
        if not query or not query.strip():
            return []
        
        # Load model, index, and metadata
        model = self._load_model()
        index = self._load_index()
        metadata = self._load_metadata()
        
        # Encode query
        query_embedding = model.encode([query], convert_to_numpy=True).astype(np.float32)
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = index.search(query_embedding, k)
        
        # Format results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if 0 <= idx < len(metadata):
                result = metadata[idx].copy()
                result["score"] = float(score)  # Convert numpy float to Python float
                results.append(result)
        
        # Apply score threshold filtering if specified
        if score_threshold is not None:
            filtered_results = [r for r in results if r["score"] >= score_threshold]
            
            if len(filtered_results) >= 1:
                # Return filtered results (already sorted by score, highest first)
                return filtered_results
            else:
                # No results meet threshold
                if return_no_answer:
                    return []
                else:
                    # Best-effort fallback: return original results
                    return results
        
        return results
    
    def get_verse_by_reference(self, surah_number: int, ayah_number: int) -> Optional[Dict[str, Any]]:
        """
        Returns a single verse dict from metadata by exact reference.
        
        Args:
            surah_number: Surah number (1-114)
            ayah_number: Ayah number within the surah
            
        Returns:
            Dictionary containing verse data, or None if not found
        """
        metadata = self._load_metadata()
        
        for verse in metadata:
            if verse["surah_number"] == surah_number and verse["ayah_number"] == ayah_number:
                return verse.copy()
        
        return None
    
    def add_context_window(self, result: dict, window: int = 1) -> dict:
        """
        Given a single ayah result, attach context verses from the same surah
        within ±window of ayah_number.
        
        Args:
            result: Single ayah result dictionary
            window: Number of ayahs before and after to include
            
        Returns:
            New dictionary with added "context" key containing list of context ayahs.
            Does not modify the input result.
        """
        metadata = self._load_metadata()
        surah_number = result["surah_number"]
        ayah_number = result["ayah_number"]
        
        # Find all ayahs in the same surah
        surah_ayahs = [v for v in metadata if v["surah_number"] == surah_number]
        
        # Determine context range
        min_ayah = max(1, ayah_number - window)
        max_ayah = min(
            max(v["ayah_number"] for v in surah_ayahs) if surah_ayahs else ayah_number,
            ayah_number + window
        )
        
        # Collect context ayahs (excluding the main result ayah)
        context = []
        for verse in surah_ayahs:
            if min_ayah <= verse["ayah_number"] <= max_ayah and verse["ayah_number"] != ayah_number:
                context_entry = {
                    "surah_number": verse["surah_number"],
                    "surah_name_english": verse["surah_name_english"],
                    "ayah_number": verse["ayah_number"],
                    "text_simple": verse["text_simple"],
                    "translation_en_yusufali": verse["translation_en_yusufali"]
                }
                context.append(context_entry)
        
        # Sort context by ayah_number
        context.sort(key=lambda x: x["ayah_number"])
        
        # Create new result dict with context
        result_with_context = result.copy()
        result_with_context["context"] = context
        
        return result_with_context
    
    def search_with_context(self,
                           query: str,
                           k: int = 5,
                           score_threshold: float | None = None,
                           window: int = 1) -> List[Dict[str, Any]]:
        """
        Search for similar ayahs and add context window to each result.
        
        Args:
            query: Search query string
            k: Number of top results to return
            score_threshold: Minimum similarity score (None = no threshold)
            window: Number of ayahs before and after to include in context
            
        Returns:
            List of dictionaries with context added to each result
        """
        results = self.search(query, k=k, score_threshold=score_threshold, return_no_answer=True)
        
        # Add context to each result
        results_with_context = []
        for result in results:
            result_with_context = self.add_context_window(result, window=window)
            results_with_context.append(result_with_context)
        
        return results_with_context
    
    def retrieve_citation_bundle(self,
                                query: str,
                                k: int = 5,
                                score_threshold: float | None = None,
                                window: int = 1) -> Dict[str, Any]:
        """
        Retrieve search results with context and return as a structured citation bundle.
        
        Args:
            query: Search query string
            k: Number of top results to return
            score_threshold: Minimum similarity score (None = no threshold)
            window: Number of ayahs before and after to include in context
            
        Returns:
            Dictionary with query, parameters, has_answer flag, and results with context.
            All values are JSON-serializable.
        """
        results = self.search_with_context(query, k=k, score_threshold=score_threshold, window=window)
        
        # Ensure all values are JSON-serializable (convert numpy types)
        serializable_results = []
        for result in results:
            serializable_result = {
                "surah_number": int(result["surah_number"]),
                "surah_name_english": str(result["surah_name_english"]),
                "ayah_number": int(result["ayah_number"]),
                "text_simple": str(result["text_simple"]),
                "translation_en_yusufali": str(result["translation_en_yusufali"]),
                "score": float(result["score"]),
                "context": []
            }
            
            # Serialize context entries
            for ctx in result.get("context", []):
                serializable_result["context"].append({
                    "surah_number": int(ctx["surah_number"]),
                    "surah_name_english": str(ctx["surah_name_english"]),
                    "ayah_number": int(ctx["ayah_number"]),
                    "text_simple": str(ctx["text_simple"]),
                    "translation_en_yusufali": str(ctx["translation_en_yusufali"])
                })
            
            serializable_results.append(serializable_result)
        
        bundle = {
            "query": str(query),
            "k": int(k),
            "score_threshold": float(score_threshold) if score_threshold is not None else None,
            "has_answer": len(serializable_results) > 0,
            "results": serializable_results
        }
        
        return bundle


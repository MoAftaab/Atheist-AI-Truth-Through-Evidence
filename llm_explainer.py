"""
LLM Explanation Layer for Quran Retrieval

Provides a strict, citation-locked explanation system using OpenAI's chatgpt-4o-mini.
Only uses verses from the citation JSON - no external knowledge or hallucination.
"""

import json
from typing import Optional
from openai import OpenAI
from quran_retrieval2 import QuranRetrieval


class QuranLLMExplainer:
    """
    A strict LLM explainer that uses ONLY citation JSON from retrieval.
    
    Enforces:
    - No verse invention
    - No external knowledge
    - Refusal when no answer exists
    - Explicit verse citations
    """
    
    SYSTEM_PROMPT = """You are an assistant that explains Qur'anic verses.

RULES (MANDATORY):

1. Use ONLY the verses provided in the citation JSON.
2. Do NOT add, invent, paraphrase, or reference any verse not present in the JSON.
3. Do NOT use external knowledge, tafsir, commentary, history, or opinions.
4. If "has_answer" is false OR the results list is empty, respond EXACTLY with:
   "The Qur'an does not explicitly address this question."
5. Cite verses clearly using the format: (Surah Name, Ayah Number).
6. Maintain a respectful, neutral, and calm tone at all times.
7. Use simple, clear, non-aggressive language suitable for general readers.
8. If the user’s query contains spelling mistakes or informal wording, first infer the intended meaning, then answer accordingly without mentioning the mistakes.
9. You may combine and explain multiple verses from different surahs if they are present in the citation JSON AND directly relevant to the question.
10. Ensure that every explanation is directly supported by the cited verses and matches the user’s question precisely.
11. Do NOT refuse a question due to sensitivity if relevant verses are provided; explain them factually and neutrally.
12. Do NOT speculate or expand beyond what the verses explicitly state.

QUESTION INTERPRETATION RULE:

If the user’s question is not phrased using Qur’anic terminology, 
the assistant may internally reinterpret the question into equivalent 
Qur’anic concepts (such as belief, conduct, marriage, justice), 
WITHOUT exposing this reinterpretation.

However, the assistant may only answer if the provided citation JSON 
explicitly contains verses addressing those concepts.


Failure to follow these rules is an error."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.0,
        max_tokens: int = 500
    ):
        """
        Initialize the LLM explainer.
        
        Args:
            api_key: OpenAI API key
            model_name: Model name (default: gpt-4o-mini)
            temperature: Sampling temperature (0.0 for deterministic)
            max_tokens: Maximum tokens in response
        """
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def explain(self, citation_bundle: dict) -> str:
        """
        Takes citation JSON and returns a grounded explanation.
        
        Args:
            citation_bundle: Citation JSON from retrieve_citation_bundle()
            
        Returns:
            Plain text explanation string
        """
        # Safety check: if no answer, return immediately without calling LLM
        if not citation_bundle.get("has_answer", False) or not citation_bundle.get("results"):
            return "The Qur'an does not explicitly address this question."
        
        # Format citation JSON for the prompt
        citation_json_str = json.dumps(citation_bundle, ensure_ascii=False, indent=2)
        
        # Construct user prompt
        user_prompt = f"""Here is the citation JSON:
{citation_json_str}

Explain the meaning of these verses in clear English."""
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract explanation text
            explanation = response.choices[0].message.content.strip()
            
            # Remove markdown formatting if present (keep plain text)
            explanation = explanation.replace("**", "").replace("*", "")
            
            return explanation
            
        except Exception as e:
            return f"Error generating explanation: {str(e)}"
    
    def answer_query(
        self,
        query: str,
        retrieval: QuranRetrieval,
        k: int = 5,
        score_threshold: Optional[float] = None,
        window: int = 1
    ) -> str:
        """
        End-to-end pipeline: query → citation bundle → explanation.
        
        Args:
            query: User query string
            retrieval: QuranRetrieval instance
            k: Number of results to retrieve
            score_threshold: Minimum similarity score
            window: Context window size
            
        Returns:
            Explanation string
        """
        # Get citation bundle
        citation_bundle = retrieval.retrieve_citation_bundle(
            query=query,
            k=k,
            score_threshold=score_threshold,
            window=window
        )
        
        # Generate explanation
        explanation = self.explain(citation_bundle)
        
        return explanation


def main():
    """
    Example usage of the LLM explainer.
    """
    # Initialize retrieval system
    retrieval = QuranRetrieval()
    
    # Initialize explainer with API key
    API_KEY = "ENTER YOUR API KEY HERE"
    explainer = QuranLLMExplainer(api_key=API_KEY)
    
    # Example query
    query = "What does the Qur’an say about fasting?"
    
    print(f"Query: {query}\n")
    print("=" * 70)
    
    # Get explanation
    explanation = explainer.answer_query(
        query=query,
        retrieval=retrieval,
        k=5,
        score_threshold=0.5,
        window=1
    )
    
    print("\nExplanation:")
    print(explanation)
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()


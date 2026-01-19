"""
Blog Generator Module
Interfaces with Google Gemini API to generate blog content.
Handles retry logic and response parsing.
"""

import logging
import json
import re
from typing import Dict
from tenacity import retry, stop_after_attempt, wait_exponential
import google.generativeai as genai
from app.config import settings

logger = logging.getLogger(__name__)


class BlogGenerator:
    """Generates blog content using Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client."""
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key not configured")
        
        genai.configure(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model
        self.gemini_model = genai.GenerativeModel(self.model)
        logger.info(f"BlogGenerator initialized with Gemini model: {self.model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def _call_gemini(self, prompt: str) -> str:
        """
        Call Google Gemini API with retry logic.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        try:
            # Gemini configuration for JSON output
            # Use low temperature for more deterministic, JSON-friendly output
            generation_config = {
                "temperature": 0.0,
                "top_p": 1.0,
                "top_k": 0,
                "max_output_tokens": 2500,
            }
            
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            content = response.text
            logger.info(f"Gemini API call successful")
            
            return content
            
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            raise
    
    def parse_json_response(self, response: str) -> Dict:
        """
        Parse JSON response from LLM.
        Handles markdown code blocks and malformed JSON.
        
        Args:
            response: Raw response from LLM
            
        Returns:
            Parsed JSON dictionary
        """
        # Helper: try to json.loads and return None on failure
        def try_loads(text: str):
            try:
                return json.loads(text)
            except Exception:
                return None

        # Strip common markdown code fences
        if "```json" in response:
            try:
                response = response.split("```json", 1)[1].split("```", 1)[0]
            except Exception:
                pass
        elif "```" in response:
            try:
                # take the first fenced block
                response = response.split("```", 1)[1].split("```", 1)[0]
            except Exception:
                pass

        raw = response.strip()

        # First quick attempt
        data = try_loads(raw)
        if data is not None:
            return data

        # Attempt 2: extract first JSON object substring (from first '{' to last '}')
        first_brace = raw.find('{')
        last_brace = raw.rfind('}')
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            candidate = raw[first_brace:last_brace+1]
            data = try_loads(candidate)
            if data is not None:
                return data

        # Attempt 3: normalize smart quotes and remove trailing commas
        cleaned = raw
        # Replace smart quotes with straight quotes
        cleaned = cleaned.replace('“', '"').replace('”', '"')
        cleaned = cleaned.replace("‘", "'").replace("’", "'")

        # Remove control characters that may break JSON (except newline)
        cleaned = re.sub(r"[\x00-\x1f\x7f]", '', cleaned)

        # Remove trailing commas before closing braces/brackets
        cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

        # Try loads again
        data = try_loads(cleaned)
        if data is not None:
            return data

        # Attempt 4: try to find a JSON-like block with braces and balance them
        # progressively expand from the first '{'
        if first_brace != -1:
            for end in range(first_brace+1, min(len(raw), first_brace+20000)):
                if raw[end] == '}':
                    candidate = raw[first_brace:end+1]
                    # quick check for balanced braces
                    if candidate.count('{') == candidate.count('}'):
                        data = try_loads(candidate)
                        if data is not None:
                            return data

        # All attempts failed - log helpful debug info
        logger.error("Failed to parse JSON response: all recovery attempts failed")
        logger.debug(f"Raw response (first 2000 chars): {raw[:2000]}")
        raise ValueError("LLM did not return valid JSON")

    def _reformat_to_json(self, raw_response: str) -> str:
        """
        Ask the LLM to convert a previously returned (malformed) output into valid JSON
        matching our schema. Returns the raw text the model produced (should be JSON).
        """
        try:
            repair_prompt = (
                "The previous output was not valid JSON.\n"
                "Below is the original output. Convert it into a single, valid JSON object that matches this schema:\n"
                "{\n"
                "  \"title\": string,\n"
                "  \"meta_description\": string,\n"
                "  \"introduction\": string,\n"
                "  \"sections\": [ { \"heading\": string, \"content\": string } ],\n"
                "  \"conclusion\": string,\n"
                "  \"cta\": string,\n"
                "  \"tags\": [string]\n"
            "}\n"
                "Return ONLY the valid JSON object, with straight quotes, no trailing commas, and no additional text.\n\n"
                "ORIGINAL OUTPUT:\n" + raw_response
            )

            repair_resp = self._call_gemini(repair_prompt)
            logger.info("Requested LLM to reformat output into valid JSON")
            return repair_resp
        except Exception as e:
            logger.error(f"Reformatting request failed: {str(e)}")
            raise
    
    def generate(self, prompt: str) -> Dict:
        """
        Generate blog content from prompt.
        
        Args:
            prompt: Structured prompt for blog generation
            
        Returns:
            Dictionary with blog content structure
            
        Raises:
            ValueError: If generation or parsing fails
        """
        try:
            # Call Gemini API
            response = self._call_gemini(prompt)
            
            # Parse response
            try:
                blog_data = self.parse_json_response(response)
            except ValueError:
                # Attempt automatic reformat: ask the model to convert its previous output into valid JSON
                logger.warning("Initial parse failed - attempting to ask LLM to reformat its output into valid JSON")
                repaired = self._reformat_to_json(response)
                blog_data = self.parse_json_response(repaired)
            
            logger.info("Blog generation successful")
            return blog_data
            
        except Exception as e:
            logger.error(f"Blog generation failed: {str(e)}")
            raise
    
    def estimate_cost(self, prompt_length: int, expected_output_length: int = 2000) -> float:
        """
        Estimate API cost for generation (approximate).
        
        Args:
            prompt_length: Length of prompt in characters
            expected_output_length: Expected output length in characters
            
        Returns:
            Estimated cost in USD
        """
        # Rough token estimation: 1 token ≈ 4 characters
        prompt_tokens = prompt_length // 4
        output_tokens = expected_output_length // 4
        
        # Gemini Flash is very cost-effective
        # Approximate pricing for Gemini 2.0
        total_cost = ((prompt_tokens + output_tokens) / 1000) * 0.0001
        return total_cost


# Convenience function
def generate_blog(prompt: str) -> Dict:
    """
    Generate blog from prompt (convenience function).
    
    Args:
        prompt: Input prompt
        
    Returns:
        Blog content dictionary
    """
    generator = BlogGenerator()
    return generator.generate(prompt)

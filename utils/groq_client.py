from groq import Groq
import json
import logging
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqClient:
    """Groq API client for generating flashcards."""
    
    def __init__(self):
        if Config.GROQ_API_KEY and not Config.GROQ_API_KEY.startswith('gsk_dummy'):
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            self.model = Config.GROQ_MODEL
            self.enabled = True
        else:
            logger.warning("Groq API key not available - running in development mode")
            self.client = None
            self.model = Config.GROQ_MODEL
            self.enabled = False
    
    def generate_flashcards(self, topic, num_flashcards=8):
        """
        Generate flashcards for a given topic using Groq API.
        
        Args:
            topic (str): The topic for which to generate flashcards
            num_flashcards (int): Number of flashcards to generate
        
        Returns:
            list: List of flashcard dictionaries with 'question' and 'answer' keys
        """
        if not self.enabled:
            logger.warning("Groq API not available - returning sample flashcards")
            return self._get_sample_flashcards(topic)
        
        try:
            # Construct the prompt for flashcard generation
            prompt = self._create_flashcard_prompt(topic, num_flashcards)
            
            # Make API call to Groq
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator who creates high-quality educational flashcards. Always respond with valid JSON format containing an array of flashcard objects."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2048,
                top_p=1,
                stream=False,
                stop=None,
            )
            
            # Extract and parse the response
            response_text = completion.choices[0].message.content.strip()
            logger.info(f"Groq API response received for topic: {topic}")
            
            # Parse JSON response
            flashcards = self._parse_flashcard_response(response_text)
            
            return flashcards if flashcards else self._get_sample_flashcards(topic)
            
        except Exception as e:
            logger.error(f"Error generating flashcards: {str(e)}")
            # Return sample flashcards as fallback
            return self._get_sample_flashcards(topic)
    
    def _create_flashcard_prompt(self, topic, num_flashcards):
        """Create a prompt for flashcard generation."""
        prompt = f"""Create {num_flashcards} educational flashcards about "{topic}". 

Requirements:
- Each flashcard should have a clear, concise question and a comprehensive answer
- Questions should test understanding, not just memorization
- Answers should be informative but not too lengthy
- Cover different aspects of the topic
- Use varied question types (what, how, why, when, where)
- Ensure questions are appropriate for learning and studying

Return the flashcards in this exact JSON format:
{{
  "flashcards": [
    {{
      "question": "Clear, specific question about the topic",
      "answer": "Comprehensive but concise answer"
    }}
  ]
}}

Topic: {topic}
Generate {num_flashcards} flashcards now."""
        
        return prompt
    
    def _parse_flashcard_response(self, response_text):
        """Parse the JSON response from Groq API."""
        try:
            # Clean up the response text
            response_text = response_text.strip()
            
            # Handle potential markdown code blocks
            if '```json' in response_text:
                # Extract JSON from markdown code block
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                if end != -1:
                    response_text = response_text[start:end].strip()
            elif '```' in response_text:
                # Handle generic code blocks
                start = response_text.find('```') + 3
                end = response_text.rfind('```')
                if end != -1 and end > start:
                    response_text = response_text[start:end].strip()
                    # Remove any language identifier
                    lines = response_text.split('\n')
                    if lines and not lines[0].strip().startswith('{'):
                        response_text = '\n'.join(lines[1:]).strip()
            
            # Look for JSON content between curly braces
            if not response_text.startswith('{'):
                start = response_text.find('{')
                end = response_text.rfind('}')
                if start != -1 and end != -1 and end > start:
                    response_text = response_text[start:end+1]
            
            # Parse JSON
            parsed_response = json.loads(response_text)
            
            # Extract flashcards array
            if 'flashcards' in parsed_response:
                flashcards = parsed_response['flashcards']
            else:
                # Assume the response is directly an array
                flashcards = parsed_response
            
            # Validate flashcard structure
            validated_flashcards = []
            for card in flashcards:
                if isinstance(card, dict) and 'question' in card and 'answer' in card:
                    validated_flashcards.append({
                        'question': str(card['question']).strip(),
                        'answer': str(card['answer']).strip()
                    })
            
            return validated_flashcards
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Response text: {response_text}")
            return []
        except Exception as e:
            logger.error(f"Error parsing flashcard response: {str(e)}")
            return []
    
    def _get_sample_flashcards(self, topic):
        """Return sample flashcards as fallback."""
        return [
            {
                "question": f"What is the main concept of {topic}?",
                "answer": f"This is a sample answer about {topic}. The actual content would depend on the specific topic being studied."
            },
            {
                "question": f"Why is {topic} important?",
                "answer": f"{topic} is important because it helps us understand key concepts and principles in this subject area."
            },
            {
                "question": f"How can you apply knowledge of {topic}?",
                "answer": f"Knowledge of {topic} can be applied in various practical situations and helps build understanding of related concepts."
            }
        ]

# Global Groq client instance
groq_client = GroqClient()

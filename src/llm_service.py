from langchain_openai import ChatOpenAI
from src.config import OPENROUTER_API_KEY, LLM_MODEL
import json

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=OPENROUTER_API_KEY,
            model=LLM_MODEL,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.7
        )
    
    def generate_question(self, idea_context):
        """Generate next clarifying question based on context"""
        prompt = f"Based on this idea: {idea_context}\nAsk one clarifying question to better understand it."
        response = self.llm.invoke(prompt)
        return response.content
    
    

    def score_idea(self, idea_name, idea_description, retrieved_chunks, mode):
        """Score idea using LLM with few-shot prompting."""

        # Build few-shot examples
        if retrieved_chunks:
            examples = "\n\n".join(
                [
                    f"Example {i+1}:\n"
                    f"{chunk['text'][:200]}...\n"
                    f"(Mode: {chunk['mode']}, Similarity: {chunk['score']:.2f})"
                    for i, chunk in enumerate(retrieved_chunks[:3])
                ]
            )
        else:
            examples = "No similar examples found."

        # Criteria and JSON schema based on mode
        if mode.lower() == "startup":

            dimensions = """
    1. Market Size (20%) - TAM, growth potential
    2. Problem Fit (15%) - Real customer pain?
    3. Competition (15%) - Direct/indirect competitors, defensibility
    4. Team Feasibility (15%) - Required skills vs founder background
    5. Revenue Model (15%) - Clear monetization path
    6. Go-to-Market (10%) - Distribution channel clarity
    7. Timing (10%) - Market maturity, tech readiness
    """

            json_schema = """
    {
    "market_size": {"score": 0, "reason": ""},
    "problem_fit": {"score": 0, "reason": ""},
    "competition": {"score": 0, "reason": ""},
    "team_feasibility": {"score": 0, "reason": ""},
    "revenue_model": {"score": 0, "reason": ""},
    "go_to_market": {"score": 0, "reason": ""},
    "timing": {"score": 0, "reason": ""},
    "overall_score": 0,
    "strengths": [],
    "weaknesses": [],
    "improvements": [],
    "recommendation": ""
    }
    """

        else:

            dimensions = """
    1. Industry Relevance (20%) - Solves real problem?
    2. Technical Depth (20%) - Demonstrates mastery?
    3. Differentiation (15%) - Unique vs typical projects?
    4. Skill Alignment (15%) - Targets desired tech stack?
    5. Execution Feasibility (15%) - Doable in 2-4 months?
    6. Placement Utility (10%) - Hireable signal?
    7. Scope & Polish (5%) - MVP quality vs overambition?
    """

            json_schema = """
    {
    "industry_relevance": {"score": 0, "reason": ""},
    "technical_depth": {"score": 0, "reason": ""},
    "differentiation": {"score": 0, "reason": ""},
    "skill_alignment": {"score": 0, "reason": ""},
    "execution_feasibility": {"score": 0, "reason": ""},
    "placement_utility": {"score": 0, "reason": ""},
    "scope_polish": {"score": 0, "reason": ""},
    "overall_score": 0,
    "strengths": [],
    "weaknesses": [],
    "improvements": [],
    "recommendation": ""
    }
    """

        # Build Prompt
        prompt = f"""
    You are an experienced {mode} advisor.

    Below are similar examples retrieved from a database.

    SIMILAR EXAMPLES:
    {examples}

    ----------------------------------------

    IDEA TO EVALUATE

    Name:
    {idea_name}

    Description:
    {idea_description}

    Type:
    {mode.upper()}

    ----------------------------------------

    Evaluate this idea.

    Score EACH criterion from 1-10.

    Criteria:
    {dimensions}

    For EACH criterion:
    - score
    - explain the reasoning in 2-3 sentences

    Finally provide:
    - weighted overall score
    - top 3 strengths
    - top 3 weaknesses
    - top 3 improvements
    - recommendation (BUILD / VALIDATE / REJECT)

    Return ONLY valid JSON.

    JSON Format:

    {json_schema}
    """

        # Call LLM
        response = self.llm.invoke(prompt)

        # Extract response text
        if hasattr(response, "content"):
            text = response.content
        elif hasattr(response, "text"):
            text = response.text
        else:
            text = str(response)

        text = text.strip()

        # Remove markdown if present
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        # Parse JSON
        try:
            return json.loads(text)

        except Exception as e:
            return {
                "error": str(e),
                "raw_response": text
            }
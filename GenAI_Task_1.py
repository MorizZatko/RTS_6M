"""GenAI task 1.

This module sets up the Google GenAI client, queries available models,
and requests structured 3D scene generation and sentiment analysis
using Pydantic schemas for data validation and parsing.
"""

from pydantic import BaseModel, Field
from google import genai
from typing import List
from dotenv import load_dotenv
import os


class Asset(BaseModel):
    """Schema representing an individual 3D asset within a scene."""

    asset_name: str
    spawn_position: List[float]
    estimated_scale: float

class Scene(BaseModel):
    """Schema representing the overall generated scene containing multiple assets."""

    items: List[Asset]

# Load environment variables from a .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

# List available models that support text/content generation
for m in client.models.list():
    if 'generateContent' in m.supported_actions:
        print(f"ID: {m.name}")

# Request structured JSON output using the Pydantic schema
res = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Generiere ein Sci-Fi Lager mit 3 verschiedenen Kisten und einem Terminal",
    config={'response_mime_type': 'application/json', 'response_schema': Scene}
)

# Extract and iterate through the parsed Pydantic objects directly
asset_obj = res.parsed
for item in asset_obj.items:
    print(f"Baue {item.asset_name} bei {item.spawn_position}")

class PromptAnalysis(BaseModel):
    """Schema for analyzing prompt sentiment and key phrases."""

    sentiment: str = Field(
        description="The sentiment of the prompt, e.g., positive, neutral or negative"
    )
    score: float = Field(
        description="1.0"
    )
    key_phrases: List[str] = Field(
        description="Dark"
    )


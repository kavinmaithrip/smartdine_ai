import os
import random
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY not found in environment.")

client = Groq(api_key=api_key)


class LLMExplainer:
    """
    LLaMA-3 based explanation generator.

    Guarantees:
    - Unique wording per item
    - Natural tone (no forced patterns)
    - Weather mentioned ONLY when relevant
    """

    def explain(
        self,
        *,
        item,
        city,
        mood=None,
        weather=None,
        surprise=False
    ) -> str:

        dish = item.get("Item_Name", "this dish")
        restaurant = item.get("Restaurant_Name", "this restaurant")
        rating = item.get("Average_Rating", "N/A")
        cuisine = item.get("Cuisine", "the cuisine")
        price = "budget-friendly" if item.get("Is_Expensive") == 0 else "premium"

        weather_category = weather.get("category") if weather else None

        
        style = random.choice([
            "friendly foodie tone",
            "warm and comforting",
            "casual and conversational",
            "short and energetic",
            "descriptive and thoughtful"
        ])

        
        system_prompt = (
            "You are a food recommendation assistant like Swiggy or Zomato.\n"
            "Every explanation must be unique.\n"
            "Avoid generic phrases like 'solid pick', 'fits the moment', or 'quietly delivers'.\n"
            "Mention at least one concrete attribute such as flavor, spice level, texture, or richness.\n"
            "Sound natural and human."
        )

        
        weather_instruction = ""
        if weather_category:
            weather_instruction = (
                f"- If relevant, relate the dish to the {weather_category} weather.\n"
                "- Do NOT force weather if it sounds unnatural.\n"
            )

        
        user_prompt = f"""
Write a {style} explanation in 1–2 sentences.

Dish: {dish}
Restaurant: {restaurant}
City: {city}
Cuisine: {cuisine}
Rating: {rating}/5
Price: {price}
Mood: {mood or "unspecified"}
Surprise mode: {surprise}

Guidelines:
{weather_instruction}
- Do not reuse sentence patterns
- Avoid vague wording
- Focus on why someone would enjoy this dish
"""

        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=random.uniform(0.9, 1.1),
                max_tokens=90
            )
            return response.choices[0].message.content.strip()

        except Exception:
            
            if weather_category:
                fallbacks = [
                    f"In {city}’s {weather_category} weather, the flavors of {dish} at {restaurant} feel especially comforting.",
                    f"The {dish.lower()} from {restaurant} works well right now, particularly with the {weather_category} conditions.",
                    f"{dish} at {restaurant} feels like a natural choice given the {weather_category} weather in {city}."
                ]
            else:
                fallbacks = [
                    f"{dish} from {restaurant} stands out for its flavors and is an easy choice if you’re deciding quickly.",
                    f"If you’re in the mood for something familiar, {restaurant} does this dish particularly well.",
                    f"This dish offers a satisfying balance of taste and comfort without overthinking the choice."
                ]

            return random.choice(fallbacks)

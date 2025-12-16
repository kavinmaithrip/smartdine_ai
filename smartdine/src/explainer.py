import random

class SmartExplainer:

    WEATHER_PHRASES = {
        "hot": [
            "perfect for a hot day",
            "great when the weather is warm",
            "refreshing for today’s heat"
        ],
        "cold": [
            "ideal for a cool day",
            "perfect when it’s a bit chilly",
            "comforting in this cold weather"
        ],
        "pleasant": [
            "great for a pleasant day",
            "a lovely choice for today’s weather",
            "perfect for this kind of weather"
        ],
        "rainy": [
            "perfect for rainy weather",
            "comforting on a rainy day",
            "a great pick while it’s raining"
        ],
        "unknown": [
            "a great choice right now",
            "something locals really enjoy",
            "a solid pick anytime"
        ]
    }

    OPENERS = [
        "You might enjoy",
        "A great choice would be",
        "You should definitely try",
        "This could be perfect for you"
    ]

    SURPRISE_OPENERS = [
        "Feeling adventurous?",
        "Can’t decide?",
        "Let us surprise you!",
        "Here’s a fun pick for you"
    ]

    def explain(self, *, item, city, mood=None, weather=None, surprise=False):
        dish = item.get("Item_Name", "this dish")
        restaurant = item.get("Restaurant_Name", "this restaurant")

        weather_cat = weather.get("category", "unknown") if weather else "unknown"
        weather_phrase = random.choice(self.WEATHER_PHRASES.get(weather_cat, self.WEATHER_PHRASES["unknown"]))

        opener = random.choice(
            self.SURPRISE_OPENERS if surprise else self.OPENERS
        )

        reason_parts = []

        if mood and not surprise:
            reason_parts.append(f"it matches your {mood} craving")

        if item.get("Is_Bestseller") == 1:
            reason_parts.append("it’s one of their popular picks")

        if item.get("Is_Expensive") == 0:
            reason_parts.append("it’s budget-friendly")

        reason_text = ""
        if reason_parts:
            reason_text = " because " + " and ".join(reason_parts)

        return (
            f"{opener}, {dish} from {restaurant} in {city} — "
            f"{weather_phrase}{reason_text}."
        )

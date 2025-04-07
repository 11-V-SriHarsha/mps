import re
from google import genai
import json

YOUR_API_KEY = "AIzaSyBYkQTlg8E9fytxPsRhejzMnWfXWayzBOg"
client = genai.Client(api_key=YOUR_API_KEY)

def clean_json_output(text):
    cleaned = re.sub(r"```(?:json)?\n(.*?)```", r"\1", text.strip(), flags=re.DOTALL)
    return cleaned.strip()

def parse_trends(text):
    # More robust parsing with error handling
    result = []
    for pair in text.split(","):
        try:
            parts = pair.split("-", 1)
            if len(parts) == 2:
                date = parts[0].strip()
                # Handle percentage signs and other non-numeric characters
                value_str = re.sub(r'[^\d.]', '', parts[1].strip())
                value = int(float(value_str)) if value_str else 0
                result.append({"date": date, "value": value})
        except (ValueError, IndexError) as e:
            print(f"Error parsing trend: {pair} - {str(e)}")
    return result

def parse_seasonal(text):
    # More robust parsing with error handling
    result = []
    for pair in text.split(","):
        try:
            parts = pair.split("-", 1)
            if len(parts) == 2:
                season = parts[0].strip()
                # Handle percentage signs and other non-numeric characters
                value_str = re.sub(r'[^\d.]', '', parts[1].strip())
                value = int(float(value_str)) if value_str else 0
                result.append({"season": season, "requirement": value})
        except (ValueError, IndexError) as e:
            print(f"Error parsing seasonal: {pair} - {str(e)}")
    return result

def parse_distribution(text):
    # More robust parsing with error handling
    result = []
    for pair in text.split(","):
        try:
            parts = pair.split("-", 1)
            if len(parts) == 2:
                name = parts[0].strip()
                # Handle percentage signs and other non-numeric characters
                value_str = re.sub(r'[^\d.]', '', parts[1].strip())
                value = int(float(value_str)) if value_str else 0
                result.append({"name": name, "value": value})
        except (ValueError, IndexError) as e:
            print(f"Error parsing distribution: {pair} - {str(e)}")
    return result

def parse_imbalance(text):
    # More robust parsing with error handling
    result = []
    # Clean up text by removing the explanatory part after "the imbalance should be..."
    text = text.split("the imbalance should be")[0].strip()
    for pair in text.split(","):
        try:
            parts = pair.split("-", 1)
            if len(parts) == 2:
                nutrient = parts[0].strip()
                # Handle percentage signs and other non-numeric characters
                value_str = re.sub(r'[^\d.]', '', parts[1].strip())
                value = int(float(value_str)) if value_str else 0
                result.append({"nutrient": nutrient, "value": value})
        except (ValueError, IndexError) as e:
            print(f"Error parsing imbalance: {pair} - {str(e)}")
    return result

def get_fertiliser_query(fertilizer_name: str, nitrogen: float, phosphorus: float, potassium: float):
    prompt = f""" Give a structured fertilizer recommendation for the following:

Fertilizer: {fertilizer_name}
Nutrient Levels:
- Nitrogen: {nitrogen}
- Phosphorus: {phosphorus}
- Potassium: {potassium}

I want the output strictly in this format:

Fertilizer: <Fertilizer Name>
Dosage: <Application dosage and frequency>
Best Practices: <How to apply the fertilizer>
Warnings: <Warnings or side-effects>
Trends: Jan-0, Feb-0, Mar-15, Apr-15, May-15
Seasonal Requirements: Spring-33, Summer-33, Autumn-33, Winter-0
Nutrient Distribution: Nitrogen-38, Phosphorus-23, Potassium-15
Nutrient Imbalance: Nitrogen-50, Phosphorus-30, Potassium-20

Please use only numeric values (no text or percentages) for all the data points in Trends, Seasonal Requirements, Nutrient Distribution, and Nutrient Imbalance.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        print("Raw Gemini Output:\n", response.text)
        
        # Extract sections more robustly
        text = response.text.strip()
        sections = {}
        
        # Extract each section
        fertilizer_match = re.search(r'Fertilizer:\s*(.*?)(?:\n|$)', text)
        dosage_match = re.search(r'Dosage:\s*(.*?)(?:\n|$)', text)
        practices_match = re.search(r'Best Practices:\s*(.*?)(?:\n|$)', text)
        warnings_match = re.search(r'Warnings:\s*(.*?)(?:\n|$)', text)
        trends_match = re.search(r'Trends:\s*(.*?)(?:\n|$)', text)
        seasonal_match = re.search(r'Seasonal Requirements:\s*(.*?)(?:\n|$)', text)
        distribution_match = re.search(r'Nutrient Distribution:\s*(.*?)(?:\n|$)', text)
        imbalance_match = re.search(r'Nutrient Imbalance:\s*(.*?)(?:\n|$)', text)
        
        return {
            "fertilizer": {"name": fertilizer_match.group(1).strip() if fertilizer_match else fertilizer_name},
            "dosage": dosage_match.group(1).strip() if dosage_match else "",
            "bestPractices": practices_match.group(1).strip() if practices_match else "",
            "warnings": warnings_match.group(1).strip() if warnings_match else "",
            "trendsData": parse_trends(trends_match.group(1)) if trends_match else [],
            "seasonalRequirements": parse_seasonal(seasonal_match.group(1)) if seasonal_match else [],
            "nutrientDistribution": parse_distribution(distribution_match.group(1)) if distribution_match else [],
            "nutrientImbalance": parse_imbalance(imbalance_match.group(1)) if imbalance_match else [],
            "npk_values": {
                "n": nitrogen,
                "p": phosphorus,
                "k": potassium
            }
        }
        
    except Exception as e:
        print(f"Error in get_fertiliser_query: {str(e)}")
        return {"error": str(e), "npk_values": {"n": nitrogen, "p": phosphorus, "k": potassium}}

# Example test
if __name__ == "__main__":
    result = get_fertiliser_query("Urea", 80, 40, 60)
    print("Parsed Fertilizer JSON:\n", json.dumps(result, indent=2))
import requests
from typing import Optional, Dict
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def fetch_food_data(query: str) -> Optional[Dict]:
    """
    Fetch nutritional information from USDA Food Data Central API
    """
    api_key = settings.USDA_API_KEY
    base_url = "https://api.nal.usda.gov/fdc/v1"
    
    # Search for the food item
    search_url = f"{base_url}/foods/search"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "pageSize": 1,
        "sortBy": "score",
        "sortOrder": "desc"
    }
    
    try:
        logger.info(f"Searching for food: {query}")
        logger.debug(f"Making request to {search_url} with payload: {payload}")
        
        response = requests.post(
            f"{search_url}?api_key={api_key}",
            headers=headers,
            json=payload
        )
        
        logger.info(f"API Response status: {response.status_code}")
        logger.debug(f"API Response headers: {response.headers}")
        
        if response.status_code != 200:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return None
            
        data = response.json()
        logger.debug(f"API Response data: {data}")
        
        if not data.get('foods'):
            logger.warning(f"No foods found for query: {query}")
            return None
            
        food = data['foods'][0]
        nutrients = food.get('foodNutrients', [])
        
        logger.info(f"Found food: {food.get('description')} with {len(nutrients)} nutrients")
        
        # Extract relevant nutritional information
        nutrition_data = {
            'food_name': food.get('description', ''),
            'calories': 0,
            'carbs': 0,
            'protein': 0,
            'fat': 0
        }
        
        # Map nutrient numbers to our fields
        nutrient_map = {
            '208': 'calories',    # Energy (kcal)
            '205': 'carbs',       # Carbohydrates
            '203': 'protein',     # Protein
            '204': 'fat'          # Total fat
        }
        
        for nutrient in nutrients:
            nutrient_number = str(nutrient.get('nutrientNumber', ''))
            if nutrient_number in nutrient_map:
                field_name = nutrient_map[nutrient_number]
                value = nutrient.get('value', 0)
                if value is not None:
                    nutrition_data[field_name] = round(float(value), 2)
                logger.debug(f"Found {field_name}: {value}")
        
        logger.info(f"Processed nutrition data: {nutrition_data}")
        return nutrition_data
        
    except requests.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in fetch_food_data: {str(e)}")
        return None

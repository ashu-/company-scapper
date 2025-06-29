from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import os
from dotenv import load_dotenv
from firecrawl import JsonConfig, FirecrawlApp
from pydantic import BaseModel
from src.utils.company_info import get_company_info

# Load environment variables
load_dotenv(override=True)

company_bp = Blueprint('company', __name__)

class ExtractSchema(BaseModel):
    company_name: str
    company_url: str
    company_mission: str
    what_company_does_in_100_words: str
    kind_of_products_services: str
    customers_if_available_on_website: str
    company_size: str
    company_location: str
    comany_functionality: str

@company_bp.route('/scrape', methods=['POST'])
@cross_origin()
def scrape_company():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Initialize Firecrawl app
        app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
        
        # Configure JSON extraction schema
        json_config = JsonConfig(schema=ExtractSchema)
        
        # Scrape the URL
        llm_extraction_result = app.scrape_url(
            url,
            formats=["json"],
            json_options=json_config,
            only_main_content=False,
            timeout=120000
        )
        
        data = llm_extraction_result.json
        company_name = data.get('company_name')
        company_url = data.get('company_url')
        search_query = company_name + " " + company_url
        company_info = get_company_info(search_query)
        print(company_info)
        data['company_info'] = company_info
        return jsonify({
            'success': True,
            'data': data,
            'url': url
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


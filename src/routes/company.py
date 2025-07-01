from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import os
from dotenv import load_dotenv
from firecrawl import JsonConfig, FirecrawlApp
from pydantic import BaseModel
from pydantic.functional_serializers import SerializeAsAny
from src.utils.company_info import get_company_info

# Load environment variables
load_dotenv(override=True)

company_bp = Blueprint('company', __name__)

from enum import Enum

class Sector(Enum):
    E_COMMERCE = "E-Commerce"
    FINTECH = "FinTech"
    AI = "AI"
    SAAS = "SaaS"
    HEALTH_TECH = "Health Tech"
    MOBILITY_TECH = "Mobility Tech"
    EDTECH = "EdTech"
    REAL_ESTATE_PROPTECH = "Real Estate - Proptech"
    F_AND_B = "F&B"
    AGRITECH = "Agritech"
    MEDIA_ENTERTAINMENT = "Media & Entertainment"
    RETAIL_TECH = "RetailTech"
    CONSUMER_SERVICE_LIFESTYLE = "Consumer Service & Lifestyle"
    MANUFACTURING = "Manufacturing"
    ENERGY_SUSTAINABILITY = "Energy & Sustainability"
    DEEPTECH = "DeepTech"
    TELECOM = "Telecom"
    LEGALTECH = "LegalTech"
    OTHERS = "Others"

class SubSector(Enum):
    # E-Commerce Subsectors
    B2C_ECOMMERCE = "B2C E-commerce"
    B2B_ECOMMERCE = "B2B E-commerce"
    VERTICAL_ECOMMERCE = "Vertical E-commerce"
    SOCIAL_COMMERCE = "Social Commerce"
    QUICK_COMMERCE = "Quick Commerce"
    CROSS_BORDER_COMMERCE = "Cross-border Commerce"
    RESALE_RECOMMERCE = "Resale & Recommerce"
    AGGREGATOR = "Aggregator"
    MARKETPLACE = "Marketplace"
    
    # FinTech Subsectors
    DIGITAL_PAYMENTS = "Digital Payments"
    DIGITAL_BANKING = "Digital Banking"
    DIGITAL_LENDING = "Digital Lending"
    WEALTH_MANAGEMENT = "Wealth Management"
    INSURANCE_TECHNOLOGY = "Insurance Technology"
    CRYPTOCURRENCY_BLOCKCHAIN = "Cryptocurrency & Blockchain"
    REGTECH = "RegTech"
    CREDIT_INFRASTRUCTURE = "Credit Infrastructure"
    FINTECH_CONSULTING = "Consulting"
    NEO_BANK = "Neo Bank"
    
    # AI Subsectors
    CONVERSATIONAL_AI = "Conversational AI"
    VOICE_AI = "Voice AI"
    COMPUTER_VISION = "Computer Vision"
    AI_INFRASTRUCTURE = "AI Infrastructure"
    GENERATIVE_AI = "Generative AI"
    AI_FOR_ENTERPRISE = "AI for Enterprise"
    AI_IN_HEALTHCARE = "AI in Healthcare"
    AI_IN_FINANCE = "AI in Finance"
    EDGE_AI = "Edge AI"
    AI_MEDIA = "Media (img/video/music)"
    AI_CONSULTING = "Consulting"
    LLM = "LLM"
    AI_3D = "3D"
    AI_REASONING_MATH = "Reasoning / Math"
    AI_ROBOTICS = "Robotics"
    AUTONOMOUS_VEHICLES = "Autonomous Vehicles"
    AI_CLOUD = "AI Cloud"
    AI_CHIPS = "Chips"
    AI_DEPLOYMENT_SERVING = "Deployment & serving"
    MODEL_TUNING = "Model Tuning"
    ORCHESTRATOR_AGENT_BUILDER = "Orchestrator/agent builder"
    LLMOPS = "LLMOps"
    EVALS_RL = "Evals + RL"
    VECTOR_DBS = "Vector DBs"
    DATA_PIPELINE = "Data pipeline"
    AI_PRIVACY = "Privacy"
    AI_SECURITY = "Security"
    AI_OTHERS = "Others"
    AGENTIC_PLATFORM = "Agentic Platform"
    AI_CUSTOMER_SUPPORT = "Customer Support"
    AI_SALES = "Sales"
    AI_MARKETING = "Marketing"
    AI_CUSTOMER_SUCCESS = "Customer Success"
    AI_HR = "HR"
    AI_SOFTWARE_DEV = "Software Dev"
    AI_DEVOPS = "DevOps"
    AI_LEGAL_COMPLIANCE = "Legal/Compliance"
    AI_FINANCE = "Finance"
    AI_PROCUREMENT = "Procurement"
    AI_PRODUCTIVITY = "Productivity"
    AI_ANALYTICS = "Analytics"
    AI_LEGAL = "Legal"
    AI_AUDIT_ACCOUNTING = "Audit & Accounting"
    AI_IT_SERVICES = "IT Services"
    AI_CALL_CENTRES = "Call Centres"
    AI_HEALTHCARE_PROVIDERS = "Healthcare Providers"
    AI_BIOTECH = "Biotech"
    AI_INSURANCE = "Insurance"
    AI_HOSPITALITY = "Hospitality"
    AI_MANUFACTURING = "Manufacturing"
    AI_ECOMMERCE = "Ecommerce"
    AI_GAMING = "Gaming"
    AI_PRIVATE_EQUITY = "Private Equity"
    AI_WEALTH_MANAGEMENT = "Wealth Management"
    AI_SERVICES = "AI Services"
    AI_RECRUITMENT = "Recruitment"
    AI_CALL_CENTRE = "Call Centre"
    AI_HEALTH = "Health"
    AI_ACCOUNTING_FINANCE = "Accounting/ Finance"
    AI_EDTECH = "Edtech"
    AI_CREATOR_ECONOMY = "Creator Economy"
    AI_PRIMARY_HEALTH = "Primary health"
    AI_MENTAL_HEALTH = "Mental Health"
    AI_NO_CODE = "No Code / Low Code / Zero Code"
    AI_OBSERVABILITY = "Observability"
    AI_RCM = "RCM"
    AI_TRAVEL = "Travel"
    AI_RETAIL_ECOMMERCE = "Retail/E-commerce"
    AI_TRANSPORTATION_LOGISTICS = "Transportation/Logistics"
    AI_SECURITY_FRAUD = "Security/Fraud Detection"
    AI_AGRICULTURE = "Agriculture"
    AI_DEVOPS_MLOPS = "DevOps/MLOps"
    AI_LEGAL_TECH = "Legal Tech"
    AI_EDUCATION = "Education"
    
    # SaaS Subsectors
    CRM_SALES = "CRM & Sales"
    HR_TECHNOLOGY = "HR Technology"
    MARKETING_TECHNOLOGY = "Marketing Technology"
    PRODUCTIVITY_TOOLS = "Productivity Tools"
    INDUSTRY_SPECIFIC_SOFTWARE = "Industry-Specific Software"
    DATA_ANALYTICS = "Data & Analytics"
    CYBERSECURITY = "Cybersecurity"
    CLOUD_INFRASTRUCTURE = "Cloud Infrastructure"
    
    # Health Tech Subsectors
    TELEMEDICINE = "Telemedicine"
    DIGITAL_THERAPEUTICS = "Digital Therapeutics"
    HEALTH_RECORDS = "Health Records"
    MEDICAL_DEVICES = "Medical Devices"
    PHARMACEUTICAL = "Pharmaceutical"
    MENTAL_HEALTH = "Mental Health"
    FITNESS_WELLNESS = "Fitness & Wellness"
    HEALTHCARE_ANALYTICS = "Healthcare Analytics"
    ONCOLOGY = "Oncology"
    
    # Mobility Tech Subsectors
    MOBILITY_AGGREGATORS = "Aggregators"
    LOGISTICS_DELIVERY = "Logistics & Delivery"
    ELECTRIC_VEHICLES = "Electric Vehicles"
    MICRO_MOBILITY = "Micro-mobility"
    FLEET_MANAGEMENT = "Fleet Management"
    TRANSPORTATION_ANALYTICS = "Transportation Analytics"
    AUTOMOTIVE_TECHNOLOGY = "Automotive Technology"
    PUBLIC_TRANSPORTATION = "Public Transportation"
    NAVIGATION = "Navigation"
    
    # EdTech Subsectors
    K12_EDUCATION = "K-12 Education"
    HIGHER_EDUCATION = "Higher Education"
    PROFESSIONAL_TRAINING = "Professional Training"
    LANGUAGE_LEARNING = "Language Learning"
    TEST_PREPARATION = "Test Preparation"
    VOCATIONAL_TRAINING = "Vocational Training"
    EDUCATIONAL_CONTENT = "Educational Content"
    EDUCATION_INFRASTRUCTURE = "Education Infrastructure"
    
    # Real Estate - Proptech Subsectors
    PROPERTY_PLATFORMS = "Property Platforms"
    PROPERTY_MANAGEMENT = "Property Management"
    REAL_ESTATE_FINANCING = "Real Estate Financing"
    CONSTRUCTION_TECHNOLOGY = "Construction Technology"
    COMMERCIAL_REAL_ESTATE = "Commercial Real Estate"
    PROPERTY_ANALYTICS = "Property Analytics"
    BUILDING_MATERIALS = "Building Materials"
    SMART_HOME = "Smart Home"
    
    # F&B Subsectors
    FOOD_DELIVERY = "Food Delivery"
    FOOD_TECHNOLOGY = "Food Technology"
    RESTAURANT_TECHNOLOGY = "Restaurant Technology"
    NUTRITION_DIET = "Nutrition & Diet"
    BEVERAGE_INNOVATION = "Beverage Innovation"
    SUPPLY_CHAIN = "Supply Chain"
    FOOD_SAFETY = "Food Safety"
    
    # Agritech Subsectors
    PRECISION_AGRICULTURE = "Precision Agriculture"
    FARM_MANAGEMENT = "Farm Management"
    AGRICULTURAL_MARKETPLACE = "Agricultural Marketplace"
    AGRI_SUPPLY_CHAIN = "Supply Chain"
    AGRICULTURAL_FINANCE = "Agricultural Finance"
    SUSTAINABLE_AGRICULTURE = "Sustainable Agriculture"
    AGRICULTURAL_BIOTECHNOLOGY = "Agricultural Biotechnology"
    
    # Media & Entertainment Subsectors
    OTT_PLATFORMS = "OTT Platforms"
    GAMING = "Gaming"
    CONTENT_CREATION = "Content Creation"
    DIGITAL_PUBLISHING = "Digital Publishing"
    SOCIAL_MEDIA = "Social Media"
    VIRTUAL_EVENTS = "Virtual Events"
    SPORTS_TECHNOLOGY = "Sports Technology"
    
    # RetailTech Subsectors
    POINT_OF_SALE = "Point of Sale"
    RETAIL_ANALYTICS = "Retail Analytics"
    RETAIL_SUPPLY_CHAIN = "Supply Chain Management"
    CUSTOMER_EXPERIENCE = "Customer Experience"
    VISUAL_MERCHANDISING = "Visual Merchandising"
    RETAIL_AUTOMATION = "Retail Automation"
    FRANCHISE_MANAGEMENT = "Franchise Management"
    
    # Consumer Service & Lifestyle Subsectors
    HOME_SERVICES = "Home Services"
    APPAREL = "Apparel"
    PERSONAL_CARE = "Personal Care"
    TRAVEL_HOSPITALITY = "Travel & Hospitality"
    EVENT_MANAGEMENT = "Event Management"
    SUBSCRIPTION_SERVICES = "Subscription Services"
    PEER_TO_PEER_SERVICES = "Peer-to-Peer Services"
    LIFESTYLE_APPS = "Lifestyle Apps"
    CS_FITNESS_WELLNESS = "Fitness & Wellness"
    MATRIMONY = "Matrimony"
    RELIGIOUS_TECH = "Religious Tech"
    
    # Manufacturing Subsectors
    SMART_MANUFACTURING = "Smart Manufacturing"
    SUPPLY_CHAIN_OPTIMIZATION = "Supply Chain Optimization"
    METAVERSE = "Metaverse"
    INDUSTRIAL_AUTOMATION = "Industrial Automation"
    MFG_ROBOTICS = "Robotics"
    DIGITAL_TWIN = "Digital Twin"
    ADDITIVE_MANUFACTURING = "Additive Manufacturing"
    SUSTAINABLE_MANUFACTURING = "Sustainable Manufacturing"
    HARDWARE = "Hardware"
    SEMICONDUCTORS = "Semiconductors"
    MFG_DEFENCE_TECHNOLOGY = "Defence Technology"
    
    # Energy & Sustainability Subsectors
    RENEWABLE_ENERGY = "Renewable Energy"
    ENERGY_MANAGEMENT = "Energy Management"
    CARBON_MANAGEMENT = "Carbon Management"
    WASTE_MANAGEMENT = "Waste Management"
    WATER_TECHNOLOGY = "Water Technology"
    ENVIRONMENTAL_MONITORING = "Environmental Monitoring"
    GREEN_FINANCE = "Green Finance"
    CLEANTECH = "Cleantech"
    
    # DeepTech Subsectors
    QUANTUM_COMPUTING = "Quantum Computing"
    BIOTECHNOLOGY = "Biotechnology"
    NANOTECHNOLOGY = "Nanotechnology"
    DT_ROBOTICS = "Robotics"
    ADVANCED_MATERIALS = "Advanced Materials"
    SPACE_TECHNOLOGY = "Space Technology"
    NUCLEAR_TECHNOLOGY = "Nuclear Technology"
    AEROSPACE = "Aerospace"
    DT_DEFENCE_TECHNOLOGY = "Defence Technology"
    
    # Telecom Subsectors
    TELECOM_5G = "5G & Telecommunications"
    
    # LegalTech Subsectors
    LEGAL = "Legal"
    
    # Others Subsectors
    EXTENDED_REALITY = "Extended Reality (XR)"
    INTERNET_OF_THINGS = "Internet of Things (IoT)"
    DIGITAL_IDENTITY = "Digital Identity"
    AUTOMATION_RPA = "Automation & RPA"
    WEB3 = "Web3"

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
    sector: Sector
    sub_sector: SubSector

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
        # company_info = get_company_info(search_query)
        # print(company_info)
        # data['company_info'] = company_info
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


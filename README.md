# Company Information Scraper

A web application that extracts structured company information from any website using Firecrawl AI technology.

## Features

- **Simple URL Input**: Enter any company website URL
- **AI-Powered Extraction**: Uses Firecrawl to intelligently extract company information
- **Structured Output**: Displays information in organized, easy-to-read cards
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Real-time Processing**: Live feedback during extraction process

## Extracted Information

The application extracts the following company details:

- **Company Mission**: The company's mission statement and core values
- **What Company Does**: A 100-word summary of the company's activities
- **Products & Services**: Types of products and services offered
- **Target Customers**: Information about the company's customer base
- **Company Size**: Details about the organization's scale
- **Location**: Company's geographical location
- **Core Functionality**: Main business functions and operations

## Technology Stack

### Backend
- **Flask**: Python web framework
- **Firecrawl**: AI-powered web scraping and data extraction
- **Pydantic**: Data validation and serialization
- **Flask-CORS**: Cross-origin resource sharing support

### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: Advanced styling with gradients, animations, and responsive design
- **JavaScript**: Interactive functionality and API communication
- **Font Awesome**: Professional icons

## Project Structure

```
company-scraper/
├── src/
│   ├── main.py              # Flask application entry point
│   ├── routes/
│   │   ├── company.py       # Company scraping API endpoints
│   │   └── user.py          # User management (template)
│   ├── models/
│   │   └── user.py          # Database models (template)
│   ├── static/
│   │   └── index.html       # Frontend interface
│   └── database/
│       └── app.db           # SQLite database
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (API keys)
└── README.md               # This documentation
```

## API Endpoints

### POST /api/scrape
Extracts company information from a given URL.

**Request Body:**
```json
{
    "url": "https://example.com"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "company_mission": "...",
        "what_company_does_in_100_words": "...",
        "kind_of_products_services": "...",
        "customers_if_available_on_website": "...",
        "company_size": "...",
        "company_location": "...",
        "comany_functionality": "..."
    },
    "url": "https://example.com"
}
```

## Environment Variables

Create a `.env` file in the project root with:

```
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

## Local Development

1. **Clone and Setup**:
   ```bash
   cd company-scraper
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   - Create `.env` file with your Firecrawl API key

4. **Run the Application**:
   ```bash
   python src/main.py
   ```

5. **Access the Application**:
   - Open http://localhost:5000 in your browser

## Usage Instructions

1. **Enter URL**: Type or paste a company website URL in the input field
2. **Extract Information**: Click the "Extract Info" button
3. **Wait for Processing**: The application will show a loading indicator
4. **View Results**: Extracted information will be displayed in organized cards
5. **Try Another URL**: Enter a new URL to extract information from another company

## Features in Detail

### User Interface
- **Responsive Design**: Works on desktop and mobile devices
- **Modern Styling**: Gradient backgrounds, rounded corners, and shadows
- **Interactive Elements**: Hover effects and smooth transitions
- **Loading States**: Visual feedback during processing
- **Error Handling**: Clear error messages for failed requests

### Data Processing
- **URL Validation**: Automatic protocol addition for incomplete URLs
- **Structured Extraction**: Uses Pydantic models for data validation
- **Timeout Handling**: 120-second timeout for complex websites
- **Error Recovery**: Graceful handling of extraction failures

### Performance
- **Efficient API Calls**: Single request per URL
- **Optimized Frontend**: Minimal JavaScript for fast loading
- **Responsive Backend**: Flask with proper CORS configuration

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Firecrawl API key is correctly set in the `.env` file
2. **URL Not Working**: Try adding `https://` prefix to the URL
3. **Slow Extraction**: Some complex websites may take longer to process
4. **No Results**: Some websites may not have extractable company information

### Error Messages

- **"Please enter a valid URL"**: The URL field is empty or invalid
- **"Network error"**: Connection issues with the backend
- **"Failed to scrape the website"**: The Firecrawl service couldn't extract information

## Deployment

For production deployment, consider:
- Using a production WSGI server (e.g., Gunicorn)
- Setting up proper environment variable management
- Implementing rate limiting for API calls
- Adding user authentication if needed

## License

This project is created for demonstration purposes. Please ensure you have proper licensing for Firecrawl API usage in production environments.

## Support

For issues or questions about this application, please refer to:
- Firecrawl documentation for API-related questions
- Flask documentation for backend modifications
- This README for general usage instructions


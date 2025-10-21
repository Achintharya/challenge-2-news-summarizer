# Challenge 2: Web Scraper with AI Summarization (AWS Lambda)

## Overview

A serverless web scraping tool that extracts content from any URL and generates intelligent summaries using Mistral AI. Built with AWS Lambda for the backend and a simple HTML frontend hosted on Vercel.

## Features

- 🌐 **Web Scraping**: Extract content from any webpage URL
- 🤖 **AI Summarization**: Intelligent summaries using Mistral AI
- ⚡ **Serverless**: AWS Lambda backend for scalability
- 🌍 **Web UI**: Simple interface hosted on Vercel
- 📝 **Fallback**: Basic summarization when API key not available

## Architecture

- **Frontend**: Static HTML/JS hosted on Vercel
- **Backend**: AWS Lambda Function
- **AI**: Mistral API for intelligent summarization
- **Extraction**: BeautifulSoup4 for HTML parsing

## Setup Instructions

### 1. Deploy Lambda Function

1. **Package Dependencies**:
```bash
pip install -r requirements.txt -t ./package
copy lambda_function.py package\
cd package
Compress-Archive -Path * -DestinationPath ..\lambda-deployment.zip
```

## How It Works

1. **User enters URL** in the web interface
2. **Lambda extracts** webpage content using BeautifulSoup4
3. **Mistral AI generates** intelligent summary with key points
4. **Results displayed** in the frontend

## API Response Format

```json
{
  "url": "https://example.com/article",
  "summary": "AI-generated summary with key points...",
  "word_count": 150,
  "from_cache": false
}
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MISTRAL_API_KEY` | Mistral API key for AI summaries | Optional (falls back to basic) |

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: AWS Lambda (Python 3.12)
- **AI**: Mistral API
- **Web Scraping**: BeautifulSoup4, Requests
- **Hosting**: Vercel (frontend)

## Testing

Test the Lambda function locally:
```python
python lambda_function.py
```

## Cost Optimization

- **Lambda**: 1M free requests/month
- **Mistral API**: Pay per token used
- **Vercel**: Free tier for static hosting

## Troubleshooting

### No Summary Generated
- Check if Mistral API key is set
- Verify the URL is accessible
- Check Lambda timeout (should be 30+ seconds)

### CORS Errors
- Ensure Function URL has CORS enabled
- Check allowed origins in Function URL settings

## License

MIT

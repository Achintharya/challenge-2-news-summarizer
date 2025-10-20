# Challenge 2: News Summarizer (AWS Lambda Backend)

## Objective

Create a serverless function that takes a news article URL as input and returns a summarized version using AWS Lambda.

## Architecture

- **Frontend**: Static HTML/JS hosted on Vercel
- **Backend**: AWS Lambda + API Gateway  
- **AI**: Mistral API for intelligent summarization
- **Cache**: Optional DynamoDB for repeated URLs
- **Extraction**: BeautifulSoup4 for HTML parsing

## Project Structure

```
challenge-2-news-summarizer/
├── lambda_function.py      # AWS Lambda handler
├── public/                 # Frontend files (Vercel)
│   └── index.html         # Web UI
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel static hosting config
├── LAMBDA_DEPLOYMENT.md   # Step-by-step Lambda setup
└── README.md
```

## Features

- Serverless news summarization using AWS Lambda
- Intelligent extraction with BeautifulSoup4
- AI-powered summaries with Mistral API
- Optional DynamoDB caching for repeated URLs
- Clean web interface hosted on Vercel
- CORS-enabled API endpoint

## Quick Start

### 1. Deploy Lambda Backend

Follow the detailed guide in [LAMBDA_DEPLOYMENT.md](./LAMBDA_DEPLOYMENT.md)

Quick steps:
1. Package Lambda function with dependencies
2. Create Lambda function in AWS Console
3. Set up API Gateway with CORS
4. Configure environment variables

### 2. Deploy Frontend to Vercel

```bash
git push origin master
```

Vercel will automatically deploy the static frontend from the `public/` directory.

### 3. Configure Frontend

When you first visit the app, it will prompt for your Lambda API Gateway URL:
```
https://your-api-id.execute-api.region.amazonaws.com/prod/summarize
```

## API Endpoint

### POST /summarize

**Request:**
```json
{
  "url": "https://www.example.com/news-article"
}
```

**Response:**
```json
{
  "url": "https://www.example.com/news-article",
  "summary": "Article summary with key points...",
  "word_count": 150,
  "from_cache": false
}
```

## Environment Variables (Lambda)

Set these in AWS Lambda Console:

| Variable | Description | Required |
|----------|-------------|----------|
| `MISTRAL_API_KEY` | Mistral API key for AI summaries | Optional |
| `AWS_REGION` | AWS region (e.g., us-east-1) | Yes |
| `DYNAMODB_TABLE` | DynamoDB table name for caching | Optional |

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: AWS Lambda (Python 3.12)
- **AI**: Mistral API
- **Extraction**: BeautifulSoup4
- **Caching**: AWS DynamoDB (optional)
- **Hosting**: Vercel (frontend only)

## How It Works

1. User enters a news article URL in the web interface
2. Frontend sends POST request to Lambda via API Gateway
3. Lambda function:
   - Checks DynamoDB cache (if configured)
   - Fetches and parses article with BeautifulSoup4
   - Generates summary using Mistral API (or fallback method)
   - Saves to cache for future requests
4. Returns formatted summary to frontend

## Testing Locally

```python
# Test Lambda function locally
python lambda_function.py
```

## Cost Optimization

- **Lambda**: 1M free requests/month
- **API Gateway**: $3.50 per million requests
- **DynamoDB**: On-demand billing, very low cost for caching
- **Vercel**: Free tier for static hosting

## Troubleshooting

### CORS Errors
- Ensure API Gateway CORS is properly configured
- Lambda must return CORS headers in response

### 500 Errors
- Check CloudWatch logs for Lambda function
- Verify environment variables are set
- Ensure Lambda has proper IAM permissions

### No Summary Generated
- Check if article URL is accessible
- Verify Mistral API key is valid
- Some sites may block automated requests

## Security Considerations

- Never commit API keys to Git
- Use environment variables in Lambda
- Configure API Gateway throttling for production
- Consider adding authentication for production use

## License

MIT

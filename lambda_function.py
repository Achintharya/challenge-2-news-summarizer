"""
AWS Lambda function for Web Scraping with Mistral AI Summarization
Uses BeautifulSoup4 for extraction and Mistral API for intelligent summarization
"""

import json
import os

def lambda_handler(event, context):
    """
    Main Lambda handler
    Accepts POST request with URL and returns AI-generated summary
    """
    try:
        # Get URL from request body
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        
        # Check if URL was provided
        if not url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'URL is required'})
            }
        
        # Extract article text
        article_text = extract_article_text(url)
        
        if not article_text:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Could not extract text from article'})
            }
        
        # Get summary using Mistral API if available, otherwise use simple method
        if os.environ.get('MISTRAL_API_KEY'):
            summary = get_mistral_summary(article_text, url)
        else:
            summary = get_simple_summary(article_text)
        
        if not summary:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Could not generate summary'})
            }
        
        # Return summary
        return {
            'statusCode': 200,
            'body': json.dumps({
                'url': url,
                'summary': summary,
                'word_count': len(summary.split()),
                'from_cache': False
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def extract_article_text(url):
    """Extract text from webpage using BeautifulSoup4"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Fetch webpage
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Try to find article content
        article_text = ""
        
        # Look for article tag first
        article = soup.find('article')
        if article:
            article_text = article.get_text()
        
        # If no article tag, look for main content
        if not article_text:
            main = soup.find('main')
            if main:
                article_text = main.get_text()
        
        # If still no content, look for common content divs
        if not article_text:
            for selector in ['.content', '#content', '.article-body', '.post-content']:
                content = soup.select_one(selector)
                if content:
                    article_text = content.get_text()
                    break
        
        # Fallback to all paragraph tags
        if not article_text:
            paragraphs = soup.find_all('p')
            article_text = ' '.join([p.get_text() for p in paragraphs])
        
        # Clean up text
        lines = (line.strip() for line in article_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        article_text = ' '.join(chunk for chunk in chunks if chunk)
        
        return article_text[:5000]  # Limit to 5000 chars
        
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None


def get_mistral_summary(article_text, url):
    """Use Mistral API to generate intelligent summary"""
    try:
        from mistralai import Mistral
        
        # Initialize Mistral client
        client = Mistral(api_key=os.environ.get('MISTRAL_API_KEY'))
        
        # Create prompt for summarization
        prompt = f"""Please provide a comprehensive summary of the following article.
        Include:
        1. A 3-4 sentence summary of the main points
        2. 3-5 key takeaways as bullet points
        
        Article URL: {url}
        
        Article Text:
        {article_text[:3000]}  # Limit text to avoid token limits
        
        Format your response as:
        Summary: [Your summary here]
        
        Key Points:
        • [Point 1]
        • [Point 2]
        • [Point 3]
        """
        
        # Get response from Mistral
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Mistral API error: {e}") 
        # Fallback to simple summary
        return get_simple_summary(article_text)


def get_simple_summary(article_text):
    """Simple text summarization without AI (fallback)"""
    try:
        # Take first 3-4 sentences
        sentences = []
        for sentence in article_text.split('.'):
            cleaned = sentence.strip()
            if len(cleaned) > 50:  # Only meaningful sentences
                sentences.append(cleaned)
            if len(sentences) >= 4:
                break
        
        if not sentences:
            return "Could not extract meaningful content from the article."
        
        summary = '. '.join(sentences) + '.'
        
        # Limit length
        if len(summary) > 600:
            summary = summary[:597] + '...'
        
        return summary
        
    except Exception as e:
        return f"Error creating summary: {str(e)}"


# For local testing
if __name__ == "__main__":
    # Test event
    test_event = {
        'body': json.dumps({
            'url': 'https://example.com/article'
        })
    }
    
    result = lambda_handler(test_event, None)
    print("Response:", json.dumps(result, indent=2))

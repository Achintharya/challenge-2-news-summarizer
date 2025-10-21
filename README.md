# Challenge 2: Web Scraper with Summary Generation

## Overview

A simple web scraping tool that extracts content from URLs and generates automatic summaries using BeautifulSoup4 for HTML parsing and basic text processing for summarization.

## Features

- 🌐 **Web Scraping**: Extract content from any webpage
- 📝 **Auto Summary**: Generate concise summaries from extracted content
- 📊 **Batch Processing**: Process multiple URLs at once
- 💾 **JSON Export**: Save results in structured JSON format
- 📑 **Source Tracking**: Maintain a markdown file with all scraped sources
- 🛡️ **Error Handling**: Graceful handling of failed requests

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Achintharya/challenge-2-news-summarizer.git
cd challenge-2-news-summarizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the Web Scraper

```bash
python web_scraper.py
```

You'll be prompted to:
1. Enter URLs manually (one per line)
2. Use example URLs
3. Enter a single URL

### Programmatic Usage

```python
from web_scraper import WebScraper

# Initialize scraper
scraper = WebScraper(output_dir="./data")

# Single URL extraction
result = scraper.extract_article_content("https://example.com/article")
summary = scraper.generate_summary(result["content"])

# Multiple URLs
urls = [
    "https://example.com/article1",
    "https://example.com/article2"
]
results = scraper.extract_multiple_urls(urls)

# Save results
scraper.save_results(results)
scraper.save_sources(urls, "My Scraping Session")
```

## Output Format

### JSON Output (`data/extracted_content.json`)
```json
[
  {
    "url": "https://example.com/article",
    "title": "Article Title",
    "content": "Full extracted content...",
    "summary": "Generated summary...",
    "extracted_at": "2024-10-21T21:00:00",
    "success": true
  }
]
```

### Sources File (`data/sources.md`)
```markdown
# Web Scraping Results

_Generated: 2024-10-21 21:00:00_

## Sources (3 URLs)

- [https://example.com/article1](https://example.com/article1)
- [https://example.com/article2](https://example.com/article2)
- [https://example.com/article3](https://example.com/article3)
```

## Project Structure

```
challenge-2-news-summarizer/
├── web_scraper.py      # Main scraper implementation
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
├── data/              # Output directory (created automatically)
│   ├── extracted_content.json
│   └── sources.md
└── test_scraper.py    # Test script (optional)
```

## How It Works

1. **Content Extraction**: 
   - Fetches HTML content from provided URLs
   - Removes scripts, styles, navigation elements
   - Extracts text from article tags, main content, or paragraphs

2. **Summary Generation**:
   - Identifies meaningful sentences (>50 characters)
   - Selects first 4 sentences as summary
   - Limits summary to 600 characters maximum

3. **Data Storage**:
   - Saves extracted content with metadata
   - Maintains source list for reference
   - Outputs in JSON format for easy processing

## Configuration

Modify the `WebScraper` class initialization to customize:

```python
scraper = WebScraper(
    output_dir="./custom_output"  # Change output directory
)
```

Adjust summary length:
```python
summary = scraper.generate_summary(text, max_sentences=6)
```

## Error Handling

The scraper handles:
- Network timeouts (10 seconds default)
- Invalid URLs
- Missing content
- Rate limiting (1-second delay between requests)

## Limitations

- Simple text-based summarization (no AI/ML)
- May not work with JavaScript-heavy sites
- Basic content extraction (may miss some dynamic content)

## Future Improvements

- [ ] Add support for RSS feeds
- [ ] Implement keyword extraction
- [ ] Add sentiment analysis
- [ ] Support for PDF and other document formats
- [ ] Multi-threading for faster batch processing
- [ ] Integration with AI summarization APIs

## License

MIT

## Author

Created as part of the Intern Assessment - Hands-On Project

# Crawl4AI Quick Start Guide

This document contains the complete Crawl4AI quick start guide for Amazon Q Developer context.

## Getting Started with Crawl4AI

Welcome to **Crawl4AI**, an open-source LLM-friendly Web Crawler & Scraper. In this tutorial, you'll:

1. Run your **first crawl** using minimal configuration.
2. Generate **Markdown** output (and learn how it's influenced by content filters).
3. Experiment with a simple **CSS-based extraction** strategy.
4. See a glimpse of **LLM-based extraction** (including open-source and closed-source model options).
5. Crawl a **dynamic** page that loads content via JavaScript.

## 1. Introduction

Crawl4AI provides:
- An asynchronous crawler, **`AsyncWebCrawler`**.
- Configurable browser and run settings via **`BrowserConfig`** and **`CrawlerRunConfig`**.
- Automatic HTML-to-Markdown conversion via **`DefaultMarkdownGenerator`** (supports optional filters).
- Multiple extraction strategies (LLM-based or "traditional" CSS/XPath-based).

## 2. Your First Crawl

Here's a minimal Python script that creates an **`AsyncWebCrawler`**, fetches a webpage, and prints the first 300 characters of its Markdown output:

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com")
        print(result.markdown[:300])  # Print first 300 chars

if __name__ == "__main__":
    asyncio.run(main())
```

**What's happening?**
- **`AsyncWebCrawler`** launches a headless browser (Chromium by default).
- It fetches `https://example.com`.
- Crawl4AI automatically converts the HTML into Markdown.

## 3. Basic Configuration

Crawl4AI's crawler can be heavily customized using two main classes:

1. **`BrowserConfig`**: Controls browser behavior (headless or full UI, user agent, JavaScript toggles, etc.).
2. **`CrawlerRunConfig`**: Controls how each crawl runs (caching, extraction, timeouts, hooking, etc.).

```python
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser_conf = BrowserConfig(headless=True)  # or False to see the browser
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS
    )
    
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url="https://example.com",
            config=run_conf
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
```

> IMPORTANT: By default cache mode is set to `CacheMode.ENABLED`. So to have fresh content, you need to set it to `CacheMode.BYPASS`

## 4. CSS-based Data Extraction

```python
import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    schema = {
        "name": "Example Items",
        "baseSelector": "div.item",
        "fields": [
            {"name": "title", "selector": "h2", "type": "text"},
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://example.com",
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(schema)
            )
        )
        data = json.loads(result.extracted_content)
        print(data)

if __name__ == "__main__":
    asyncio.run(main())
```

## 5. LLM-based Data Extraction

```python
import os
import json
import asyncio
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(..., description="Fee for output token for the OpenAI model.")

async def extract_structured_data_using_llm():
    browser_config = BrowserConfig(headless=True)
    
    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=LLMExtractionStrategy(
            llm_config=LLMConfig(provider="openai/gpt-4o", api_token=os.getenv("OPENAI_API_KEY")),
            schema=OpenAIModelFee.model_json_schema(),
            extraction_type="schema",
            instruction="Extract all mentioned model names along with their fees for input and output tokens."
        ),
    )
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://openai.com/api/pricing/", 
            config=crawler_config
        )
        print(result.extracted_content)

if __name__ == "__main__":
    asyncio.run(extract_structured_data_using_llm())
```

## 6. Multi-URL Concurrency

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def quick_parallel_example():
    urls = [
        "https://example.com/page1",
        "https://example.com/page2", 
        "https://example.com/page3"
    ]
    
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        stream=True  # Enable streaming mode
    )
    
    async with AsyncWebCrawler() as crawler:
        # Stream results as they complete
        async for result in await crawler.arun_many(urls, config=run_conf):
            if result.success:
                print(f"[OK] {result.url}, length: {len(result.markdown.raw_markdown)}")
            else:
                print(f"[ERROR] {result.url} => {result.error_message}")

if __name__ == "__main__":
    asyncio.run(quick_parallel_example())
```

## Key Features Summary

- **Asynchronous crawling** with `AsyncWebCrawler`
- **Configurable browser settings** with `BrowserConfig`
- **Flexible run configurations** with `CrawlerRunConfig`
- **Multiple extraction strategies**: CSS-based and LLM-based
- **Concurrent crawling** with `arun_many()`
- **Dynamic content handling** with JavaScript execution
- **Caching support** for improved performance
- **Markdown generation** with content filtering options

This guide provides the foundation for using Crawl4AI effectively in your web scraping and data extraction projects.

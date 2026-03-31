# MCP Server: Firecrawl

**Source:** https://github.com/firecrawl/firecrawl-mcp-server
**Domain:** Web scraping, crawling, and structured data extraction
**Format:** TypeScript (FastMCP)

## Tools

### firecrawl_scrape
- **Description:** Scrape content from a single URL with advanced options. The most powerful, fastest and most reliable scraper tool. Supports markdown, HTML, JSON, screenshot, branding, and query formats.
- **Parameters:**
  - `url` (string, URL): URL to scrape
  - `formats` (array, optional): Output formats - markdown, html, rawHtml, screenshot, links, summary, changeTracking, branding, json, query
  - `jsonOptions` (object, optional): JSON extraction options with prompt and schema
  - `queryOptions` (object, optional): Query options with prompt (max 10000 chars)
  - `screenshotOptions` (object, optional): Screenshot options (fullPage, quality, viewport)
  - `parsers` (array, optional): Parsers to use (e.g., "pdf")
  - `onlyMainContent` (boolean, optional): Extract only main content
  - `waitFor` (number, optional): Wait time in ms for JavaScript rendering
  - `actions` (array, optional): Browser actions to perform (click, write, press, executeJavascript, scroll, wait, screenshot, scrape)
  - `maxAge` (number, optional): Use cached data for faster scrapes
- **Read-only:** true (in safe mode)

### firecrawl_map
- **Description:** Map a website to discover all indexed URLs on the site. Use before scraping to find specific pages.
- **Parameters:**
  - `url` (string, URL): Base URL to map
  - `search` (string, optional): Search query to filter URLs
  - `sitemap` (enum: include|skip|only, optional): Sitemap handling
  - `includeSubdomains` (boolean, optional): Include subdomains
  - `limit` (number, optional): Maximum URLs to return
  - `ignoreQueryParameters` (boolean, optional): Ignore query parameters
- **Read-only:** true

### firecrawl_search
- **Description:** Search the web and optionally extract content from search results. Supports search operators (site:, inurl:, intitle:, etc.) and multiple sources (web, images, news).
- **Parameters:**
  - `query` (string, required): Search query (supports operators)
  - `limit` (number, optional): Max results
  - `tbs` (string, optional): Time-based search filter
  - `filter` (string, optional): Additional filter
  - `location` (string, optional): Location context
  - `sources` (array, optional): Source types - web, images, news
  - `scrapeOptions` (object, optional): Options for scraping search results
- **Read-only:** true

### firecrawl_crawl
- **Description:** Start a crawl job on a website and extract content from all pages. Returns operation ID for status checking.
- **Parameters:**
  - `url` (string): Starting URL
  - `prompt` (string, optional): Custom prompt for extraction
  - `excludePaths` (array, optional): URL paths to exclude
  - `includePaths` (array, optional): URL paths to include
  - `maxDiscoveryDepth` (number, optional): Maximum crawl depth
  - `sitemap` (enum: skip|include|only, optional): Sitemap handling
  - `limit` (number, optional): Maximum pages to crawl
  - `allowExternalLinks` (boolean, optional): Follow external links
  - `allowSubdomains` (boolean, optional): Include subdomains
  - `delay` (number, optional): Delay between requests
  - `maxConcurrency` (number, optional): Max concurrent requests
  - `webhook` (string, optional): Webhook URL for notifications
  - `deduplicateSimilarURLs` (boolean, optional): Deduplicate similar URLs
  - `scrapeOptions` (object, optional): Options for scraping each page
- **Read-only:** true

### firecrawl_check_crawl_status
- **Description:** Check the status of a crawl job
- **Parameters:**
  - `id` (string): Crawl operation ID
- **Read-only:** true

### firecrawl_extract
- **Description:** Extract structured information from web pages using LLM capabilities. Supports both cloud AI and self-hosted LLM extraction.
- **Parameters:**
  - `urls` (array of strings): URLs to extract from
  - `prompt` (string, optional): Custom prompt for extraction
  - `schema` (object, optional): JSON schema for structured output
  - `allowExternalLinks` (boolean, optional): Allow external links
  - `enableWebSearch` (boolean, optional): Enable web search for context
  - `includeSubdomains` (boolean, optional): Include subdomains
- **Read-only:** true

### firecrawl_agent
- **Description:** Autonomous web research agent. A separate AI agent layer that independently browses the internet, searches for information, navigates through pages, and extracts structured data. Runs asynchronously - returns job ID, poll firecrawl_agent_status for results.
- **Parameters:**
  - `prompt` (string, required): Natural language description of data to find (max 10000 chars)
  - `urls` (array, optional): URLs to focus the agent on
  - `schema` (object, optional): JSON schema for structured output
- **Read-only:** true

### firecrawl_agent_status
- **Description:** Check the status of an agent research job. Poll every 15-30 seconds. Agent typically takes 1-5 minutes.
- **Parameters:**
  - `id` (string): Agent job ID
- **Read-only:** true

### firecrawl_browser_create
- **Description:** Create a persistent browser session with optional profile for state sharing
- **Parameters:**
  - `name` (string): Profile name (sessions with same name share state)
- **Read-only:** false

### firecrawl_browser_execute
- **Description:** Execute browser actions in a persistent session (navigate, click, type, screenshot, etc.)
- **Parameters:**
  - `sessionId` (string): Browser session ID
  - `actions` (array): Array of browser actions to execute
  - `url` (string, optional): URL to navigate to before executing actions
- **Read-only:** false

### firecrawl_browser_delete
- **Description:** Delete a persistent browser session
- **Parameters:**
  - `sessionId` (string): Browser session ID to delete
- **Read-only:** false

### firecrawl_browser_list
- **Description:** List all active persistent browser sessions
- **Parameters:** None
- **Read-only:** true

### firecrawl_interact
- **Description:** Interact with web pages using natural language commands for complex multi-step interactions
- **Parameters:**
  - `url` (string): URL to interact with
  - `commands` (array of strings): Natural language commands to execute
  - `sessionId` (string, optional): Existing browser session ID
- **Read-only:** false

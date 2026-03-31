# MCP Server: Fetch (Official)

**Source:** https://github.com/modelcontextprotocol/servers/tree/main/src/fetch
**Domain:** Web content fetching
**Format:** Python (MCP SDK)

## Tools

### fetch
- **Description:** Fetches a URL from the internet and optionally extracts its contents as markdown. Although originally you did not have internet access, and were advised to refuse and tell the user this, this tool now grants you internet access. Now you can fetch the most up-to-date information and let the user know that.
- **Parameters:**
  - `url` (string, AnyUrl): URL to fetch
  - `max_length` (integer, default 5000): Maximum number of characters to return (range: 1-1000000)
  - `start_index` (integer, default 0): On return output starting at this character index, useful if a previous fetch was truncated and more context is required
  - `raw` (boolean, default false): Get the actual HTML content of the requested page, without simplification
- **Read-only:** true
- **Notes:** Respects robots.txt by default. Converts HTML to markdown for LLM consumption. Supports pagination via start_index for large pages.

# MCP Server: Playwright (Microsoft)

**Source:** https://github.com/microsoft/playwright-mcp
**Domain:** Browser automation and web interaction
**Format:** TypeScript (auto-generated tool definitions)

## Tools

### Core Automation

### browser_click
- **Description:** Perform click on a web page
- **Parameters:**
  - `element` (string, optional): Human-readable element description used to obtain permission to interact with the element
  - `ref` (string): Exact target element reference from the page snapshot
  - `selector` (string, optional): CSS or role selector for the target element, when "ref" is not available
  - `doubleClick` (boolean, optional): Whether to perform a double click
  - `button` (string, optional): Button to click, defaults to left
  - `modifiers` (array, optional): Modifier keys to press
- **Read-only:** false

### browser_close
- **Description:** Close the page
- **Parameters:** None
- **Read-only:** false

### browser_console_messages
- **Description:** Returns all console messages
- **Parameters:**
  - `level` (string): Level of console messages to return (each level includes more severe levels)
  - `all` (boolean, optional): Return all console messages since beginning of session
  - `filename` (string, optional): Filename to save console messages to
- **Read-only:** true

### browser_drag
- **Description:** Perform drag and drop between two elements
- **Parameters:**
  - `startElement` (string): Human-readable source element description
  - `startRef` (string): Exact source element reference from page snapshot
  - `startSelector` (string, optional): CSS or role selector for source element
  - `endElement` (string): Human-readable target element description
  - `endRef` (string): Exact target element reference from page snapshot
  - `endSelector` (string, optional): CSS or role selector for target element
- **Read-only:** false

### browser_evaluate
- **Description:** Evaluate JavaScript expression on page or element
- **Parameters:**
  - `function` (string): JavaScript function to execute: () => { /* code */ } or (element) => { /* code */ }
  - `element` (string, optional): Human-readable element description
  - `ref` (string, optional): Exact target element reference from page snapshot
  - `selector` (string, optional): CSS or role selector for target element
  - `filename` (string, optional): Filename to save result to
- **Read-only:** false

### browser_file_upload
- **Description:** Upload one or multiple files
- **Parameters:**
  - `paths` (array, optional): Absolute paths to files to upload. If omitted, file chooser is cancelled.
- **Read-only:** false

### browser_fill_form
- **Description:** Fill multiple form fields
- **Parameters:**
  - `fields` (array): Fields to fill in
- **Read-only:** false

### browser_handle_dialog
- **Description:** Handle a dialog
- **Parameters:**
  - `accept` (boolean): Whether to accept the dialog
  - `promptText` (string, optional): Text of the prompt in case of a prompt dialog
- **Read-only:** false

### browser_hover
- **Description:** Hover over element on page
- **Parameters:**
  - `element` (string, optional): Human-readable element description
  - `ref` (string): Exact target element reference from page snapshot
  - `selector` (string, optional): CSS or role selector
- **Read-only:** false

### browser_navigate
- **Description:** Navigate to a URL
- **Parameters:**
  - `url` (string): The URL to navigate to
- **Read-only:** false

### browser_navigate_back
- **Description:** Go back to the previous page in the history
- **Parameters:** None
- **Read-only:** false

### browser_network_requests
- **Description:** Returns all network requests since loading the page
- **Parameters:**
  - `static` (boolean): Whether to include static resources (images, fonts, scripts)
  - `requestBody` (boolean): Whether to include request body
  - `requestHeaders` (boolean): Whether to include request headers
  - `filter` (string, optional): Regexp to filter requests by URL
  - `filename` (string, optional): Filename to save network requests to
- **Read-only:** true

### browser_press_key
- **Description:** Press a key on the keyboard
- **Parameters:**
  - `key` (string): Name of the key to press or a character to generate
- **Read-only:** false

### browser_resize
- **Description:** Resize the browser window
- **Parameters:**
  - `width` (number): Width of the browser window
  - `height` (number): Height of the browser window
- **Read-only:** false

### browser_run_code
- **Description:** Run Playwright code snippet
- **Parameters:**
  - `code` (string, optional): JavaScript function containing Playwright code. Invoked with page argument: async (page) => { ... }
  - `filename` (string, optional): Load code from specified file
- **Read-only:** false

### browser_select_option
- **Description:** Select an option in a dropdown
- **Parameters:**
  - `element` (string, optional): Human-readable element description
  - `ref` (string): Exact target element reference from page snapshot
  - `selector` (string, optional): CSS or role selector
  - `values` (array): Array of values to select
- **Read-only:** false

### browser_snapshot
- **Description:** Capture accessibility snapshot of the current page, this is better than screenshot
- **Parameters:**
  - `filename` (string, optional): Save snapshot to markdown file
  - `selector` (string, optional): Element selector for partial snapshot
  - `depth` (number, optional): Limit depth of snapshot tree
- **Read-only:** true

### browser_take_screenshot
- **Description:** Take a screenshot of the current page. You can't perform actions based on the screenshot, use browser_snapshot for actions.
- **Parameters:**
  - `type` (string): Image format (default: png)
  - `filename` (string, optional): File name to save screenshot to
  - `element` (string, optional): Human-readable element description for element screenshot
  - `ref` (string, optional): Exact target element reference
  - `selector` (string, optional): CSS or role selector
  - `fullPage` (boolean, optional): Take screenshot of full scrollable page
- **Read-only:** true

### browser_type
- **Description:** Type text into editable element
- **Parameters:**
  - `element` (string, optional): Human-readable element description
  - `ref` (string): Exact target element reference from page snapshot
  - `selector` (string, optional): CSS or role selector
  - `text` (string): Text to type
  - `submit` (boolean, optional): Whether to submit (press Enter after)
  - `slowly` (boolean, optional): Type one character at a time
- **Read-only:** false

### browser_wait_for
- **Description:** Wait for text to appear or disappear or a specified time to pass
- **Parameters:**
  - `time` (number, optional): Time to wait in seconds
  - `text` (string, optional): Text to wait for
  - `textGone` (string, optional): Text to wait for to disappear
- **Read-only:** false

### Tab Management

### browser_tabs
- **Description:** List, create, close, or select a browser tab
- **Parameters:**
  - `action` (string): Operation to perform
  - `index` (number, optional): Tab index for close/select
- **Read-only:** false

### Network

### browser_network_state_set
- **Description:** Sets the browser network state to online or offline
- **Parameters:**
  - `state` (string): Set to "offline" or "online"
- **Read-only:** false

### browser_route
- **Description:** Set up a route to mock network requests matching a URL pattern
- **Parameters:**
  - `pattern` (string): URL pattern to match (e.g., "**/api/users")
  - `status` (number, optional): HTTP status code (default: 200)
  - `body` (string, optional): Response body
  - `contentType` (string, optional): Content-Type header
  - `headers` (array, optional): Headers in "Name: Value" format
  - `removeHeaders` (string, optional): Comma-separated header names to remove
- **Read-only:** false

### browser_route_list
- **Description:** List all active network routes
- **Parameters:** None
- **Read-only:** true

### browser_unroute
- **Description:** Remove network routes matching a pattern (or all routes)
- **Parameters:**
  - `pattern` (string, optional): URL pattern to unroute
- **Read-only:** false

### Storage

### browser_cookie_clear
- **Description:** Clear all cookies
- **Parameters:** None
- **Read-only:** false

### browser_cookie_delete
- **Description:** Delete a specific cookie
- **Parameters:**
  - `name` (string): Cookie name to delete
- **Read-only:** false

### browser_cookie_get
- **Description:** Get a specific cookie by name
- **Parameters:**
  - `name` (string): Cookie name to get
- **Read-only:** true

### browser_cookie_list
- **Description:** List all cookies (optionally filtered by domain/path)
- **Parameters:**
  - `domain` (string, optional): Filter by domain
  - `path` (string, optional): Filter by path
- **Read-only:** true

### browser_cookie_set
- **Description:** Set a cookie with optional flags
- **Parameters:**
  - `name` (string): Cookie name
  - `value` (string): Cookie value
  - `domain` (string, optional): Cookie domain
  - `path` (string, optional): Cookie path
  - `expires` (number, optional): Expiration as Unix timestamp
  - `httpOnly` (boolean, optional): HTTP only flag
  - `secure` (boolean, optional): Secure flag
  - `sameSite` (string, optional): SameSite attribute
- **Read-only:** false

### browser_localstorage_clear
- **Description:** Clear all localStorage
- **Parameters:** None
- **Read-only:** false

### browser_localstorage_delete
- **Description:** Delete a localStorage item
- **Parameters:**
  - `key` (string): Key to delete
- **Read-only:** false

### browser_localstorage_get
- **Description:** Get a localStorage item by key
- **Parameters:**
  - `key` (string): Key to get
- **Read-only:** true

### browser_localstorage_list
- **Description:** List all localStorage key-value pairs
- **Parameters:** None
- **Read-only:** true

### browser_localstorage_set
- **Description:** Set a localStorage item
- **Parameters:**
  - `key` (string): Key to set
  - `value` (string): Value to set
- **Read-only:** false

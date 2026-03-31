# MCP Server: GhidraMCP

**Source:** https://github.com/LaurieWired/GhidraMCP
**Domain:** Reverse engineering / binary analysis (via Ghidra)
**Format:** Python (FastMCP, bridges to Ghidra REST API)

## Tools

### list_methods
- **Description:** List all function names in the program with pagination
- **Parameters:**
  - `offset` (integer, default 0): Starting offset for pagination
  - `limit` (integer, default 100): Maximum number of results
- **Read-only:** true

### list_classes
- **Description:** List all namespace/class names in the program with pagination
- **Parameters:**
  - `offset` (integer, default 0): Starting offset for pagination
  - `limit` (integer, default 100): Maximum number of results
- **Read-only:** true

### decompile_function
- **Description:** Decompile a specific function by name and return the decompiled C code
- **Parameters:**
  - `name` (string): Function name to decompile
- **Read-only:** true

### rename_function
- **Description:** Rename a function in the program
- **Parameters:**
  - `old_name` (string): Current function name
  - `new_name` (string): New function name
- **Read-only:** false

### rename_data
- **Description:** Rename a data label in the program
- **Parameters:**
  - `old_name` (string): Current data label name
  - `new_name` (string): New data label name
- **Read-only:** false

### list_segments
- **Description:** List all memory segments/sections in the program
- **Parameters:** None
- **Read-only:** true

### list_imports
- **Description:** List all imported functions/symbols in the program
- **Parameters:** None
- **Read-only:** true

### list_exports
- **Description:** List all exported functions/symbols in the program
- **Parameters:** None
- **Read-only:** true

### list_namespaces
- **Description:** List all namespaces in the program
- **Parameters:** None
- **Read-only:** true

### list_data_items
- **Description:** List all defined data items in the program with pagination
- **Parameters:**
  - `offset` (integer, default 0): Starting offset
  - `limit` (integer, default 100): Maximum results
- **Read-only:** true

### get_function_by_address
- **Description:** Get function information by memory address
- **Parameters:**
  - `address` (string): Memory address (hex format)
- **Read-only:** true

### search_functions_by_name
- **Description:** Search for functions matching a name pattern
- **Parameters:**
  - `query` (string): Search pattern
- **Read-only:** true

### list_strings
- **Description:** List all defined strings in the program with pagination
- **Parameters:**
  - `offset` (integer, default 0): Starting offset
  - `limit` (integer, default 100): Maximum results
- **Read-only:** true

### search_strings
- **Description:** Search for strings matching a pattern in the program
- **Parameters:**
  - `query` (string): Search pattern to match
- **Read-only:** true

### get_cross_references
- **Description:** Get all cross-references (xrefs) to or from a given address
- **Parameters:**
  - `address` (string): Memory address to find references for
- **Read-only:** true

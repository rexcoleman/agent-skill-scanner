# MCP Server: Filesystem (Official)

**Source:** https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
**Domain:** File system operations
**Format:** TypeScript (MCP SDK)

## Tools

### read_file (deprecated)
- **Description:** Read the complete contents of a file as text. DEPRECATED: Use read_text_file instead.
- **Parameters:**
  - `path` (string): File path to read
  - `tail` (number, optional): If provided, returns only the last N lines of the file
  - `head` (number, optional): If provided, returns only the first N lines of the file
- **Read-only:** true

### read_text_file
- **Description:** Read the complete contents of a file from the file system as text. Handles various text encodings and provides detailed error messages if the file cannot be read. Use the 'head' parameter to read only the first N lines of a file, or the 'tail' parameter to read only the last N lines. Only works within allowed directories.
- **Parameters:**
  - `path` (string): File path to read
  - `tail` (number, optional): If provided, returns only the last N lines of the file
  - `head` (number, optional): If provided, returns only the first N lines of the file
- **Read-only:** true

### read_media_file
- **Description:** Read an image or audio file. Returns the base64 encoded data and MIME type. Only works within allowed directories.
- **Parameters:**
  - `path` (string): File path to read
- **Read-only:** true

### read_multiple_files
- **Description:** Read the contents of multiple files simultaneously. More efficient than reading files one by one when you need to analyze or compare multiple files. Each file's content is returned with its path as a reference. Failed reads for individual files won't stop the entire operation. Only works within allowed directories.
- **Parameters:**
  - `paths` (array of strings): Array of file paths to read
- **Read-only:** true

### write_file
- **Description:** Create a new file or completely overwrite an existing file with new content. Use with caution as it will overwrite existing files without warning. Handles text content with proper encoding. Only works within allowed directories.
- **Parameters:**
  - `path` (string): File path to write
  - `content` (string): Content to write
- **Read-only:** false
- **Destructive:** true

### edit_file
- **Description:** Make line-based edits to a text file. Each edit replaces exact line sequences with new content. Returns a git-style diff showing the changes made. Only works within allowed directories.
- **Parameters:**
  - `path` (string): File path to edit
  - `edits` (array): Array of {oldText, newText} replacements
  - `dryRun` (boolean, default false): Preview changes using git-style diff format
- **Read-only:** false
- **Destructive:** true

### create_directory
- **Description:** Create a new directory or ensure a directory exists. Can create multiple nested directories in one operation. If the directory already exists, this operation will succeed silently. Only works within allowed directories.
- **Parameters:**
  - `path` (string): Directory path to create
- **Read-only:** false

### list_directory
- **Description:** Get a detailed listing of all files and directories in a specified path. Results clearly distinguish between files and directories with [FILE] and [DIR] prefixes. Only works within allowed directories.
- **Parameters:**
  - `path` (string): Directory path to list
- **Read-only:** true

### list_directory_with_sizes
- **Description:** Get a detailed listing of all files and directories in a specified path, including sizes. Only works within allowed directories.
- **Parameters:**
  - `path` (string): Directory path to list
  - `sortBy` (enum: name|size, optional): Sort entries by name or size
- **Read-only:** true

### directory_tree
- **Description:** Get a recursive tree view of files and directories as a JSON structure. Each entry includes 'name', 'type' (file/directory), and 'children' for directories. Only works within allowed directories.
- **Parameters:**
  - `path` (string): Root path for tree
  - `excludePatterns` (array of strings, optional): Glob patterns to exclude
- **Read-only:** true

### move_file
- **Description:** Move or rename files and directories. Can move files between directories and rename them in a single operation. If the destination exists, the operation will fail. Both source and destination must be within allowed directories.
- **Parameters:**
  - `source` (string): Source path
  - `destination` (string): Destination path
- **Read-only:** false
- **Destructive:** true

### search_files
- **Description:** Recursively search for files and directories matching a pattern. The patterns should be glob-style patterns. Use '*.ext' for current directory, '**/*.ext' for all subdirectories. Only searches within allowed directories.
- **Parameters:**
  - `path` (string): Root search path
  - `pattern` (string): Glob pattern to match
  - `excludePatterns` (array of strings, optional): Patterns to exclude
- **Read-only:** true

### get_file_info
- **Description:** Retrieve detailed metadata about a file or directory. Returns comprehensive information including size, creation time, last modified time, permissions, and type. Only works within allowed directories.
- **Parameters:**
  - `path` (string): File or directory path
- **Read-only:** true

### list_allowed_directories
- **Description:** Returns the list of directories that this server is allowed to access. Subdirectories within these allowed directories are also accessible.
- **Parameters:** None
- **Read-only:** true

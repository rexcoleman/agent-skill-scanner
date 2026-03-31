# MCP Server: Git (Official)

**Source:** https://github.com/modelcontextprotocol/servers/tree/main/src/git
**Domain:** Git version control operations
**Format:** Python (MCP SDK)

## Tools

### git_status
- **Description:** Shows the working tree status
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
- **Read-only:** true

### git_diff_unstaged
- **Description:** Shows changes in the working directory that are not yet staged
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
  - `context_lines` (integer, default 3): Number of context lines in diff
- **Read-only:** true

### git_diff_staged
- **Description:** Shows changes that are staged for commit
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
  - `context_lines` (integer, default 3): Number of context lines in diff
- **Read-only:** true

### git_diff
- **Description:** Shows differences between branches or commits
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
  - `target` (string): Branch or commit to diff against
  - `context_lines` (integer, default 3): Number of context lines in diff
- **Read-only:** true
- **Notes:** Validates target is a real git ref. Rejects targets starting with '-' to prevent flag injection.

### git_commit
- **Description:** Records changes to the repository
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
  - `message` (string): Commit message
- **Read-only:** false

### git_add
- **Description:** Adds file contents to the staging area
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
  - `files` (array of strings): List of file paths to stage
- **Read-only:** false

### git_reset
- **Description:** Unstages all staged changes
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
- **Read-only:** false
- **Destructive:** true

### git_log
- **Description:** Shows the commit logs
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
  - `max_count` (integer, default 10): Maximum number of commits to show
  - `start_timestamp` (string, optional): Start timestamp for filtering (ISO 8601, relative dates, or absolute dates)
  - `end_timestamp` (string, optional): End timestamp for filtering
- **Read-only:** true

### git_create_branch
- **Description:** Creates a new branch from an optional base branch
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
  - `branch_name` (string): Name for the new branch
  - `base_branch` (string, optional): Base branch to create from
- **Read-only:** false

### git_checkout
- **Description:** Switches branches
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
  - `branch_name` (string): Branch to switch to
- **Read-only:** false
- **Notes:** Validates branch_name is a real git ref. Rejects names starting with '-' to prevent flag injection.

### git_show
- **Description:** Shows the contents of a commit
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
  - `revision` (string): Commit hash or revision to show
- **Read-only:** true

### git_branch
- **Description:** List Git branches
- **Parameters:**
  - `repo_path` (string): Path to the Git repository
  - `branch_type` (string): Whether to list 'local', 'remote', or 'all' branches
  - `contains` (string, optional): Commit SHA that branches should contain
  - `not_contains` (string, optional): Commit SHA that branches should NOT contain
- **Read-only:** true

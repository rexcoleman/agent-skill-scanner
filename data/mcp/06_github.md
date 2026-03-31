# MCP Server: GitHub (Official GitHub MCP Server)

**Source:** https://github.com/github/github-mcp-server
**Domain:** GitHub API operations (issues, PRs, repos, security)
**Format:** Go (tool snapshots)

## Tools

### create_or_update_file
- **Description:** Create or update a single file in a GitHub repository
- **Parameters:**
  - `owner` (string): Repository owner
  - `repo` (string): Repository name
  - `path` (string): File path within the repository
  - `content` (string): File content (will be base64 encoded)
  - `message` (string): Commit message
  - `branch` (string): Branch name
  - `sha` (string, optional): SHA of the file being replaced (required for updates)
- **Read-only:** false
- **Destructive:** true

### get_file_contents
- **Description:** Get the contents of a file or directory from a GitHub repository
- **Parameters:**
  - `owner` (string): Repository owner
  - `repo` (string): Repository name
  - `path` (string): File path
  - `branch` (string, optional): Branch name
- **Read-only:** true

### create_issue
- **Description:** Create a new issue in a GitHub repository
- **Parameters:**
  - `owner` (string): Repository owner
  - `repo` (string): Repository name
  - `title` (string): Issue title
  - `body` (string, optional): Issue body content
  - `assignees` (array of strings, optional): GitHub usernames to assign
  - `labels` (array of strings, optional): Labels to apply
  - `milestone` (integer, optional): Milestone number
- **Read-only:** false

### create_pull_request
- **Description:** Create a new pull request in a GitHub repository
- **Parameters:**
  - `owner` (string): Repository owner
  - `repo` (string): Repository name
  - `title` (string): PR title
  - `body` (string, optional): PR description
  - `head` (string): Branch containing changes
  - `base` (string): Branch to merge into
  - `draft` (boolean, optional): Create as draft PR
  - `maintainer_can_modify` (boolean, optional): Allow maintainer edits
- **Read-only:** false

### get_secret_scanning_alert
- **Description:** Get details of a secret scanning alert in a GitHub repository
- **Parameters:**
  - `owner` (string): Repository owner
  - `repo` (string): Repository name
  - `alertNumber` (integer): Alert number
- **Read-only:** true

### list_code_scanning_alerts
- **Description:** List code scanning alerts for a repository
- **Parameters:**
  - `owner` (string): Repository owner
  - `repo` (string): Repository name
  - `ref` (string, optional): Git reference
  - `state` (string, optional): Filter by state (open, closed, dismissed, fixed)
  - `severity` (string, optional): Filter by severity
- **Read-only:** true

### create_repository
- **Description:** Create a new GitHub repository
- **Parameters:**
  - `name` (string): Repository name
  - `description` (string, optional): Repository description
  - `private` (boolean, optional): Whether the repository is private
  - `autoInit` (boolean, optional): Initialize with a README
- **Read-only:** false

### fork_repository
- **Description:** Fork a GitHub repository to your account or specified organization
- **Parameters:**
  - `owner` (string): Repository owner
  - `repo` (string): Repository name
  - `organization` (string, optional): Organization to fork to
- **Read-only:** false

### list_issues
- **Description:** List and filter issues in a GitHub repository
- **Parameters:**
  - `owner` (string): Repository owner
  - `repo` (string): Repository name
  - `state` (string, optional): Filter by state (open, closed, all)
  - `labels` (array of strings, optional): Filter by labels
  - `sort` (string, optional): Sort by (created, updated, comments)
  - `direction` (string, optional): Sort direction (asc, desc)
  - `per_page` (integer, optional): Results per page
  - `page` (integer, optional): Page number
- **Read-only:** true

### list_pull_requests
- **Description:** List and filter pull requests in a GitHub repository
- **Parameters:**
  - `owner` (string): Repository owner
  - `repo` (string): Repository name
  - `state` (string, optional): Filter by state
  - `sort` (string, optional): Sort field
  - `direction` (string, optional): Sort direction
  - `per_page` (integer, optional): Results per page
  - `page` (integer, optional): Page number
- **Read-only:** true

### get_global_security_advisory
- **Description:** Get a global security advisory by its GHSA ID
- **Parameters:**
  - `ghsa_id` (string): The GHSA (GitHub Security Advisory) identifier
- **Read-only:** true

### list_global_security_advisories
- **Description:** List global security advisories with optional filters
- **Parameters:**
  - `ghsa_id` (string, optional): Filter by GHSA ID
  - `type` (string, optional): Filter by type (reviewed, unreviewed, malware)
  - `cve_id` (string, optional): Filter by CVE ID
  - `ecosystem` (string, optional): Filter by package ecosystem
  - `severity` (string, optional): Filter by severity (low, medium, high, critical)
  - `per_page` (integer, optional): Results per page
- **Read-only:** true

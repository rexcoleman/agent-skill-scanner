# MCP Server: Memory (Official)

**Source:** https://github.com/modelcontextprotocol/servers/tree/main/src/memory
**Domain:** Knowledge graph / persistent memory
**Format:** TypeScript (MCP SDK)

## Tools

### create_entities
- **Description:** Create multiple new entities in the knowledge graph
- **Parameters:**
  - `entities` (array): Array of entity objects, each with:
    - `name` (string): The name of the entity
    - `entityType` (string): The type of the entity
    - `observations` (array of strings): Observation contents associated with the entity
- **Read-only:** false

### create_relations
- **Description:** Create multiple new relations between entities in the knowledge graph. Relations should be in active voice.
- **Parameters:**
  - `relations` (array): Array of relation objects, each with:
    - `from` (string): The name of the entity where the relation starts
    - `to` (string): The name of the entity where the relation ends
    - `relationType` (string): The type of the relation
- **Read-only:** false

### add_observations
- **Description:** Add new observations to existing entities in the knowledge graph
- **Parameters:**
  - `observations` (array): Array of objects, each with:
    - `entityName` (string): The name of the entity to add observations to
    - `contents` (array of strings): Observation contents to add
- **Read-only:** false

### delete_entities
- **Description:** Delete multiple entities and their associated relations from the knowledge graph
- **Parameters:**
  - `entityNames` (array of strings): Entity names to delete
- **Read-only:** false
- **Destructive:** true

### delete_observations
- **Description:** Delete specific observations from entities in the knowledge graph
- **Parameters:**
  - `deletions` (array): Array of objects, each with:
    - `entityName` (string): Entity containing the observations
    - `observations` (array of strings): Observations to delete
- **Read-only:** false
- **Destructive:** true

### delete_relations
- **Description:** Delete multiple relations from the knowledge graph
- **Parameters:**
  - `relations` (array): Array of relation objects to delete (from, to, relationType)
- **Read-only:** false
- **Destructive:** true

### read_graph
- **Description:** Read the entire knowledge graph
- **Parameters:** None
- **Read-only:** true

### search_nodes
- **Description:** Search for nodes in the knowledge graph based on a query
- **Parameters:**
  - `query` (string): Search query to match against entity names, types, and observation content
- **Read-only:** true

### open_nodes
- **Description:** Open specific nodes in the knowledge graph by their names
- **Parameters:**
  - `names` (array of strings): Entity names to retrieve
- **Read-only:** true

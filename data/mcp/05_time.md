# MCP Server: Time (Official)

**Source:** https://github.com/modelcontextprotocol/servers/tree/main/src/time
**Domain:** Time and timezone operations
**Format:** Python (MCP SDK)

## Tools

### get_current_time
- **Description:** Get current time in a specific timezone
- **Parameters:**
  - `timezone` (string, required): IANA timezone name (e.g., 'America/New_York', 'Europe/London')
- **Read-only:** true
- **Returns:** TimeResult with timezone, datetime (ISO), day_of_week, is_dst

### convert_time
- **Description:** Convert time between timezones
- **Parameters:**
  - `source_timezone` (string, required): Source IANA timezone name
  - `time` (string, required): Time to convert in 24-hour format (HH:MM)
  - `target_timezone` (string, required): Target IANA timezone name
- **Read-only:** true
- **Returns:** TimeConversionResult with source, target (TimeResult), and time_difference

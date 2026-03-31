# MCP Server: AWS SNS/SQS (Amazon)

**Source:** https://github.com/awslabs/mcp/tree/main/src/amazon-sns-sqs-mcp-server
**Domain:** Cloud messaging (Amazon SNS topics/subscriptions and SQS queues)
**Format:** Python (FastMCP with boto3)

## Server Configuration
- **Instructions:** Manage Amazon SNS topics, subscriptions, and Amazon SQS queues for messaging.
- **Flag:** `--allow-resource-creation` enables tools that create resources on user AWS account

## SNS Tools

### sns_list_topics
- **Description:** List all SNS topics in the configured AWS account/region
- **Parameters:** None
- **Read-only:** true

### sns_get_topic_attributes
- **Description:** Get attributes of a specific SNS topic
- **Parameters:**
  - `topic_arn` (string): ARN of the SNS topic
- **Read-only:** true

### sns_list_subscriptions
- **Description:** List subscriptions for a specific SNS topic
- **Parameters:**
  - `topic_arn` (string): ARN of the SNS topic
- **Read-only:** true

### sns_get_subscription_attributes
- **Description:** Get attributes of a specific SNS subscription
- **Parameters:**
  - `subscription_arn` (string): ARN of the subscription
- **Read-only:** true

### sns_publish
- **Description:** Publish a message to an SNS topic
- **Parameters:**
  - `topic_arn` (string): ARN of the SNS topic
  - `message` (string): Message body to publish
  - `subject` (string, optional): Subject for email subscriptions
  - `message_attributes` (object, optional): Message attributes
- **Read-only:** false

### sns_create_topic
- **Description:** Create a new SNS topic (requires --allow-resource-creation flag)
- **Parameters:**
  - `name` (string): Topic name
  - `attributes` (object, optional): Topic attributes
  - `tags` (array, optional): Tags for the topic
- **Read-only:** false
- **Gated:** Only available with --allow-resource-creation

### sns_subscribe
- **Description:** Subscribe an endpoint to an SNS topic (requires --allow-resource-creation flag)
- **Parameters:**
  - `topic_arn` (string): ARN of the SNS topic
  - `protocol` (string): Subscription protocol (email, sqs, lambda, http, https, sms)
  - `endpoint` (string): Endpoint to receive notifications
  - `attributes` (object, optional): Subscription attributes
- **Read-only:** false
- **Gated:** Only available with --allow-resource-creation

## SQS Tools

### sqs_list_queues
- **Description:** List all SQS queues in the configured AWS account/region
- **Parameters:**
  - `queue_name_prefix` (string, optional): Filter queues by name prefix
- **Read-only:** true

### sqs_get_queue_attributes
- **Description:** Get attributes of a specific SQS queue
- **Parameters:**
  - `queue_url` (string): URL of the SQS queue
- **Read-only:** true

### sqs_send_message
- **Description:** Send a message to an SQS queue
- **Parameters:**
  - `queue_url` (string): URL of the SQS queue
  - `message_body` (string): Message body
  - `delay_seconds` (integer, optional): Delay before message becomes visible
  - `message_attributes` (object, optional): Message attributes
- **Read-only:** false

### sqs_receive_messages
- **Description:** Receive messages from an SQS queue
- **Parameters:**
  - `queue_url` (string): URL of the SQS queue
  - `max_number_of_messages` (integer, optional, default 1): Max messages to receive (1-10)
  - `wait_time_seconds` (integer, optional): Long polling wait time
  - `visibility_timeout` (integer, optional): Visibility timeout for received messages
- **Read-only:** true

### sqs_delete_message
- **Description:** Delete a message from an SQS queue after processing
- **Parameters:**
  - `queue_url` (string): URL of the SQS queue
  - `receipt_handle` (string): Receipt handle from receive_messages
- **Read-only:** false
- **Destructive:** true

### sqs_create_queue
- **Description:** Create a new SQS queue (requires --allow-resource-creation flag)
- **Parameters:**
  - `queue_name` (string): Queue name
  - `attributes` (object, optional): Queue attributes (DelaySeconds, MaximumMessageSize, etc.)
  - `tags` (object, optional): Tags for the queue
- **Read-only:** false
- **Gated:** Only available with --allow-resource-creation

### sqs_purge_queue
- **Description:** Purge all messages from an SQS queue
- **Parameters:**
  - `queue_url` (string): URL of the SQS queue
- **Read-only:** false
- **Destructive:** true

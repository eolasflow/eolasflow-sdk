# EolasFlow Python SDK

Official Python client for the [EolasFlow](https://eolasflow.ai) Voice AI API.

## Installation

```bash
pip install eolasflow
```

## Quick Start

```python
from eolasflow import EolasFlow

client = EolasFlow(api_key="your-api-key")

# List your VoiceFlows
voiceflows = client.voiceflows.list()
for vf in voiceflows:
    print(f"{vf.name} ({vf.status})")

# Make an outbound call
result = client.calls.create(
    to_number="+353851234567",
    from_number="+35319079387",
    voiceflow_id="vf_abc123",
    customer_data={"name": "John", "reason": "appointment reminder"},
)

# Create a contact
contact = client.contacts.create(
    name="Jane Doe",
    phone="+353851234567",
    email="jane@example.com",
    company="Acme Corp",
    tags=["lead", "demo-requested"],
)

# Get call transcript and analysis
transcript = client.calls.get_transcript("call_abc123")
print(transcript.summary)

analysis = client.calls.get_analysis("call_abc123")
for item in analysis.action_items:
    print(f"- {item['item']} ({item.get('priority', 'normal')})")

# Search contacts
results = client.contacts.list(search="John")

# Find contact by phone
contact = client.contacts.find_by_phone("+353851234567")

# Manage webhooks
webhook = client.webhooks.create(
    url="https://your-app.com/webhooks/eolasflow",
    events=["call.completed", "call.started"],
)

# Add contacts to a VoiceFlow for outbound
client.voiceflows.add_contacts("vf_abc123", [
    {"phone": "+353851234567", "name": "John Doe"},
    {"phone": "+353861234567", "name": "Jane Smith"},
])
```

## Context Manager

```python
with EolasFlow(api_key="your-api-key") as client:
    calls = client.calls.list()
```

## Async Support

```python
from eolasflow.client import AsyncEolasFlow

async with AsyncEolasFlow(api_key="your-api-key") as client:
    calls = client.calls.list()
    contact = client.contacts.create(name="Jane", phone="+353851234567")
```

## Resources

| Resource | Methods |
|----------|---------|
| `client.calls` | `create`, `list`, `get`, `get_transcript`, `get_analysis`, `get_recording` |
| `client.contacts` | `create`, `get`, `find_by_phone`, `list`, `update`, `delete`, `bulk_import` |
| `client.voiceflows` | `list`, `get`, `get_stats`, `create`, `update`, `delete`, `start`, `pause`, `add_contacts` |
| `client.webhooks` | `create`, `list`, `delete` |
| `client.phone_numbers` | `list` |

## Error Handling

```python
from eolasflow import EolasFlow, AuthenticationError, RateLimitError, NotFoundError

client = EolasFlow(api_key="your-api-key")

try:
    call = client.calls.get("nonexistent")
except NotFoundError:
    print("Call not found")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except AuthenticationError:
    print("Invalid API key")
```

## License

MIT

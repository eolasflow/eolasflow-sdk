# EolasFlow SDK

Official SDKs for the [EolasFlow](https://eolasflow.ai) Voice AI API.

| Language | Package | Status |
|----------|---------|--------|
| Python | `pip install eolasflow` | In Development |
| Node.js | `npm install @eolasflow/sdk` | Planned |

## Python Quick Start

```python
from eolasflow import EolasFlow

client = EolasFlow(api_key="your-api-key")

# Make an outbound call
call = client.calls.create(
    to_number="+353851234567",
    from_number="+35319079387",
    voiceflow_id="vf_abc123",
)
print(f"Call started: {call.id}")

# List contacts
contacts = client.contacts.list(search="John")
for contact in contacts:
    print(f"{contact.name} — {contact.phone}")

# Get call transcript
transcript = client.calls.get_transcript("call_abc123")
print(transcript.summary)
```

## Authentication

Get your API key from the [EolasFlow Dashboard](https://app.eolasflow.ai) > Settings > API Keys.

```python
client = EolasFlow(
    api_key="your-api-key",
    base_url="https://api.eolasflow.ai",  # default
)
```

## Documentation

- [API Reference](https://docs.eolasflow.ai)
- [Python SDK Docs](python/README.md)

## License

MIT

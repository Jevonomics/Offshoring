"""Remove API keys echoed back in API responses before saving raw JSON."""
import os
def redact(obj):
    keys = {v for k, v in os.environ.items() if k.endswith("_API_KEY") and v}
    if isinstance(obj, dict): return {k: redact(v) for k, v in obj.items()}
    if isinstance(obj, list): return [redact(v) for v in obj]
    if isinstance(obj, str):
        for key in keys: obj = obj.replace(key, "REDACTED")
    return obj

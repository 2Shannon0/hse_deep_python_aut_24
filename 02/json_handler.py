import json
from typing import Callable, List, Optional


def process_json(
    json_str: str,
    required_keys: Optional[List[str]] = None,
    tokens: Optional[List[str]] = None,
    callback: Optional[Callable[[str, str], None]] = None,
) -> None:
    if not json_str:
        return

    data = json.loads(json_str)

    if required_keys is None or len(required_keys) == 0:
        print('required_keys list is empty')
        return

    if tokens is None or len(tokens) == 0:
        print('tokens list is empty')
        return

    for key, value in data.items():

        if key in required_keys:
            value_lower = value.lower()

            for token in tokens:
                if token.lower() in value_lower:
                    if callback:
                        callback(key, token)

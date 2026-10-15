"""Helpers for normalizing and displaying benchmark environment variables."""

import html
import json

import pandas as pd


def normalize_env_vars_value(value):
    """Normalize missing and whitespace-only environment-variable values."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def format_env_vars_hover(value):
    """Format environment variables as safe, readable Plotly hover text."""
    normalized_value = normalize_env_vars_value(value)
    if not normalized_value:
        return "None configured"

    try:
        parsed_value = json.loads(normalized_value)
    except (json.JSONDecodeError, TypeError):
        preview = html.escape(normalized_value)
    else:
        if isinstance(parsed_value, dict):
            lines = []
            for key, env_value in parsed_value.items():
                value_text = (
                    env_value
                    if isinstance(env_value, str)
                    else json.dumps(env_value, ensure_ascii=False)
                )
                lines.append(f"{html.escape(str(key))}: {html.escape(value_text)}")
            preview = "<br>".join(lines)
        else:
            preview = html.escape(json.dumps(parsed_value, ensure_ascii=False))

    return preview if len(preview) <= 800 else preview[:797] + "..."

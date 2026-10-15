"""Tests for environment-variable normalization and tooltip formatting."""

import json

import pandas as pd
import pytest

from env_vars import format_env_vars_hover, normalize_env_vars_value


@pytest.mark.parametrize("value", [None, pd.NA, float("nan"), "", " \t\n"])
def test_normalize_missing_or_whitespace_values(value):
    assert normalize_env_vars_value(value) == ""


def test_normalize_strips_outer_whitespace():
    assert normalize_env_vars_value('  {"A":"1"}  ') == '{"A":"1"}'


def test_normalize_structured_values_with_stable_key_order():
    assert normalize_env_vars_value({"B": 2, "A": 1}) == '{"A": 1, "B": 2}'


def test_hover_formats_json_as_readable_escaped_lines():
    value = json.dumps({"NCCL_DEBUG": "INFO", "VALUE": "<worker>&"})

    assert format_env_vars_hover(value) == (
        "NCCL_DEBUG: INFO<br>VALUE: &lt;worker&gt;&amp;"
    )


def test_hover_handles_missing_and_invalid_json():
    assert format_env_vars_hover("  ") == "None configured"
    assert format_env_vars_hover("<not-json>") == "&lt;not-json&gt;"


def test_hover_preview_is_bounded():
    preview = format_env_vars_hover("x" * 900)

    assert len(preview) == 800
    assert preview.endswith("...")


def test_blank_variants_do_not_create_duplicate_config_keys():
    configs = pd.DataFrame(
        {
            "model": ["model"] * 4,
            "accelerator": ["H200"] * 4,
            "version": ["vLLM"] * 4,
            "TP": [1] * 4,
            "env_vars": ["", "  ", None, '{"A":"1"}'],
        }
    )
    configs["env_vars"] = configs["env_vars"].map(normalize_env_vars_value)

    assert len(configs.drop_duplicates()) == 2

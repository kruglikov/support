import pytest

from support.config import Config, ConfigError, load_config


def test_load_config_reads_both_environment_variables(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "secret_abc")
    monkeypatch.setenv("NOTION_ROOT_PAGE_ID", "9bbf3c16e12041f3996bae0eb316cd78")

    config = load_config()

    assert config == Config(
        notion_token="secret_abc",
        root_page_id="9bbf3c16e12041f3996bae0eb316cd78",
    )


def test_load_config_raises_when_token_missing(monkeypatch):
    monkeypatch.delenv("NOTION_TOKEN", raising=False)
    monkeypatch.setenv("NOTION_ROOT_PAGE_ID", "9bbf3c16e12041f3996bae0eb316cd78")

    with pytest.raises(ConfigError, match="NOTION_TOKEN"):
        load_config()


def test_load_config_raises_when_root_page_missing(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "secret_abc")
    monkeypatch.delenv("NOTION_ROOT_PAGE_ID", raising=False)

    with pytest.raises(ConfigError, match="NOTION_ROOT_PAGE_ID"):
        load_config()

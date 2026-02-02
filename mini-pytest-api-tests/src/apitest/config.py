import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_url: str
    timeout: int = 10
    retries: int = 3
    api_token: Optional[str] = None


def load_config() -> Settings:
    # 1. Determine environment
    env_name = os.getenv("TARGET_ENV", "dev")

    # 2. Locate config file
    # Assuming config is in project_root/config/
    # This file is in src/apitest/config.py -> ../../config
    base_dir = Path(__file__).parent.parent.parent
    config_path = base_dir / "config" / f"{env_name}.yml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    # 3. Load YAML
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f) or {}

    # 4. Override with ENV vars (e.g. from .env file loaded by dotenv or shell)
    # Note: pydantic BaseSettings usually reads env vars, but here we explicitly mix yaml + env
    # For simple overrides, we can just update the dict if env var is set

    # Let's use pydantic to validate the final dict.
    # Env vars can effectively be passed via kwargs or allow pydantic to read them.
    # BaseSettings reads env vars (case-insensitive by default).
    # But checking if we want priority: ENV > YAML

    # We can pass the yaml dictionary as init kwargs. Env vars will take precedence if passed to init?
    # Actually BaseSettings priority: arguments > environment variables > dotenv > default values
    # So if we pass yaml data as arguments, they override env vars.
    # We want ENV vars to override YAML.

    # Strategy: load env vars manually into the dict only if they exist, or rely on pydantic.
    # To keep it robust: define fields in Settings, pass yaml as defaults.

    # Better approach for hybrid:
    # 1. Load yaml.
    # 2. Instantiate Settings(**yaml_data).
    # BUT this ignores Env vars for fields present in yaml data because args > env.

    # Correct approach for "ENV overrides YAML":
    # Don't pass as args. Let Pydantic load env vars.
    # But how to load YAML defaults?
    # We can update os.environ with YAML data IF NOT present? No, that's messy.

    # Cleanest:
    # implementation logic here needs to be clean
    # merged_config = config_data.copy() <--- removed

    # Explicitly check for ENV overrides for critical keys if needed,
    # or just trust user to set ENV vars that Pydantic picks up,
    # but since we want YAML to be the "defaults" for that environment...

    # Let's do:
    # 1. Create Settings object from YAML (this validates YAML).
    # 2. Update with Env vars?

    # Actually, simplest is:
    # Use Pydantic's `settings_customise_sources` if we want deep integration.
    # But for this task, let's keep it readable.

    # If I pass `**config_data` to Settings(), it overrides Env vars.
    # So I should only put things in `**config_data` that are NOT in os.environ?
    # Or just iterate config_data and set as defaults?

    # Let's stick to the requirement: "credentials/tokens from env vars only".
    # Base URL from config file.

    # Implementation:
    # Load YAML.
    # API_TOKEN comes from Env var (BaseSettings handles this).

    return Settings(**config_data)


# Global Accessor
try:
    from dotenv import load_dotenv

    load_dotenv()  # Load .env if present
except ImportError:
    pass

settings = load_config()

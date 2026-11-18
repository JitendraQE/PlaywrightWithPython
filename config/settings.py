"""Validated, environment-aware framework configuration."""
from functools import lru_cache
import os
from pathlib import Path
from typing import Literal
import yaml
from pydantic import BaseModel, Field, ValidationError


ROOT_DIR = Path(__file__).resolve().parents[1]


class ViewportConfig(BaseModel):
    width: int
    height: int


class ApplicationConfig(BaseModel):
    name: str
    base_url: str


class BrowserConfig(BaseModel):
    name: Literal["chromium", "firefox", "webkit"]
    headless: bool
    slow_mo_ms: int
    viewport: ViewportConfig = Field(default_factory=ViewportConfig)


class TimeoutConfig(BaseModel):
    action_ms: int
    navigation_ms: int
    expect_ms: int


class LoginConfig(BaseModel):
    path: str
    username_label: str
    password_label: str
    submit_button: str
    success_indicator: str
    error_indicator: str
    logout_button: str

class ExecutionConfig(BaseModel):
    workers: int
    retries: int


class ArtifactConfig(BaseModel):
    directory: str


class FrameworkConfig(BaseModel):
    application: ApplicationConfig
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    timeouts: TimeoutConfig = Field(default_factory=TimeoutConfig)
    login: LoginConfig = Field(default_factory=LoginConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    artifacts: ArtifactConfig = Field(default_factory=ArtifactConfig)


@lru_cache(maxsize=4)
def load_config(environment: str | None = None) -> FrameworkConfig:
    """Load YAML for ENV and apply supported environment-variable overrides."""
    env_name = (environment or os.getenv("ENV", "qa")).lower()
    config_path = ROOT_DIR / "config" / "environments" / f"{env_name}.yaml"

    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open(encoding="utf-8") as stream:
        raw = yaml.safe_load(stream) or {}

    # Environment variables override non-secret deployment-specific values.
    if os.getenv("BASE_URL"):
        raw.setdefault("application", {})["base_url"] = os.environ["BASE_URL"]
    if os.getenv("BROWSER"):
        raw.setdefault("browser", {})["name"] = os.environ["BROWSER"]
    if os.getenv("HEADLESS"):
        raw.setdefault("browser", {})["headless"] = os.environ["HEADLESS"].lower() == "true"

    try:
        return FrameworkConfig.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"Invalid framework configuration for ENV={env_name}:\n{exc}") from exc

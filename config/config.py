import os
import yaml
from pydantic import BaseModel
from typing import Dict

class TenantConfig(BaseModel):
    tenant_id: str
    url: str
    admin_user: str
    admin_pass: str

class EnvironmentConfig(BaseModel):
    env_name: str
    base_domain: str
    api_url: str
    tenants: Dict[str, TenantConfig]

class FrameworkConfig(BaseModel):
    environment: EnvironmentConfig
    browserstack_user: str = os.getenv("BROWSERSTACK_USERNAME", "demo_user")
    browserstack_key: str = os.getenv("BROWSERSTACK_ACCESS_KEY", "demo_key")

def get_config(env_name: str = None) -> FrameworkConfig:
    env = env_name or os.getenv("TEST_ENV", "staging")
    config_file = os.path.join(os.path.dirname(__file__), "environments.yaml")
    
    with open(config_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    env_data = data["environments"][env]
    env_config = EnvironmentConfig(
        env_name=env,
        base_domain=env_data["base_domain"],
        api_url=env_data["api_url"],
        tenants=env_data["tenants"]
    )
    return FrameworkConfig(environment=env_config)

from .util import run_bundled_exe as run_bundled_exe

DEFAULT_ROJO_PROJECT_PATH: str
ROJO_SOURCE: str
ROJO_VERSION: str

def get_rojo_project_path() -> str: ...
def build_sourcemap(project_json_path: str = ...): ...
def get_roblox_path_from_env_path(env_path: str) -> str: ...

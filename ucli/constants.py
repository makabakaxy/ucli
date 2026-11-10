"""Path constants and configuration defaults."""

import os
from pathlib import Path

USER_HOME = Path(os.environ.get("UCLI_USER_HOME", str(Path.home()))).expanduser().resolve()
DATA_DIR = USER_HOME / ".agents" / "ucli"
SESSIONS_DIR = DATA_DIR / ".sessions"
TOOLS_DIR = DATA_DIR / "tools"
CLI_DIR = DATA_DIR / "cli"
SKILLS_DIR = DATA_DIR / "skills"
SERVERS_YAML = DATA_DIR / "servers.yaml"
CONFIG_YAML = DATA_DIR / "config.yaml"
DAEMON_PID = DATA_DIR / "daemon.pid"
DAEMON_SOCK = DATA_DIR / "daemon.sock"
DAEMON_LOG = DATA_DIR / "daemon.log"
DAEMON_LOCK = DATA_DIR / "daemon.lock"

SHARED_SKILLS_DIR = USER_HOME / ".agents" / "skills"

CLIENT_CONFIGS = {
    "claude": {
        "config_path": USER_HOME / ".claude.json",
        "skill_dir": USER_HOME / ".claude" / "skills",
        "format": "claude_json",
        "server_key": "mcpServers",
    },
    "cursor": {
        "config_path": USER_HOME / ".cursor" / "mcp.json",
        "skill_dir": USER_HOME / ".cursor" / "skills",
        "format": "cursor_json",
        "server_key": "mcpServers",
    },
    "codex": {
        "config_path": USER_HOME / ".codex" / "config.toml",
        "skill_dir": SHARED_SKILLS_DIR,
        "format": "codex_toml",
        "server_key": "mcp_servers",
    },
}

TEMPLATES_DIR = Path(__file__).parent / "generator" / "templates"

SESSION_EXPIRY_HOURS = 24

PROTECTED_SKILL_DIRS = frozenset({"users", "scripts"})

RESERVED_COMMANDS = frozenset({
    "list", "scan", "generate", "validate", "daemon",
    "tools", "call", "convert", "install", "remove",
    "uninstall", "update", "mcp", "skill", "preset",
    "cli", "exec", "batch", "doctor",
})

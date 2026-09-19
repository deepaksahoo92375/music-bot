from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int = 0) -> int:
    try: return int(os.getenv(name, default))
    except ValueError: return default


def _bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(slots=True)
class Config:
    api_id: int
    api_hash: str
    bot_token: str
    owner_id: int
    assistant_sessions: list[str] = field(default_factory=list)
    web_host: str = "0.0.0.0"
    web_port: int = 8080
    web_base_url: str = "http://127.0.0.1:8080"
    database_url: str = "sqlite:///data/tss_music.db"
    cache_dir: Path = Path("cache")
    cache_max_gb: int = 500
    min_free_disk_gb: int = 100
    persist_queue: bool = True
    log_level: str = "INFO"
    requests_per_user_minute: int = 5
    max_group_queue: int = 100
    max_resolutions: int = 4
    max_video_sessions: int = 3
    auto_dj_default: bool = False
    spotify_client_id: str = ""
    spotify_client_secret: str = ""

    @classmethod
    def from_env(cls) -> "Config":
        sessions = [os.getenv(f"ASSISTANT_{i}_SESSION", "").strip() for i in range(1, 7)]
        return cls(
            api_id=_int("API_ID"), api_hash=os.getenv("API_HASH", "").strip(),
            bot_token=os.getenv("BOT_TOKEN", "").strip(), owner_id=_int("OWNER_ID"),
            assistant_sessions=sessions, web_host=os.getenv("WEB_HOST", "0.0.0.0"),
            web_port=_int("WEB_PORT", 8080), web_base_url=os.getenv("WEB_BASE_URL", "http://127.0.0.1:8080"),
            database_url=os.getenv("DATABASE_URL", "sqlite:///data/tss_music.db"),
            cache_dir=Path(os.getenv("CACHE_DIR", "cache")), cache_max_gb=_int("CACHE_MAX_GB", 500),
            min_free_disk_gb=_int("MIN_FREE_DISK_GB", 100), persist_queue=_bool("PERSIST_QUEUE", True),
            log_level=os.getenv("LOG_LEVEL", "INFO"), requests_per_user_minute=_int("REQUESTS_PER_USER_MINUTE", 5),
            max_group_queue=_int("MAX_GROUP_QUEUE", 100), max_resolutions=_int("MAX_RESOLUTIONS", 4),
            max_video_sessions=_int("MAX_VIDEO_SESSIONS", 3), auto_dj_default=_bool("AUTO_DJ_DEFAULT", False),
            spotify_client_id=os.getenv("SPOTIFY_CLIENT_ID", ""), spotify_client_secret=os.getenv("SPOTIFY_CLIENT_SECRET", ""),
        )

    def validate(self) -> list[str]:
        errors=[]
        if not self.api_id: errors.append("API_ID is missing")
        if not self.api_hash: errors.append("API_HASH is missing")
        if not self.bot_token: errors.append("BOT_TOKEN is missing")
        if not self.owner_id: errors.append("OWNER_ID is missing")
        if not self.assistant_sessions or not self.assistant_sessions[0]: errors.append("ASSISTANT_1_SESSION is missing")
        return errors

    def ensure_dirs(self) -> None:
        for p in [Path("data"), Path("logs"), Path("backups"), Path("sessions"), Path("temp"), self.cache_dir,
                  self.cache_dir/"audio", self.cache_dir/"video", self.cache_dir/"thumbnails", self.cache_dir/"metadata"]:
            p.mkdir(parents=True, exist_ok=True)

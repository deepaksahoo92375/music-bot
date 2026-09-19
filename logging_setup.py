import logging, os

def setup_logging(level: str = "INFO") -> None:
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO),
                        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler("logs/tss_music.log", encoding="utf-8")])

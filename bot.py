from __future__ import annotations
import asyncio, logging
from pyrogram import Client
from config import Config
from logging_setup import setup_logging
from database.database import Database
from database.repository import Repository
from core.assistant_manager import AssistantManager
from core.player_supervisor import PlayerSupervisor
from services.statistics import Statistics
from services.monitoring import Monitor
from web.app import create_web_app
from telegram.commands import register_handlers
from telegram.callbacks import register_callbacks
from aiohttp import web

async def main():
    config=Config.from_env(); config.ensure_dirs(); setup_logging(config.log_level); log=logging.getLogger("tss")
    errors=config.validate()
    if errors: raise RuntimeError("Configuration errors: "+"; ".join(errors))
    db=Database(config.database_url); await db.connect(); repo=Repository(db)
    assistants=AssistantManager(config); await assistants.start()
    if not assistants.choose(): raise RuntimeError("Assistant 1 must be online for startup")
    supervisor=PlayerSupervisor(config,assistants,repo); stats=Statistics(db); monitor=Monitor()
    bot=Client("tss_bot",api_id=config.api_id,api_hash=config.api_hash,bot_token=config.bot_token,in_memory=True)
    register_handlers(bot,supervisor,stats,config.owner_id); await register_callbacks(bot,supervisor)
    app=create_web_app(config,supervisor,assistants,monitor,stats); runner=web.AppRunner(app); await runner.setup(); site=web.TCPSite(runner,config.web_host,config.web_port); await site.start()
    await bot.start(); log.info("TSS Music started on %s:%s",config.web_host,config.web_port)
    try: await asyncio.Event().wait()
    finally:
        await bot.stop(); await runner.cleanup(); await assistants.stop(); await db.close()

if __name__=="__main__": asyncio.run(main())

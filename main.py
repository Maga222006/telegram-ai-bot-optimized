"""
Main application entry point with optimized database connection pooling.
Initializes centralized connection pool for improved performance.
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from database.user import init_user_db
from database.config import init_config_db
from database.connection_pool import connection_pool, initialize_connection_pool, cleanup_connection_pool
from bot.handlers import router
from bot.keyboard_handlers import router as config_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token="8009768458:AAGrbFRcjMvbLGxUfgN0KMUrcHtUUolUfYU")
dp = Dispatcher()

dp.include_router(config_router)
dp.include_router(router)

async def startup():
    """Initialize application with connection pool."""
    logger.info("Starting application...")
    
    # Initialize centralized connection pool
    await initialize_connection_pool()
    
    # Initialize databases using connection pool
    await init_config_db()
    await init_user_db()
    
    # Log connection pool statistics
    pool_stats = await connection_pool.get_pool_stats()
    logger.info(f"Connection pool initialized: {pool_stats}")
    
    # Perform health check
    health_ok = await connection_pool.health_check()
    logger.info(f"Database health check: {'PASSED' if health_ok else 'FAILED'}")
    
    logger.info("Application startup complete")

async def shutdown():
    """Cleanup application resources."""
    logger.info("Shutting down application...")
    
    # Cleanup connection pool
    await cleanup_connection_pool()
    
    logger.info("Application shutdown complete")

async def main():
    """Main application loop with proper resource management."""
    try:
        await startup()
        logger.info("Bot initialized and starting polling...")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
    finally:
        await shutdown()

if __name__ == "__main__":
    asyncio.run(main())
import structlog
from fastapi import FastAPI
from app.config.settings import settings

logger = structlog.get_logger()

app = FastAPI(title="QFTE API", version="0.1.0")


@app.get("/")
async def root():
    return {"service": "QFTE", "status": "running"}


@app.get("/health")
async def health():
    logger.info("Health check requested")
    return {"status": "ok", "service": "QFTE API"}


def setup_logging():
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger("INFO"),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )


@app.on_event("startup")
async def startup_event():
    logger.info("QFTE API starting", env=settings.env)
    setup_logging()

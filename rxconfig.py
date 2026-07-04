import reflex as rx
import os

config = rx.Config(
    app_name="sistema_admisi_n_unas",
    plugins=[rx.plugins.TailwindV3Plugin(), rx.plugins.SitemapPlugin()],
    # Production settings
    db_url=os.getenv("DATABASE_URL", "sqlite:///db_admision.db"),
    # Redis for production (uncomment if using)
    # redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)

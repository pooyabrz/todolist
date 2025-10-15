from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    """Configuration class for app settings."""

    MAX_PROJECTS: int = int(os.getenv("MAX_NUMBER_OF_PROJECT", "5"))
    MAX_TASKS_PER_PROJECT: int = int(os.getenv("MAX_NUMBER_OF_TASK", "10"))

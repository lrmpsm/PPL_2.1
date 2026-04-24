from src.cli import cli
from .logging_config import setup_logging

def main() -> None:
    setup_logging()
    cli()

if __name__ == "__main__":
    main()

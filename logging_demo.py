import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("ETL pipeline started")
logging.warning("Some records contain missing values")
logging.error("Database connection failed")
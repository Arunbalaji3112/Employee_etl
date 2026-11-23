import logging
from pathlib import Path

from extract import extract_employees
from transform import transform_employee
from load import load_csv

# STEP 1: Define project paths

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "employees.csv"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# STEP 2: Configure logging
logging.basicConfig(
    filename=LOG_DIR / "etl.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# STEP 3: Initialize collections

valid_records = []
rejected_records = []
seen_ids = set()

logger.info("Employee ETL pipeline started")

# STEP 4: Extract and transform
try:
    for record in extract_employees(INPUT_FILE):

        try:
            cleaned = transform_employee(record)

            employee_id = cleaned["id"]

            if employee_id in seen_ids:
                raise ValueError("Duplicate employee ID")

            seen_ids.add(employee_id)
            valid_records.append(cleaned)

            logger.info(
                "Employee ID %s processed successfully",
                employee_id
            )

        except (ValueError, TypeError, KeyError) as e:

            rejected_records.append({
                "id": record.get("id", ""),
                "name": record.get("name", ""),
                "reason": str(e)
            })

            logger.warning(
                "Employee ID %s rejected: %s",
                record.get("id", "Unknown"),
                e
            )


    # STEP 5: Load valid records
    load_csv(
        OUTPUT_DIR / "valid_employees.csv",
        valid_records,
        ["id", "name", "salary", "department", "annual_salary"]
    )

    logger.info("Valid employee CSV created successfully")


    # STEP 6: Load rejected records
    load_csv(
        OUTPUT_DIR / "rejected_employees.csv",
        rejected_records,
        ["id", "name", "reason"]
    )

    logger.info("Rejected employee CSV created successfully")


    # STEP 7: Log summary
    logger.info(
        "Total records: %s",
        len(valid_records) + len(rejected_records)
    )

    logger.info("Valid records: %s", len(valid_records))
    logger.info("Rejected records: %s", len(rejected_records))

    logger.info("Employee ETL pipeline completed successfully")

    print("ETL completed. Check the output and logs folders.")

except Exception:
    logger.exception("ETL pipeline failed")
    raise


print("Total records:", len(valid_records) + len(rejected_records))
print("Valid records:", len(valid_records))
print("Rejected records:", len(rejected_records))
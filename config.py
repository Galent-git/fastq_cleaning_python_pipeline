import sys

MIN_PY_VERSION = (3,6)

def check_python_version():
    if sys.version_info < MIN_PY_VERSION:
        sys.stderr.write(f"Need Python {MIN_PY_VERSION[0]}.{MIN_PY_VERSION[1]} or later.\n")
        sys.exit(1)

CLEANED_SUBDIRS = [
    "raw_stats",
    "cleaned_data",
    "qc_reports/fastqc_reports",
    "logs",
    "archive",
    "qc_reports/fastqc_trimmed"
]


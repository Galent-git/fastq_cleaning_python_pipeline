
#!/usr/bin/env python3
import argparse
import logging
import sys
from pipeline import run_pipeline
from config import MIN_PY_VERSION, check_python_version
from qc_utils import which_tool

logger = logging.getLogger("fastq_pipeline")

def main():
    check_python_version()  # ensures Python >= 3.6, for example

    parser = argparse.ArgumentParser(description='FASTQ Cleaning Pipeline (Modular)')
    parser.add_argument('-i', '--input_directory', required=True)
    parser.add_argument('-o', '--output_directory', required=True)
    parser.add_argument('--min_mean_quality', type=float, default=15)
    parser.add_argument('--interactive_mode', action='store_true')
    parser.add_argument('--post_trim_qc', action='store_true')
    parser.add_argument('--parallel', action='store_true')

    args = parser.parse_args()

    # Check external executables
    for cmd in ["fastqc", "multiqc", "fastp"]:
        if not which_tool(cmd):
            logger.warning("`%s` not found in PATH. Please install %s for full functionality.", cmd, cmd)

    # Orchestrate pipeline
    run_pipeline(args)
    logger.info("Done.")

if __name__ == "__main__":
    # Configure logging if you want
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
    main()

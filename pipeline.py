
import os
import sys
import shutil
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

from bio_utils import validate_fastq, collect_stats, clean_reads
from qc_utils import run_fastqc, run_multiqc, parse_multiqc_for_adapter_info, suggest_fastp_cmd
from config import CLEANED_SUBDIRS

logger = logging.getLogger("fastq_pipeline")

def process_one_file(fq, args):
    """Processes a single FASTQ: stats, cleaning, runs fastqc."""
    stats = collect_stats(fq)
    min_len = 0.2 * stats['mean_length']
    # ...
    # call clean_reads, run_fastqc, etc.
    # Return dict of summary info
    return {
        'file': os.path.basename(fq),
        'total_reads': stats['total_reads'],
        # ...
    }

def run_pipeline(args):
    """Orchestrate the entire pipeline."""
    # Make subdirs
    for d in CLEANED_SUBDIRS:
        os.makedirs(os.path.join(args.output_directory, d), exist_ok=True)

    # Gather FASTQ files
    fastq_files = []
    for f in os.listdir(args.input_directory):
        if f.lower().endswith(('.fastq', '.fq')):
            fastq_files.append(os.path.join(args.input_directory, f))

    # Validate & copy to archive
    for fq_path in fastq_files:
        if not validate_fastq(fq_path):
            logger.error("%s not valid. Exiting.", fq_path)
            sys.exit(1)
        shutil.copy(fq_path, os.path.join(args.output_directory, 'archive'))

    # Parallel or sequential
    results = []
    if args.parallel:
        with ProcessPoolExecutor() as executor:
            futs = {executor.submit(process_one_file, fq, args): fq for fq in fastq_files}
            for fut in as_completed(futs):
                results.append(fut.result())
    else:
        for fq in fastq_files:
            results.append(process_one_file(fq, args))

    # Then run multiqc
    run_multiqc(os.path.join(args.output_directory, 'qc_reports', 'fastqc_reports'),
                os.path.join(args.output_directory, 'qc_reports', 'multiqc_data.json'))

    # parse multiqc + suggest fastp
    qc_info = parse_multiqc_for_adapter_info(os.path.join(args.output_directory, 'qc_reports', 'multiqc_data.json'))
    fastp_cmd = suggest_fastp_cmd(50, qc_info)  # just example
    # ...
    # if post_trim_qc, run fastp, etc.
    # log final summary

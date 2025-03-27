import os
import pytest
from pipeline import run_pipeline

def test_run_pipeline(tmp_path):
    # create a small test directory with dummy fastq files
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    # create a small dummy fastq
    (input_dir / "test.fastq").write_text(
        "@read1\nACGT\n+\n!!!!\n"
        "@read2\nACGT\n+\n!!!!\n"
    )

    class Args:
        input_directory = str(input_dir)
        output_directory = str(output_dir)
        min_mean_quality = 15
        interactive_mode = False
        post_trim_qc = False
        parallel = False

    run_pipeline(Args())
    # assert certain files exist
    assert (output_dir / "archive" / "test.fastq").is_file()
    assert (output_dir / "qc_reports" / "fastqc_reports").exists()


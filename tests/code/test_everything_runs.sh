#!/bin/bash
# This script ensures every command produces a nonzero exit status.
# It must be run from the project's home directory in an appropriate
# environment.

rm -rf test_output
mkdir -p test_output

python3 . fasta tests/files/fasta/RNA_section__454_9627.fa test_output/fasta.csv \
&& python3 . stats tests/files/stats/23456_WT_cellular.tombo.stats test_output/stats.csv \
&& python3 . browser-files --bed tests/files/browser_files/WT_cellular.coverage.sample.plus.bedgraph test_output/browser_files_1.csv \
&& python3 . browser-files --wig tests/files/browser_files/WT_cellular.dampened_fraction_modified_reads.plus.wig test_output/browser_files_2.csv \
&& python3 . per-read-stats --long tests/files/per_read_stats/23456_WT_cellular.tombo.per_read_stats test_output/per_read_stats_1.csv \
&& python3 . per-read-stats --wide tests/files/per_read_stats/23456_WT_cellular.tombo.per_read_stats test_output/per_read_stats_2.csv \
&& python3 . events tests/files/fast5_dir test_output/events_1.csv \
&& python3 . events --wide=length tests/files/fast5_dir test_output/events_2.csv

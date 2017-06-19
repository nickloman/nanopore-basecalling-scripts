# nanopore-basecalling-scripts

Nick Loman
19th June 2017

## Introduction

Some simple scripts to ease management and local basecalling of millions of FAST5 files.

These scripts are designed to help with the following (common) occurrences:

  * Albacore crashing/disk filling/lost power during a basecalling run; wishing to start back where you left off.
  * How to live basecall on a server while files are being synchronised into a directory.
  * Directories getting muddled with the results of multiple sequencing runs from diffrent flowcells.

## Basic usage

The scripts work in the following way and consider three main directories:

  ``data`` - the directory (including subfolders) where reads are uploaded to
  ``staging`` - a directory that basecalling is run from
  ``basecalls`` - the final results directory with the basecalls from Albacore

To run the scripts, we suggest the following pipeline

### Stage files

Symlink all the files that need to be processed into ``staging``:

  ``python stageflowcells.py data basecalls staging``

### Basecall

As normal with Albacore, substituting $flowcell as appropriate:

  ``read_fast5_basecaller.py -i staging/$flowcell -s basecalls/$flowcell ...``

### Live Basecalling

Run the following two commands, then nuke the staging directory. Loop and repeat.



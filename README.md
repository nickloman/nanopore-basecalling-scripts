# nanopore-basecalling-scripts

Nick Loman
19th June 2017

## Introduction

Some simple scripts to ease management and local basecalling of millions of FAST5 files.

These scripts are designed to help with the following (common) occurrences:

  * Albacore crashing/disk filling/lost power during a basecalling run; wishing to start back where you left off.
  * Live basecalling on a server while files are being synchronised into a directory.
  * Directories getting muddled with the results of multiple sequencing runs from diffrent flowcells.

## Basic usage

The scripts work in the following way and consider three main directories:

  * ``data`` - the directory (including subfolders) where reads are uploaded to
  * ``staging`` - a directory that basecalling is run from
  * ``basecalls`` - the final results directory with the basecalls from Albacore

To run the scripts, we suggest the following pipeline

### Stage files

Symlink all the files that need to be processed into ``staging``:

  ``python stageflowcells.py data basecalls staging``

### Basecall

As normal with Albacore, substituting $flowcell as appropriate:

  ``read_fast5_basecaller.py -i staging/$flowcell -s basecalls/$flowcell ...``

### Live Basecalling

Run the following two commands, then nuke the staging directory. Loop and repeat.

## How to sync to a server

We like to use ``rsync`` on the MinKNOW laptop. Mac and Linux machines will have ``rsync`` installed already. We like to use Cygwin on Windows PCs.

We typically use a recipe like this to transfer all reads matching ``*.fast5`` into the data directory, over an SSH connection:

   - Start a new Cygwin Window

   - Change directory to c:\data\reads, e.g.

     ``cd /cygdrive/c/data/reads``

   - To rsync on a loop, run the following, replacing ``USER``, ``SERVER`` and ``/REMOTE/DIRECTORY/data``:

    while true;
    do
       rsync -vr --remove-source-files --include "*.fast5" --include "*/" --exclude "*" . USER@SERVER:/REMOTE/DIRECTORY/data
       sleep 5 ;
    done

   - ``--remove-source-files`` will remove the FAST5 files after they are transferred! Useful if you want to stop the local MinKNOW PC hard disk from filling up.

Don't use that flag if you want to keep a local copy- but try to move the files out somewhere else from time to time or the directory will get very full and you will get a mix of files from different runs as you put more runs on which gets hard to manage!






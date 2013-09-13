Quickstart
==========

Implementation
--------------

Data organization
^^^^^^^^^^^^^^^^^

By default, samples sequenced at Science for Life Laboratory Genomics
Core Facility, Stockholm, are organized by directories *project name*,
*sample id*, and *flowcell*. Each flowcell, finally, contains the
sequence files (in gzipped fastq format) labelled with lane and
barcode sequence information. For obvious reasons, the test data in
`ngs.test.data <https://github.com/percyfal/ngs.test.data>`_ has
been organized according to these principles. Running the command
:program:`tree` on the project ``J.Doe_00_01`` yields

.. code-block:: text

    |-- P001_101_index3
    |   |-- 120924_AC003CCCXX
    |   |   |-- P001_101_index3_TGACCA_L001_R1_001.fastq.gz
    |   |   |-- P001_101_index3_TGACCA_L001_R2_001.fastq.gz
    |   |   `-- SampleSheet.csv
    |   |-- 121015_BB002BBBXX
    |   |   |-- P001_101_index3_TGACCA_L001_R1_001.fastq.gz
    |   |   |-- P001_101_index3_TGACCA_L001_R2_001.fastq.gz
    |   |   `-- SampleSheet.csv
    |-- P001_102_index6
    |   `-- 120924_AC003CCCXX
    |       |-- P001_102_index6_ACAGTG_L002_R1_001.fastq.gz
    |       |-- P001_102_index6_ACAGTG_L002_R2_001.fastq.gz
    |       `-- SampleSheet.csv

Here, sample ``P001_101_index3`` has sequence data from flowcells
``120924_AC003CCCXX`` and ``121015_BB002BBBXX``, both run in lane 1
(``L001``) with barcode sequence ``TGACCA``.

Target generating handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^

Some :mod:`ratatosk` tasks require helper functions or classes that
collect information about samples and raw data. The
:mod:`ratatosk.ext.scilife` target generating functions have been
tailored to work with data organized as described in the previous
section. For instance, the function
:func:`ratatosk.ext.scilife.sample.collect_sample_runs` collects and
organizes information about sample runs for task :class:`MergeSamFiles
<ratatosk.lib.tools.picard.MergeSamFiles>` which merges aligned
sequences for a sample and places the output directly in the sample
folder. Similarly, :class:`ratatosk.ext.scilife.sample.target_generator`
collects information about project samples for use with best practice
pipelines.


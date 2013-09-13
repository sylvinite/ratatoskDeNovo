Tutorial
========

This tutorial shows how to run some common analyses with the helper
scripts. The focus is on submitting jobs to the cluster via SLURM.

.. note:: You can receive mail notifications by creating a file
   ``client.cfg`` in the directory where you submit the jobs. The file
   should have the following content:

   .. code-block:: text

      [core]
      error-email: YOURMAILADDRESS



Pipelines
---------

Common to all pipelines is that they load a predefined configuration
file (see :mod:`ratatosk.ext.scilife.config`). Apart from defining the
task workflow order, they set SciLife-specific :ref:`target generator
functions <handler_and_targets>` to use. The following is an excerpt
from the configuration file ``haloplex.yaml``:

.. code-block:: text

   # Main configuration file for HaloPlex analysis
   settings:
     target_generator_handler: ratatosk.ext.scilife.sample.target_generator

   ratatosk.lib.tools.picard:
     MergeSamFiles:
       parent_task: ratatosk.lib.tools.picard.SortSam
       target_generator_handler: ratatosk.ext.scilife.sample.collect_sample_runs

   ratatosk.lib.align.bwa:
     Bampe:
       label: .trimmed.sync
       add_label:
	 - _R1_001.trimmed.sync
	 - _R2_001.trimmed.sync

Although the :attr:`parent_task
<ratatosk.job.BaseJobTask.parent_task>` attributes cannot be modified,
task options and more can be by providing a custom configuration file
(passed via the :attr:`custom_config
<ratatosk.job.BaseJobTask.custom_config>` parameter). In fact, the
first thing you should do is write a custom configuration file that
contains information about what reference to use, and possibly target
file locations. For instance, the configuration file
``J.Doe_00_01.yaml`` in the examples directory has the following
content:

.. code-block:: text

   # Project configuration file
   ratatosk.lib.align.bwa:
     bwaref: /path/to/data/genomes/Hsapiens/hg19/bwa/chr11.fa
     Aln:
       # NB: shouldn't work since this is a custom config file
       parent_task: ratatosk.lib.align.bwa.Sampe
       # However this should work
       options: [-e 2 -l 40]

   ratatosk.lib.tools.picard:
     HsMetrics:
       target_regions: /path/to/data/genomes/Hsapiens/hg19/seqcap/chr11_targets.interval_list
       bait_regions: /path/to/data/genomes/Hsapiens/hg19/seqcap/chr11_baits.interval_list
     MergeSamFiles:
       parent_task: ratatosk.lib.tools.picard.SortSam

   ratatosk.lib.tools.gatk:
     ref: /path/to/data/genomes/Hsapiens/hg19/seq/chr11.fa
     knownSites: 
       - /path/to/data/genomes/Hsapiens/hg19/variation/dbsnp132_chr11.vcf
     dbsnp: /path/to/data/genomes/Hsapiens/hg19/variation/dbsnp132_chr11.vcf
     train_indels: /path/to/data/genomes/Hsapiens/hg19/variation/Mills_Devine_2hit.indels.vcf

.. note:: Currently you need to set both ``bwaref`` and ``ref``. A
   future implementation will set these via a common ``genome`` option.

See also :ref:`ratatosk.pipeline`. 

Align
^^^^^^^^^^^^^^

.. code-block:: text

   ratatosk_submit_job.py Align inputdir --custom-config custom_config_file.yaml -A ACCOUNT --partition node -t TIME
   ratatosk_submit_job.py AlignSummary inputdir --custom-config custom_config_file.yaml -A ACCOUNT --partition node -t TIME


SeqCap
^^^^^^^^^^^^^^^

.. code-block:: text

   ratatosk_submit_job.py SeqCap inputdir --custom-config custom_config_file.yaml -A ACCOUNT --partition node -t TIME
   ratatosk_submit_job.py SeqCapSummary inputdir --custom-config custom_config_file.yaml -A ACCOUNT --partition node -t TIME

HaloPlex
^^^^^^^^^^^^^^^

.. code-block:: text

   ratatosk_submit_job.py HaloPlex inputdir --custom-config custom_config_file.yaml -A ACCOUNT --partition node -t TIME
   ratatosk_submit_job.py HaloPlexSummary inputdir --custom-config custom_config_file.yaml -A ACCOUNT --partition node -t TIME

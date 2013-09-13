Helper scripts
==============

.. _ratatosk_run_scilife:

ratatosk_run_scilife.py
-----------------------

:program:`ratatosk_run_scilife.py` is a helper script that is shipped
with the ratatosk distribution. It collects the library wrapper tasks,
thus serving as an interface to small tasks, as well as pipeline
tasks. The only difference between this script and the main
:mod:`ratatosk` run script is that :program:`ratatosk_run_scilife.py`
loads pipeline configuration files located at
:mod:`ratatosk.config.scilife`. These configuration files use target
generator functions specific to scilife data structure.


Running :program:`ratatosk_run_scilife.py -h` shows the main options,
as well as the available tasks (abbreviated output for clarity):

.. code-block:: text

   usage: ratatosk_run_scilife.py [-h] [--config-file CONFIG_FILE]
				  [--scheduler-port SCHEDULER_PORT] [--dry-run]
				  [--lock] [--workers WORKERS]
				  [--lock-pid-dir LOCK_PID_DIR]
				  [--scheduler-host SCHEDULER_HOST]
				  [--restart-from RESTART_FROM]
				  [--custom-config CUSTOM_CONFIG]
				  [--target-generator-file TARGET_GENERATOR_FILE]
				  [--use-long-names] [--use-target-names]
				  [--local-scheduler] [--restart]

				  {HsMetricsNonDup,Bampe,Bgzip,PicardMetricsNonDup,...}
				  ...

   positional arguments:
     {HsMetricsNonDup,Bampe,Bgzip,PicardMetricsNonDup,...}

   optional arguments:
     -h, --help            show this help message and exit
     --config-file CONFIG_FILE
			   config_file Main configuration file. [default: 
			   ~/opt/ratatosk/ratatosk/../config/ratatosk.
			   yaml]
     --scheduler-port SCHEDULER_PORT
			   scheduler_port Port of remote scheduler api process
			   [default: 8082]
     --dry-run             dry_run Generate pipeline graph/flow without running
			   any commands [default: False]
     --lock                lock Do not run if the task is already running
			   [default: False]
     --workers WORKERS     workers Maximum number of parallel tasks to run
			   [default: 1]
     --lock-pid-dir LOCK_PID_DIR
			   lock_pid_dir Directory to store the pid file [default:
			   /var/tmp/luigi]
     --scheduler-host SCHEDULER_HOST
			   scheduler_host Hostname of machine running remote
			   scheduler [default: localhost]
     --restart-from RESTART_FROM
			   restart_from NOT YET IMPLEMENTED: Restart pipeline
			   from a given task. [default: None]
     --custom-config CUSTOM_CONFIG
			   custom_config Custom configuration file for tuning
			   options in predefined pipelines in which workflow may
			   not be altered. [default: None]
     --target-generator-file TARGET_GENERATOR_FILE
			   target_generator_file Target generator file name
			   [default: None]
     --use-long-names      use_long_names Use long names (including all options)
			   in graph vizualization [default: False]
     --use-target-names    use_target_names Use target names in graph
			   vizualization [default: False]
     --local-scheduler     local_scheduler Use local scheduling [default: False]
     --restart             restart Restart pipeline from scratch. [default:
			   False]


ratatosk_submit_job.py
----------------------

:program:`ratatosk_submit_job.py` is a script that submits jobs to a
cluster using the :mod:`drmaa` module, an implementation of the
`Distributed Resource Management Application API
<http://en.wikipedia.org/wiki/DRMAA>`_ specification. It is basically
a wrapper for :program:`ratatosk_run_scilife.py`, adding options for
drmaa. The output from :program:`ratatosk_submit_job.py -h` is 

.. code-block:: text

   usage: ratatosk_submit_job.py [-h] [-n] -A ACCOUNT [-p {node,core,devel}]
				 [-t TIME] [-J JOBNAME] [-D WORKINGDIRECTORY]
				 [-o OUTPUTPATH] [-e ERRORPATH] [--email EMAIL]
				 [--extra EXTRA] [-O OUTDIR]
				 [--sample [SAMPLE [SAMPLE ...]]]
				 [--sample_file SAMPLE_FILE]
				 [--lane [{1,2,3,4,5,6,7,8} [{1,2,3,4,5,6,7,8} ...]]]
				 [--flowcell [FLOWCELL [FLOWCELL ...]]]
				 [-B BATCH_SIZE] [-1 SAMPLE_TARGET_SUFFIX]
				 [-2 RUN_TARGET_SUFFIX]
				 [--config-file CONFIG_FILE]
				 [--custom-config CUSTOM_CONFIG]
				 [--workers WORKERS]
				 [--scheduler-host SCHEDULER_HOST]
				 task indir

   ratatosk submit job arguments.

   optional arguments:
     -h, --help            show this help message and exit

   Common options:
     -n, --dry_run         do a dry run (prints commands without actually running
			   anything) (default: False)

   Drmaa options:
     -A ACCOUNT, --account ACCOUNT
			   UPPMAX project account id (default: None)
     -p {node,core,devel}, --partition {node,core,devel}
			   partition type. (default: node)
     -t TIME, --time TIME  run time (default: 10:00:00)
     -J JOBNAME, --jobname JOBNAME
			   job name (default: ratatosk)
     -D WORKINGDIRECTORY, --workingDirectory WORKINGDIRECTORY
			   working directory (default: .)
     -o OUTPUTPATH, --outputPath OUTPUTPATH
			   output path for stdout (default: .)
     -e ERRORPATH, --errorPath ERRORPATH
			   output path for stderr (default: .)
     --email EMAIL         email address to send job information to (default:
			   None)
     --extra EXTRA         Extra specification args to submit via drmaa, provided
			   as string (e.g. "--ntasks 4 --nodes 2 -C fat" for
			   running 4 tasks on 2 nodes on fat partitions)
			   (default: [])

   Sample options:
     -O OUTDIR, --outdir OUTDIR
			   Output directory. Defaults to input directory, (i.e.
			   runs analysis in input directory). Setting this will
			   create symlinks for all requested files in input
			   directory, mirroring the input directory structure.
			   (default: None)
     --sample [SAMPLE [SAMPLE ...]]
			   samples to process (default: None)
     --sample_file SAMPLE_FILE
			   file containing samples to process, one per line
			   (default: None)
     --lane [{1,2,3,4,5,6,7,8} [{1,2,3,4,5,6,7,8} ...]]
			   lanes to process (default: None)
     --flowcell [FLOWCELL [FLOWCELL ...]]
			   flowcells to process (default: None)
     -B BATCH_SIZE, --batch_size BATCH_SIZE
			   number of samples to process per node (default: 4)
     -1 SAMPLE_TARGET_SUFFIX, --sample-target-suffix SAMPLE_TARGET_SUFFIX
			   target suffix to add to the sample target (position 1
			   in target generator tuple) (default: None)
     -2 RUN_TARGET_SUFFIX, --run-target-suffix RUN_TARGET_SUFFIX
			   target suffix to add to the sample run target
			   (position 2 in target generator tuple) (default: None)
     indir                 Input directory. Assumes that data in input directory
			   is organized by sample/flowcell/sequences.fastq.gz

   Ratatosk options. These arguments are passed directly to ratatosk_run_scilife.py:
     --config-file CONFIG_FILE
			   configuration file (default: None)
     --custom-config CUSTOM_CONFIG
			   custom configuration file (default: None)
     --workers WORKERS     number of workers to use (default: 4)
     --scheduler-host SCHEDULER_HOST
			   host that runs scheduler (default: localhost)
     task                  Task to run.


As can be seen, there are three option groups; one for
:py:mod:`drmaa`, one for modifying what samples are run, and one for
ratatosk in general.


At the very minimum, a command consists of the following

.. code-block:: text
 
   ratatosk_submit_job.py Task indir -A account_name 


Adding the ``--outdir`` flag will symlink sources from the input
directory:

.. code-block:: text

   ratatosk_submit_job.py Task indir -A account_name  --outdir outdir

For large projects (e.g. HaloPlex), in which you typically have 50-100
samples, you can "batch" your input into reasonably sized groups that
will be run independently on different nodes. The following command
will submit jobs running on 8 samples in each batch.

.. code-block:: text

   ratatosk_submit_job.py Task indir -A account_name
     --outdir outdir --batch_size 8

The downside of this is of course that tasks requiring all samples to
be processed must be submitted separately once the previous tasks are
done.


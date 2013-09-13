Installation
============

Quick installation instructions
-------------------------------

The following command sequence should install
:mod:`ratatosk.ext.scilife`. Make sure you have installed the
:mod:`ratatosk` main module. 

.. code-block:: text

   INSTALL_PREFIX=~/opt
   git clone https://github.com/percyfal/ratatosk.ext.scilife $INSTALL_PREFIX/ratatosk.ext.scilife
   cd $INSTALL_PREFIX/ratatosk.ext.scilife && python setup.py develop
   cd $INSTALL_PREFIX/ratatosk.ext.scilife/test && nosetests -v -s

Pre-requisites
--------------

Install `ratatosk <https://github.com/percyfal/ratatosk>`_. To run the
full test suite, you also need to install the test data set
`ngs.test.data <https://github.com/percyfal/ngs.test.data.git>`_. The
test data set is necessary for testing and running the pipelines.

:mod:`ratatosk.ext.scilife` makes use of the :mod:`drmaa` module to
interact with SLURM. Add the following to ``.bashrc``:

.. code-block:: text

   # DRMAA for SLURM and SGE
   export DRMAA_LIBRARY_PATH=/bubo/sw/apps/build/slurm-drmaa/1.0.6/lib/libdrmaa.so
   export DRMAA_PATH=$DRMAA_LIBRARY_PATH


.. _installation:

Installation
------------

You can download and install :mod:`ratatosk.ext.scilife` from the
`Python Package Index
<https://pypi.python.org/pypi/ratatosk.ext.scilife>`_ with the command

.. code-block:: text

   pip install ratatosk.ext.scilife

To install the development version of :mod:`ratatosk.ext.scilife`, do

.. code-block:: text
	
	git clone https://github.com/percyfal/ratatosk.ext.scilife
	python setup.py develop

Running the tests
-----------------

Make sure that an instance of the daemon ``ratatoskd`` is running in
the background. It may be convenient to run it in a ``screen``
session.

.. code-block:: text

   ratatoskd &

Cd to the test directory (``test``) and run

.. code-block:: text

   nosetests -v -s 

.. note:: Currently (20130417) many tests are failing but will be
   fixed shortly
	

Running example pipelines
^^^^^^^^^^^^^^^^^^^^^^^^^

For all examples, first cd to the :mod:`ratatosk.ext.scilife`
installation path. If you want to visualize the task graph (at
``localhost:8081``), make sure to start the server daemon
:program:`ratatoskd` in the background. The ``examples`` subdirectory
contains an example configuration file for project ``J.Doe_00_01``
that is used in the following examples.

.. note:: For the time being, you need to modify the paths to point to your ngs
   test data installation directory in the configuration file

.. note:: If a pipeline fails, make sure you have set the necessary
   environment variables ``GATK_HOME``, ``PICARD_HOME``, and
   ``SNPEFF_HOME``

To run the basic alignment pipeline, issue

.. code-block:: text

   ratatosk_run_scilife.py Align --indir /path/to/ngs.test.data/data/projects/J.Doe_00_01
     --outdir output_directory --custom-config examples/J.Doe_00_01 --workers 4

Analogously, to run the SeqCap pipeline, issue

.. code-block:: text

   ratatosk_run_scilife.py SeqCap --indir /path/to/ngs.test.data/data/projects/J.Doe_00_01
     --outdir output_directory --custom-config examples/J.Doe_00_01 --workers 4


Finally, to run the HaloPlex pipeline and run the summary, run

.. code-block:: text

   ratatosk_run_scilife.py HaloPlex --indir /path/to/ngs.test.data/data/projects/J.Doe_00_01
     --outdir output_directory --custom-config examples/J.Doe_00_01 --workers 4

   ratatosk_run_scilife.py HaloPlexSummary --indir /path/to/ngs.test.data/data/projects/J.Doe_00_01
     --outdir output_directory --custom-config examples/J.Doe_00_01 --workers 4

Testing issues
^^^^^^^^^^^^^^

 - During pipeline execution, a :program:`picard` tool
   (:program:`CreateSequenceDictionary`) is used to convert the
   reference
   ``/path/to/ngs.test.data/data/genomes/Hsapiens/hg19/seq/chr11.fa``
   to a dictionary file (``chr11.dict``). For some reason, this
   currently fails. Therefore you may need to run the command
   manually.

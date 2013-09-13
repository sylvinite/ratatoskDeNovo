# Copyright (c) 2013 Per Unneberg
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
import os
import shutil
import unittest
import logging
import ratatosk.lib.files.input
from ratatosk.ext.scilife.sample import *


class Task(object):
    suffix = ".bam"
    def __init__(self, target, label, suffix, add_label=None, parent_task=ratatosk.lib.files.input.InputBamFile):
        self._target = target
        self._label = label
        self._suffix = suffix
        self._add_label = add_label
        self._parent_task = parent_task

    @property
    def target(self):
        return self._target

    @property
    def label(self):
        return self._label

    def sfx(self):
        return self._suffix

    def adl(self):
        return self._add_label

    def parent(self):
        return [self._parent_task]
        
class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.project = os.path.join("projects", "J.Doe_00_01")
        self.sample = 'P001_101_index3'
        self.flowcell = '120924_AC003CCCXX'

    def tearDown(self):
        if os.path.exists("tmp"):
            shutil.rmtree("tmp")

    def test_tg_all(self):
        """Test getting all sample runs from a project"""
        tl = target_generator(indir=self.project)
        self.assertEqual(sorted([x.sample_id() for x in tl]), ['P001_101_index3', 'P001_101_index3', 'P001_101_index3', 'P001_102_index6', 'P001_102_index6'])
        self.assertEqual(list(set([x.sample_id() for x in tl])), ['P001_101_index3', 'P001_102_index6'])

    def test_tg_subset_sample(self):
        """Test getting a subset of samples"""
        tl = target_generator(indir=self.project, sample=[self.sample])
        self.assertEqual(sorted([x.sample_id() for x in tl]), ['P001_101_index3', 'P001_101_index3', 'P001_101_index3'])

    def test_tg_subset_flowcell(self):
        """Test getting samples subsetted by flowcell"""
        tl = target_generator(indir=self.project, flowcell=[self.flowcell])
        self.assertNotIn("121015_BB002BBBXX",  sorted([os.path.basename(os.path.dirname(x.prefix("sample_run"))) for x in tl]))

    def test_tg_subset_sample_flowcell(self):
        """Test getting samples subsetted by flowcell and sample"""
        tl = target_generator(indir=self.project, flowcell=[self.flowcell], sample=[self.sample])
        self.assertEqual(sorted([os.path.basename(os.path.dirname(x.prefix("sample_run"))) for x in tl]), ['120924_AC003CCCXX', '120924_AC003CCCXX'])
        self.assertEqual(sorted([os.path.basename(x.sample_id()) for x in tl]), ['P001_101_index3', 'P001_101_index3'])

    def test_collect_sample_runs(self):
        """Test function that collects sample runs"""
        t = Task(target=os.path.join(self.project, "P001_101_index3", "P001_101_index3.sort.merge.bam"), label=".merge", suffix=".bam")
        bam_list = collect_sample_runs(t)
        self.assertEqual('P001_101_index3_TGACCA_L001.sort.bam', os.path.basename(sorted(bam_list)[0]))

    def test_collect_vcf_files(self):
        """Test function that collects vcf files"""
        t = Task(target=os.path.join(self.project, "CombineVariants.vcf"), suffix=".vcf", label="", add_label=".sort.merge",
                 parent_task=ratatosk.lib.files.input.InputVcfFile)
        vcf_list = collect_vcf_files(t)
        self.assertEqual("P001_101_index3.sort.merge.vcf", os.path.basename(sorted(vcf_list)[0]))

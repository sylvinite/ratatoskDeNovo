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

def setUpModule():
    structure= [ 
        "./projects/J.Doe_00_01/P001_101_index3/120924_AC003CCCXX/P001_101_index3_TGACCA_L001_R1_001.fastq.gz", 
        "./projects/J.Doe_00_01/P001_101_index3/120924_AC003CCCXX/P001_101_index3_TGACCA_L001_R2_001.fastq.gz", 
        "./projects/J.Doe_00_01/P001_101_index3/120924_AC003CCCXX/P001_101_index3_TGACCA_L002_R1_002.fastq.gz", 
        "./projects/J.Doe_00_01/P001_101_index3/120924_AC003CCCXX/P001_101_index3_TGACCA_L002_R2_002.fastq.gz", 

        "./projects/J.Doe_00_01/P001_101_index3/121015_BB002BBBXX/P001_101_index3_TGACCA_L001_R1_001.fastq.gz", 
        "./projects/J.Doe_00_01/P001_101_index3/121015_BB002BBBXX/P001_101_index3_TGACCA_L001_R2_001.fastq.gz", 

        "./projects/J.Doe_00_01/P001_102_index6/120924_AC003CCCXX/P001_102_index6_ACAGTG_L002_R1_001.fastq.gz", 
        "./projects/J.Doe_00_01/P001_102_index6/120924_AC003CCCXX/P001_102_index6_ACAGTG_L002_R2_001.fastq.gz", 

        "./projects/J.Doe_00_01/P001_102_index6/121015_BB002BBBXX/P001_102_index6_ACAGTG_L001_R1_001.fastq.gz", 
        "./projects/J.Doe_00_01/P001_102_index6/121015_BB002BBBXX/P001_102_index6_ACAGTG_L001_R2_001.fastq.gz", 

        "./projects/J.Doe_00_01/P001_101_index3/P001_101_index3.sort.merge.vcf", 
        "./projects/J.Doe_00_01/P001_102_index6/P001_102_index6.sort.merge.vcf", 

        ]
    for p in structure:
        path, file = os.path.split( p )
        try:
            os.makedirs( path )
        except OSError:
            pass
        with open( p, "w" ) as f:
            f.write("")

    with open("./projects/J.Doe_00_01/P001_101_index3/120924_AC003CCCXX/SampleSheet.csv", "w") as fh:
        fh.write("\n".join(["FCID,Lane,SampleID,SampleRef,Index,Description,Control,Recipe,Operator,SampleProject",
                            "C003CCCXX,1,P001_101_index3,hg19,TGACCA,J__Doe_00_01,N,R1,NN,J__Doe_00_01",
                            "C003CCCXX,2,P001_101_index3,hg19,TGACCA,J__Doe_00_01,N,R1,NN,J__Doe_00_01"]))

    with open("./projects/J.Doe_00_01/P001_101_index3/121015_BB002BBBXX/SampleSheet.csv", "w") as fh:
        fh.write("\n".join(["FCID,Lane,SampleID,SampleRef,Index,Description,Control,Recipe,Operator,SampleProject",
                            "B002BBBXX,1,P001_101_index3,hg19,TGACCA,J__Doe_00_01,N,R1,NN,J__Doe_00_01",
                            ]))

    with open("./projects/J.Doe_00_01/P001_102_index6/120924_AC003CCCXX/SampleSheet.csv", "w") as fh:
        fh.write("\n".join(["FCID,Lane,SampleID,SampleRef,Index,Description,Control,Recipe,Operator,SampleProject",
                            "C003CCCXX,2,P001_102_index6,hg19,ACAGTG,J__Doe_00_01,N,R1,NN,J__Doe_00_01"
                            ]))
    with open("./projects/J.Doe_00_01/P001_102_index6/121015_BB002BBBXX/SampleSheet.csv", "w") as fh:
        fh.write("\n".join(["FCID,Lane,SampleID,SampleRef,Index,Description,Control,Recipe,Operator,SampleProject",
                            "C003CCCXX,2,P001_102_index6,hg19,ACAGTG,J__Doe_00_01,N,R1,NN,J__Doe_00_01"
                            ]))

def tearDownModule():
    pass
    # if os.path.exists("projects"):
    #     shutil.rmtree("projects")

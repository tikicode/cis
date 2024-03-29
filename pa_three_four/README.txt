Source Files
_____________
cis.cov_tree : This file contains the class CovTreeNode to store the surface mesh data points
               It also contains the ICP method to find the closest point in the Covariance Tree
cis.frame : Contains a Frame class and methods for frame transformations
cis.icp : Contains methods for computing linear ICP
cis.pc_io : This file contains the methods for file reading and writing
cis.registration : This file contains a method for point cloud registration
cis.thang : This file contains the class and methods for a Thang (Thing) object to store triangles
               from the surface mesh given
test.test_cov_tree : This file contains the test cases for the CovTreeNode class
test.test_generator : This file contains a random frame generator for testing registration
test.test_icp : This file contains the test cases for the ICP method
test.test_registration : This file contains the test cases for the registration method
test.test_thang : This file contains the test cases for the Thang(Thing) class

pa3_run_all.sh : Shell script to run find the output for all datasets once
pa_three.py : The executable Program for this project
pa_four.py: The executable program for the second part of this project

Setup
______
Before running, please execute the following from the top level directory
conda env -f create environment.yml
conda activate CIS2022

PA3 Instructions for Running Individual Data
____________________________________________
The executable is located directly under the PROGRAMS folder.

cd PROGRAMS
Usage: python pa_three.py -n FILENAME -t SAMPLE_TYPE -o OUTPUT_DIRECTORY -d DATA_DIRECTORY

Options:
    --data_dir, -d TXT              The input data directory (default: DATA/)
    --sample_readings_type -t TXT   The sample reading type (default: Debug)
    --output_dir -o TXT             The output directory (default: ../OUTPUT/PA3)
    --name -n TXT                   The file name (default: PA3-A-Debug)

Example: python pa_three.py -n PA3-G -t Unknown

PA3 Instructions for Running All Data
_____________________________________
The shell script is localed directly under the PROGRAMS folder
cd PROGRAMS
Usage: /bin/bash pa3_run_all.sh

Instructions for Testing
________________________
The unit test cases are located directly under the TEST folder
cd PROGRAMS
Usage: python -m pytest

PA4 Instructions for Running Individual Data
____________________________________________
The executable is located directly under the PROGRAMS folder.

cd PROGRAMS
Usage: python pa_four.py -n FILENAME -t SAMPLE_TYPE -o OUTPUT_DIRECTORY -d DATA_DIRECTORY

Options:
    --data_dir, -d TXT              The input data directory (default: DATA/)
    --sample_readings_type -t TXT   The sample reading type (default: Debug)
    --output_dir -o TXT             The output directory (default: ../OUTPUT/PA3)
    --name -n TXT                   The file name (default: PA3-A-Debug)

Example: python pa_three.py -n PA4-H -t Unknown

PA4 Instructions for Running All Data
_____________________________________
The shell script is localed directly under the PROGRAMS folder
cd PROGRAMS
Usage: /bin/bash pa4_run_all.sh

Instructions for Testing
________________________
The unit test cases are located directly under the TEST folder
cd PROGRAMS
Usage: python -m pytest
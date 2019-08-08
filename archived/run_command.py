# This file is used to generate test data by running commands in Python
# reference: https://stackoverflow.com/questions/9003522/writing-command-line-output-to-file

import os
os.system('faker -r=3 -s=";" profile > out.txt')
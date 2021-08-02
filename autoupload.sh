#!/bin/bash

source Venv1/bin/activate
cd /home/petin/python3_prgs_1/OpenVino01
python3 pets04.py --prototxt mobilenet-ssd.prototxt --model mobilenet-ssd.caffemodel --show True -c 0.3


#!/bin/bash

ffmpeg -f image2 -pattern_type glob -r 10 -i /home/petin/python3_prgs_1/OpenVino01/cam1/$(date +%d-%m-%Y)/'*.jpg' -y  /home/petin/python3_prgs_1/OpenVino01/cam2-$(date +%d-%m-%Y).mp4
ffmpeg -f image2 -pattern_type glob -r 10 -i /home/petin/python3_prgs_1/OpenVino01/cam2/$(date +%d-%m-%Y)/'*.jpg' -y  /home/petin/python3_prgs_1/OpenVino01/cam2-$(date +%d-%m-%Y).mp4
ffmpeg -f image2 -pattern_type glob -r 10 -i /home/petin/python3_prgs_1/OpenVino01/cam3/$(date +%d-%m-%Y)/'*.jpg' -y  /home/petin/python3_prgs_1/OpenVino01/cam3-$(date +%d-%m-%Y).mp4
ffmpeg -f image2 -pattern_type glob -r 10 -i /home/petin/python3_prgs_1/OpenVino01/cam4/$(date +%d-%m-%Y)/'*.jpg' -y  /home/petin/python3_prgs_1/OpenVino01/cam4-$(date +%d-%m-%Y).mp4

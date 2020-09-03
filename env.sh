#!/bin/bash
pip install tqdm==4.48.2
pip install urllib3==1.25.10
pip install requests==2.24.0
cd rpms && yum install parallel-20150522-1.el7.cern.noarch.rpm

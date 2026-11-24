#!/bin/bash

echo "========================================"
echo "       BASH SYSTEM INFORMATION"
echo "========================================"

echo "Operating System:"
uname -s

echo ""

echo "Kernel Version:"
uname -r

echo ""

echo "System Architecture:"
uname -m

echo ""

echo "Hostname:"
hostname

echo ""

echo "Python Version:"
python3 --version

echo ""

echo "Current Date:"
date

echo ""

echo "Current Directory:"
pwd

echo ""

echo "Memory Information:"

if command -v free >/dev/null 2>&1
then
    free -h
else
    echo "Memory information unavailable."
fi

echo ""

echo "Disk Information:"

if command -v df >/dev/null 2>&1
then
    df -h .
else
    echo "Disk information unavailable."
fi

echo ""
echo "========================================"
echo "          END SYSTEM INFORMATION"
echo "========================================"

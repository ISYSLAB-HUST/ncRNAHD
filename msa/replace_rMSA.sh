#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

if [ ! -d "rMSA" ]; then
    echo "Error: rMSA directory not found. Please run setup_rmsa.sh first."
    exit 1
fi

echo "Backing up original rMSA.pl..."
cp rMSA/rMSA.pl rMSA/rMSA.pl.backup

echo "Replacing rMSA.pl with custom version..."
cp msa/rMSA.pl rMSA/rMSA.pl

echo "rMSA.pl replacement completed!"

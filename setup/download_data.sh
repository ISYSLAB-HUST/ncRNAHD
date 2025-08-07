#!/bin/bash

# 设置下载目录
DOWNLOAD_DIR="./data"
mkdir -p $DOWNLOAD_DIR
cd $DOWNLOAD_DIR

# 下载RNACentral数据文件
echo "正在下载RNACentral数据文件..."
wget -O rnacentral_active.fasta.gz https://ftp.ebi.ac.uk/pub/databases/RNAcentral/releases/24.0/sequences/rnacentral_active.fasta.gz

# 检查下载是否成功
if [ $? -eq 0 ]; then
    echo "下载完成！"
else
    echo "下载失败！"
    exit 1
fi

# 解压文件
echo "正在解压文件..."
gunzip rnacentral_active.fasta.gz

# 检查解压是否成功
if [ $? -eq 0 ]; then
    echo "解压完成！"
else
    echo "解压失败！"
    exit 1
fi

# 调用Python脚本处理数据
echo "正在处理RNA序列..."
python ../setup/process_rna_sequences.py

echo "所有步骤完成！"
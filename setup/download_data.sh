#!/bin/bash

# Set download directory
DOWNLOAD_DIR="./data"
mkdir -p $DOWNLOAD_DIR
cd $DOWNLOAD_DIR

# Download RNACentral data file
echo "Downloading RNACentral data file..."
wget -O rnacentral_active.fasta.gz https://ftp.ebi.ac.uk/pub/databases/RNAcentral/releases/24.0/sequences/rnacentral_active.fasta.gz

# Check if download was successful
if [ $? -eq 0 ]; then
    echo "Download completed!"
else
    echo "Download failed!"
    exit 1
fi

# Extract file
echo "Extracting file..."
gunzip rnacentral_active.fasta.gz

# Check if extraction was successful
if [ $? -eq 0 ]; then
    echo "Extraction completed!"
else
    echo "Extraction failed!"
    exit 1
fi

# Call Python script to process data
echo "Processing RNA sequences..."
python ../setup/process_rna_sequences.py

echo "All steps completed!"

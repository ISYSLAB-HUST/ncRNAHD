#!/bin/bash

echo "Setting up rMSA..."
git clone https://github.com/pylelab/rMSA
cd rMSA
./database/script/update.sh

echo "rMSA setup completed!"
echo "Run 'bash msa/replace_rmsa.sh' to replace rMSA.pl with our custom version"
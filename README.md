# ncRNAHD: Non-coding RNA Homolog Detection

ncRNAHD is a tool for detecting homologous non-coding RNA sequences using deep learning embeddings and efficient similarity search.

## Features

- Deep learning-based RNA sequence embedding using ncRNABert
- Efficient similarity search with FAISS indexing
- Multiple sequence alignment (MSA) generation support

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/ISYSLAB-HUST/ncRNAHD
cd ncRNAHD
```

### 2. Create conda environment
```bash
conda env create -f environment.yml
conda activate ncRNAHD
```

### 3. Download and process RNACentral database
```bash
bash setup/download_data.sh
python process_rna_sequences.py
```

### 4. Generate embeddings for the database
```bash
python embedding/generate_embeddings.py
```

### 5. Build FAISS index
```bash
python indexing/build_faiss_index.py
```

## Usage

### Basic homolog search
```bash
python homolog_search.py --query_fasta your_query.fasta --output_dir results

# example1:
python homolog_search.py --query_fasta examples/5kh8.fasta --output_dir results
# example2:
python homolog_search.py --query_fasta examples/batch_query.fasta --output_dir results
```



## MSA Generation (Optional)

### Option 1: Lightweight rMSA Implementation (default)
```bash
# Setup rMSA
bash msa/setup_rmsa.sh

# Replace with custom rMSA.pl
bash msa/replace_rmsa.sh

# Generate MSA (replace "5kh8" with your actual sequence ID)
cd rMSA
# 1. Format the candidate database
database/script/makeblastdb -in ../results/Homologs_your_query.fasta -parse_seqids -hash_index -dbtype nucl
# 2. Generate MSA
perl rMSA.pl your_query.fasta -db1=../results/Homologs_your_query.fasta -cpu=16
# 3. A3m format (Optional)
# perl ${WORK_DIR}/bin/reformat.pl fas a3m -l 10000 your_query.afa your_query.a3m

# Complete example:
database/script/makeblastdb -in ../results/Homologs_5kh8.fasta -parse_seqids -hash_index -dbtype nucl
perl rMSA.pl 5kh8.fasta -db1=../results/Homologs_5kh8.fasta -cpu=16
# perl ${WORK_DIR}/bin/reformat.pl fas a3m -l 10000 5kh8.afa 5kh8.a3m
```

### Option 2: Using trRosettaRNA2 script
```bash
# Setup trRosettaRNA2
bash msa/setup_trrosetta.sh

# Generate MSA using ncRNAHD candidates as database (adjust CPU cores as needed)
cd trRosettaRNA2
bash scripts/search_MSA.sh your_query.fasta output_msa_dir ../results/Homologs_your_query.fasta 16

# Example: if your query sequence ID is "5kh8", using 16 CPU cores
bash scripts/search_MSA.sh 5kh8.fasta msa_results ../results/Homologs_5kh8.fasta 16
```

## File Structure

```
ncRNAHD/
├── homolog_search.py          # Main search tool
├── environment.yml            # Conda environment configuration
├── README.md                  # This file
├── setup/                     # Data download and preprocessing scripts
│   ├── download_data.sh
│   └── process_rna_sequences.py
├── embedding/                 # Embedding generation
│   └── generate_embeddings.py
├── indexing/                  # FAISS index building
│   └── build_faiss_index.py
├── search/                    # Search components
│   ├── embedding_generator.py
│   └── faiss_searcher.py
├── msa/                       # MSA generation tools
│   ├── setup_rmsa.sh
│   ├── setup_trrosetta.sh
│   ├── replace_rmsa.sh
│   └── rMSA.pl
├── data/                      # Generated data files (created during setup)
│   ├── rnacentral_active.fasta
│   ├── rnacentral_active_processed.fasta
│   ├── rna_embeddings.npy
│   ├── trained_index.faiss
│   ├── whiten_params.npz
│   └── sequence_index.json
├── results/                   # Search results (created during search)
│   └── Homologs_{sequence_id}.fasta    # Candidate sequences for each query
└── examples/                  # Example query files
    ├── batch_query.fasta
    ├── 5kh8.fasta
    └── Homologs_5kh8.fasta
    


```

## Requirements

- Python 3.12
- PyTorch
- BioPython
- FAISS
- ncRNABert
- See `environment.yml` for complete dependencies



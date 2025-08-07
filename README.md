# ncRNAHD: Non-coding RNA Homolog Detection

ncRNAHD is a tool for detecting homologous non-coding RNA sequences using deep learning embeddings and efficient similarity search.

## Features

- Deep learning-based RNA sequence embedding using ncRNABert
- Efficient similarity search with FAISS indexing
- Large-scale RNA database processing
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
python homolog_search.py --query_fasta examples/query.fasta --output_dir results
```

### Custom parameters
```bash
python homolog_search.py \
    --query_fasta your_query.fasta \
    --output_dir your_results \
    --topk 50000
```

## MSA Generation (Optional)

### Option 1: Using rMSA (default)
```bash
# Setup rMSA
bash msa/setup_rmsa.sh

# Replace with custom rMSA.pl
bash msa/replace_rmsa.sh

# Generate MSA (use detected homologs as input)
cd rMSA
perl rMSA.pl -i ../results/candidates_1_your_query.fasta -o output_msa
```

### Option 2: Using trRosettaRNA2
```bash
# Setup trRosettaRNA2
bash msa/setup_trrosetta.sh

# Generate MSA
cd trRosettaRNA2
bash scripts/search_MSA.sh your_query.fasta
```

## File Structure

```
ncRNAHD/
├── homolog_search.py   # Main search tool
├── setup/              # Data download and preprocessing
├── embedding/          # Embedding generation
├── indexing/           # FAISS index building
├── search/             # Search components
├── msa/               # MSA generation tools
├── data/              # Generated data files
├── results/           # Search results
└── examples/          # Example query files
```

## Requirements

- Python 3.12
- PyTorch
- BioPython
- FAISS
- ncRNABert
- See `environment.yml` for complete dependencies

## Citation

If you use ncRNAHD in your research, please cite:
[Your paper citation here]

## License

[Your license here]
```

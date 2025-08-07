# ncRNAHD: Non-coding RNA Homolog Detection

ncRNAHD (Non-coding RNA Homolog Detection) is a deep learning-based tool for efficient homolog detection of non-coding RNA sequences. It leverages ncRNABert embeddings and FAISS indexing to enable fast similarity search across large RNA databases.

## Features

- **Deep Learning Embeddings**: Uses ncRNABert to generate high-quality RNA sequence representations
- **Efficient Similarity Search**: Employs FAISS indexing with whitening transformation for fast homolog detection
- **Large-scale Processing**: Capable of handling millions of RNA sequences
- **Flexible Query Interface**: Supports batch processing and customizable search parameters

## Installation

### Prerequisites

- Python 3.12
- CUDA-compatible GPU (recommended)

### Environment Setup

1. Clone the repository:

```bash
git clone https://github.com/ISYSLAB-HUST/ncRNAHD.git
cd ncRNAHD
```

2. Create and activate conda environment:

```bash
conda env create -f environment.yml
conda activate ncRNAHD
```

## Quick Start

### 1. Download and Process Data

```bash
# Download RNACentral data
bash scripts/download_data.sh

# Process sequences (filter by length and truncate)
python scripts/process_sequences.py
```

### 2. Generate Embeddings

```bash
python scripts/generate_embeddings.py
```

### 3. Build Search Index

```bash
python scripts/build_index.py
```

### 4. Search for Homologs

```bash
# Basic usage
python scripts/search_homologs.py

# Custom query file
python scripts/search_homologs.py --query_fasta your_queries.fasta

# Specify output directory and top-k results
python scripts/search_homologs.py --query_fasta queries.fasta --output_dir results --topk 50000
```

## Usage Examples

### Example 1: Default Search

```bash
python scripts/search_homologs.py
```

### Example 2: Custom Parameters

```bash
python scripts/search_homologs.py \
    --query_fasta my_sequences.fasta \
    --output_dir homolog_results \
    --topk 10000 \
    --batch_size 5
```

## Command Line Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--query_fasta` | Query sequence FASTA file | `query.fasta` |
| `--output_dir` | Output directory | `candidates` |
| `--batch_size` | Processing batch size | All sequences |
| `--topk` | Number of similar sequences to return | 100000 |

## Dependencies

- pytorch
- numpy, pandas, scikit-learn
- biopython
- ncRNABert
- faiss

## Contact

For questions or issues, please contact:

- GitHub: [@elkerist](https://github.com/elkerist)
- Repository: [ISYSLAB-HUST/ncRNAHD](https://github.com/ISYSLAB-HUST/ncRNAHD)
```

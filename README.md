# ncRNAHD: Non-coding RNA Homolog Detection

ncRNAHD (Non-coding RNA Homolog Detection) is a deep learning-based tool for efficient homolog detection of non-coding RNA sequences. It leverages ncRNABert embeddings and FAISS indexing to enable fast similarity search across large RNA databases.

## Features

- **Deep Learning Embeddings**: Uses ncRNABert to generate high-quality RNA sequence representations
- **Efficient Similarity Search**: Employs FAISS indexing with whitening transformation for fast homolog detection
- **Large-scale Processing**: Capable of handling millions of RNA sequences
- **Flexible Query Interface**: Supports batch processing and customizable search parameters
- ## Installation

### Prerequisites

- Python 3.12
- CUDA-compatible GPU (recommended)
- Minimum 16GB RAM

### Environment Setup

1. Clone the repository:
git clone https://github.com/ISYSLAB-HUST/ncRNAHD.git
cd ncRNAHD
2. Create and activate conda environment:
conda env create -f environment.yml
conda activate ncRNAHD
## Quick Start

### 1. Download and Process Data

Download RNACentral database and preprocess sequences:
# Download RNACentral data
bash scripts/download_data.sh

# Process sequences (filter by length and truncate)
python scripts/process_sequences.py
### 2. Generate Embeddings

Generate ncRNABert embeddings for the database:
python scripts/generate_embeddings.py
### 3. Build Search Index

Create FAISS index with whitening transformation:
python scripts/build_index.py
### 4. Search for Homologs

Search for homologs of query sequences:
# Basic usage
python scripts/search_homologs.py

# Custom query file
python scripts/search_homologs.py --query_fasta your_queries.fasta

# Specify output directory and top-k results
python scripts/search_homologs.py --query_fasta queries.fasta --output_dir results --topk 50000
## Usage Examples

### Example 1: Default Search
python scripts/search_homologs.py
This will process all sequences in `query.fasta` and return top 100,000 similar sequences.

### Example 2: Custom Parameters
python scripts/search_homologs.py \
    --query_fasta my_sequences.fasta \
    --output_dir homolog_results \
    --topk 10000 \
    --batch_size 5
### Example 3: Large-scale Batch Processing
python scripts/search_homologs.py \
    --query_fasta large_query_set.fasta \
    --batch_size 10 \
    --topk 50000
## Command Line Options

### search_homologs.py

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--query_fasta` | Query sequence FASTA file | `query.fasta` |
| `--whiten_params` | Whitening parameters file | `whiten_params_NoZscoreWhiteIndexFlatIP.npz` |
| `--trained_index` | FAISS index file | `trained_index_NoZscoreWhiteIndexFlatIP.faiss` |
| `--database_fasta` | Database FASTA file | `rnacentral_active_filtered_truncated_merged.fasta` |
| `--output_dir` | Output directory | `candidates` |
| `--batch_size` | Processing batch size | All sequences |
| `--topk` | Number of similar sequences to return | 100000 |
## File Descriptions

### Scripts

- **`download_data.sh`**: Downloads and extracts RNACentral database
- **`process_sequences.py`**: Filters short sequences (<30 nt) and truncates long sequences (>1024 nt)
- **`generate_embeddings.py`**: Generates ncRNABert embeddings for all sequences
- **`build_index.py`**: Creates whitened embeddings and builds FAISS index
- **`search_homologs.py`**: Performs similarity search and retrieves homolog candidates

### Output Files

- **`rnacentral_active_filtered_truncated_merged.fasta`**: Processed sequence database
- **`rna_embeddings_merged.npy`**: Raw ncRNABert embeddings
- **`trained_index_NoZscoreWhiteIndexFlatIP.faiss`**: FAISS search index
- **`whiten_params_NoZscoreWhiteIndexFlatIP.npz`**: Whitening transformation parameters
- **`candidates_*.fasta`**: Homolog candidates for each query sequence
## Multiple Sequence Alignment (MSA)

For downstream MSA analysis, you can use:

1. **rMSA**: Clone the rMSA repository and replace `rMSA.pl` with the provided version
2. **trRosettaRNA2**: Use `trRosettaRNA2/scripts/search_MSA.sh`

## Performance Notes

- **Memory Usage**: Approximately 8-16GB RAM for processing large databases
- **Processing Time**: ~40,000 sequences per progress report during embedding generation
- **GPU Acceleration**: Significantly faster with CUDA-compatible GPU

## Dependencies

Core dependencies are managed through conda:

- pytorch
- numpy, pandas, scikit-learn
- biopython
- ncRNABert
- faiss (via pip as faiss-gpu or faiss-cpu)
## Citation

If you use ncRNAHD in your research, please cite:
[Your paper citation will go here]
## Contact

For questions or issues, please contact:

- GitHub: [@elkerist](https://github.com/elkerist)
- Repository: [ISYSLAB-HUST/ncRNAHD](https://github.com/ISYSLAB-HUST/ncRNAHD)

## License

[Add your license information here]

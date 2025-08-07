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
- Minimum 16GB RAM

### Environment Setup

1. Clone the repository:

```bash
git clone https://github.com/ISYSLAB-HUST/ncRNAHD.git
cd ncRNAHD


**第二部分：**
```markdown
## Quick Start

### 1. Download and Process Data

Download RNACentral database and preprocess sequences:

```bash
# Download RNACentral data
bash scripts/download_data.sh

# Process sequences (filter by length and truncate)
python scripts/process_sequences.py


**第三部分：**
```markdown
## Usage Examples

### Example 1: Default Search

```bash
python scripts/search_homologs.py


**第四部分：**
```markdown
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

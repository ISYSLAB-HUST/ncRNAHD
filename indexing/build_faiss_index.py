import numpy as np
import faiss
import os

def compute_kernel_bias(vecs, n_components=384):
    mu = vecs.mean(axis=0, keepdims=True).astype(np.float64)
    cov = np.cov(vecs.T, dtype=np.float64)
    u, s, vh = np.linalg.svd(cov)
    W = np.dot(u, np.diag(1 / np.sqrt(s))).astype(np.float64)
    return W[:, :n_components], -mu

def build_index():
    # File path
    emb_file = "./data/rna_embeddings.npy"
    
    print("Loading complete data...")
    # Load all data at once
    embeddings = np.load(emb_file).astype(np.float64)
    total_rows, dim = embeddings.shape
    print(f"Total data: {total_rows} rows, dimension: {dim}")
    
    # Handle NaN values
    print("Handling NaN values...")
    # Calculate mean for each column (ignoring NaN)
    col_mean = np.nanmean(embeddings, axis=0)
    # Fill NaN with column mean
    embeddings = np.where(np.isnan(embeddings), col_mean, embeddings)
    
    # Compute whitening parameters
    print("Computing whitening parameters...")
    kernel, bias = compute_kernel_bias(embeddings, n_components=384)
    
    # Perform whitening transformation
    print("Performing whitening transformation...")
    whitened_embeddings = (embeddings + bias).dot(kernel).astype(np.float32)
    del embeddings  # Release original data memory
    
    # L2 normalization
    print("L2 normalization...")
    faiss.normalize_L2(whitened_embeddings)
    
    # Create index
    print("Creating index...")
    dim_whitened = kernel.shape[1]  # Dimension after whitening (384)
    
    index = faiss.IndexFlatIP(dim_whitened)
    
    # Add data to index
    print("Adding data to index...")
    index.add(whitened_embeddings)
    
    # Save index and parameters
    print("Saving index and parameters...")
    faiss.write_index(index, "./data/trained_index.faiss")
    np.savez("./data/whiten_params.npz", 
             kernel=kernel, bias=bias, col_mean=col_mean)
    
    print("Index construction completed!")

if __name__ == "__main__":
    build_index()

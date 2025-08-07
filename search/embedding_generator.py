from ncRNABert.pretrain import load_ncRNABert
from ncRNABert.utils import BatchConverter
import torch
import numpy as np
import faiss
from Bio import SeqIO

class RNAEmbeddingGenerator:
    def __init__(self, whiten_params_path="./data/whiten_params.npz"):
        """Initialize RNA embedding generator"""
        print("Initializing RNA embedding generator...")
        
        # Load whitening parameters
        print("Loading whitening parameters...")
        whiten_params = np.load(whiten_params_path)
        self.kernel = whiten_params['kernel']
        self.bias = whiten_params['bias']
        self.col_mean = whiten_params['col_mean']
        print(f"Whitening parameters loaded: kernel shape={self.kernel.shape}, bias shape={self.bias.shape}")
        
        # Load model
        print("Loading ncRNABert model...")
        self.model = load_ncRNABert()
        print("ncRNABert model loaded")

    def apply_whitening(self, embedding, kernel, bias, col_mean):
        """Apply whitening transformation"""
        # Ensure float64 type for computation
        embedding = embedding.astype(np.float64)
        
        # Handle NaN values (fill with column mean from training)
        embedding = np.where(np.isnan(embedding), col_mean, embedding)
        
        # Apply whitening transformation
        whitened = (embedding.reshape(1, -1) + bias).dot(kernel)
        
        # Convert to float32 and apply L2 normalization
        whitened = whitened.astype(np.float32)
        faiss.normalize_L2(whitened)
        
        return whitened.squeeze()

    def generate_embeddings(self, fasta_file):
        """Generate embeddings from FASTA file"""
        print(f"Generating embeddings from {fasta_file}...")
        
        embeddings = []
        identifiers = []
        num = 1
        
        for record in SeqIO.parse(fasta_file, "fasta"):
            seq_id = record.id
            sequence = str(record.seq)
            
            print(f"Processing sequence {num}: {seq_id}")
            
            # Prepare single sequence data
            data = [(seq_id, sequence)]
            
            # Convert data format
            ids, batch_token, lengths = BatchConverter(data)
            
            # Get embeddings
            with torch.no_grad():
                results = self.model(batch_token, lengths, repr_layers=[24])
            
            # Generate sequence representation (through average pooling)
            token_representations = results["representations"][24]
            sequence_representation = token_representations[0, :len(sequence)].mean(0)
            
            # Convert to numpy array
            embedding = sequence_representation.cpu().numpy()
            
            # Apply whitening transformation
            whitened_embedding = self.apply_whitening(embedding, self.kernel, self.bias, self.col_mean)
            
            embeddings.append(whitened_embedding)
            identifiers.append(f"_{num}_{seq_id}")
            
            print(f"Generated whitened embedding, shape: {whitened_embedding.shape}")
            num += 1
        
        print(f"Completed! Processed {num-1} sequences in total")
        return embeddings, identifiers

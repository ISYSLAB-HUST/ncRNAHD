import numpy as np
import faiss
from Bio import SeqIO
import os
import json
import mmap
import time

class OptimizedSearcher:
    def __init__(self, trained_index="./data/trained_index.faiss", 
                 fasta_path="./data/rnacentral_active_processed.fasta", 
                 index_path="./data/sequence_index.json"):
        # Load FAISS index
        print("Loading FAISS index...")
        start_time = time.time()
        self.index = faiss.read_index(trained_index)
        index_load_time = time.time() - start_time
        print(f"FAISS index loaded, time taken: {index_load_time:.2f} seconds")
        
        # Load sequence position index
        print("Loading sequence index...")
        start_time = time.time()
        if not os.path.exists(index_path):
            print("Sequence index does not exist, creating...")
            self._create_sequence_index(fasta_path, index_path)
        
        with open(index_path, 'r') as f:
            self.seq_positions = json.load(f)
        
        # Create memory-mapped file
        self.fasta_file = open(fasta_path, 'r')
        self.fasta_mmap = mmap.mmap(self.fasta_file.fileno(), 0, access=mmap.ACCESS_READ)
        
        seq_index_time = time.time() - start_time
        print(f"Sequence index loaded, {len(self.seq_positions)} sequences, time taken: {seq_index_time:.2f} seconds")
    
    def _create_sequence_index(self, fasta_path, index_path):
        """Create sequence position index file"""
        print("Analyzing FASTA file to create index...")
        seq_positions = []
        
        with open(fasta_path, 'rb') as f:  # Use binary mode to avoid tell() issues
            current_seq_start = None
            line_count = 0
            
            while True:
                pos = f.tell()  # Record current position
                line = f.readline()
                
                if not line:  # End of file
                    break
                
                line = line.decode('utf-8').strip()
                line_count += 1
                
                if line_count % 1000000 == 0:  # Progress indicator
                    print(f"Processed {line_count} lines...")
                
                if line.startswith('>'):
                    # Save previous sequence info (if exists)
                    if current_seq_start is not None:
                        seq_positions.append({
                            'start': current_seq_start,
                            'end': pos
                        })
                    
                    # Start new sequence
                    current_seq_start = pos
            
            # Save last sequence
            if current_seq_start is not None:
                seq_positions.append({
                    'start': current_seq_start,
                    'end': f.tell()
                })
        
        # Save index to JSON file
        print(f"Saving sequence index to {index_path}...")
        with open(index_path, 'w') as f:
            json.dump(seq_positions, f)
        
        print(f"Sequence index created, {len(seq_positions)} sequences")
    
    def get_sequence_by_index(self, idx):
        """Get single sequence by index"""
        if idx >= len(self.seq_positions):
            raise IndexError(f"Sequence index {idx} out of range")
        
        pos_info = self.seq_positions[idx]
        self.fasta_mmap.seek(pos_info['start'])
        
        # Read sequence data
        length = pos_info['end'] - pos_info['start']
        sequence_data = self.fasta_mmap.read(length).decode('utf-8')
        
        return sequence_data.strip()
    
    def get_sequences_batch(self, indices):
        """Batch get sequences, optimized IO"""
        sequences = []
        
        # Sort by file position to reduce random IO
        sorted_indices = sorted(enumerate(indices), key=lambda x: self.seq_positions[x[1]]['start'])
        
        results = [None] * len(indices)
        
        for original_pos, idx in sorted_indices:
            sequence = self.get_sequence_by_index(idx)
            results[original_pos] = sequence
        
        return results
    
    def search_batch(self, batch_embeddings, topk=100000):
        """Batch search - return indices, delay sequence retrieval"""
        print(f"Executing batch search, batch size: {len(batch_embeddings)}")
        start_time = time.time()
        
        # Stack batch embeddings into matrix
        batch_matrix = np.vstack(batch_embeddings)
        
        # Batch retrieval - only return indices
        distances, indices = self.index.search(batch_matrix, topk)
        search_time = time.time() - start_time
        print(f"FAISS search completed, time taken: {search_time:.2f} seconds")
        
        return distances, indices
    
    def save_results_with_sequences(self, indices_list, identifiers, output_dir):
        """Get sequences by indices and save results"""
        print("Getting sequences by indices and saving results...")
        start_time = time.time()
        
        for identifier, indices in zip(identifiers, indices_list):
            print(f"Processing query {identifier}, getting {len(indices)} sequences...")
            
            # Batch get sequences
            seq_start_time = time.time()
            sequences = self.get_sequences_batch(indices)
            seq_time = time.time() - seq_start_time
            print(f"Sequence retrieval completed, time taken: {seq_time:.2f} seconds")
            
            # Save to file
            output_fasta_path = os.path.join(output_dir, f"candidates{identifier}.fasta")
            with open(output_fasta_path, "w") as output_handle:
                for seq_data in sequences:
                    output_handle.write(seq_data + "\n")
            
            print(f"Saved to {output_fasta_path}")
        
        total_save_time = time.time() - start_time
        print(f"All results saved, time taken: {total_save_time:.2f} seconds")
    
    def __del__(self):
        """Clean up resources"""
        if hasattr(self, 'fasta_mmap'):
            self.fasta_mmap.close()
        if hasattr(self, 'fasta_file'):
            self.fasta_file.close()

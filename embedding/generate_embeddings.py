from ncRNABert.pretrain import load_ncRNABert
from ncRNABert.utils import BatchConverter
import torch
from Bio import SeqIO
import numpy as np
import sys

def process_single_sequence(seq_id, sequence, model, device):
    """处理单条序列"""
    batch = [(seq_id, sequence)]
    ids, batch_token, lengths = BatchConverter(batch)
    batch_token = batch_token.to(device)
    lengths = lengths.to(device)
    
    with torch.no_grad():
        results = model(batch_token, lengths, repr_layers=[24])
    token_representations = results["representations"][24]
    
    seq_rep = token_representations[0].mean(0)
    return seq_rep.cpu()

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_ncRNABert().to(device)
    model.eval()

    input_file = "./data/rnacentral_active_processed.fasta"
    output_file = "./data/rna_embeddings.npy"
    
    all_embeddings = []
    total_processed = 0
    report_interval = 40000
    
    for record in SeqIO.parse(input_file, "fasta"):
        embedding = process_single_sequence(record.id, str(record.seq), model, device)
        all_embeddings.append(embedding)
        total_processed += 1
        
        if total_processed % report_interval == 0:
            print(f"Processed {total_processed} sequences", flush=True)
    
    all_embeddings_np = np.array([embedding.numpy() for embedding in all_embeddings])
    np.save(output_file, all_embeddings_np)
    print(f"Completed. Total sequences processed: {total_processed}", flush=True)

if __name__ == "__main__":
    main()
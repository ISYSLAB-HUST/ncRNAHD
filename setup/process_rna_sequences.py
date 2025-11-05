from Bio import SeqIO

def filter_fasta_by_length(input_file, output_file, min_length=30):
    """
    Filter FASTA file, keeping sequences with length greater than or equal to specified length
    
    Args:
        input_file (str): Input FASTA file path
        output_file (str): Output FASTA file path
        min_length (int): Minimum sequence length, default is 30
    """
    # Counters
    total_sequences = 0
    kept_sequences = 0
    
    # Use SeqIO to filter sequences
    with open(output_file, 'w') as out_handle:
        for record in SeqIO.parse(input_file, "fasta"):
            total_sequences += 1
            if len(record.seq) >= min_length:
                kept_sequences += 1
                SeqIO.write(record, out_handle, "fasta")
    
    # Print statistics
    print(f"Total sequences: {total_sequences}")
    print(f"Kept sequences: {kept_sequences}")
    print(f"Filtered out sequences: {total_sequences - kept_sequences}")

def truncate_long_sequences(input_file, output_file, max_length=1024):
    """
    Process FASTA file, truncate sequences longer than max_length to max_length
    Keep sequences not exceeding max_length unchanged
    
    Args:
        input_file (str): Input FASTA file path
        output_file (str): Output FASTA file path
        max_length (int): Maximum sequence length, default is 1024
    """
    # Counters
    total_sequences = 0
    truncated_sequences = 0
    
    # Process and write sequences
    with open(output_file, 'w') as out_handle:
        for record in SeqIO.parse(input_file, "fasta"):
            total_sequences += 1
            
            # Check if sequence needs truncation
            if len(record.seq) > max_length:
                truncated_sequences += 1
                # Create truncated record
                record.seq = record.seq[:max_length]
                # Optionally add annotation in description to indicate sequence was truncated
                record.description = record.description + f" [Truncated from original length to {max_length}bp]"
                
            # Write sequence (whether truncated or not)
            SeqIO.write(record, out_handle, "fasta")
    
    # Print statistics
    print(f"Total processed sequences: {total_sequences}")
    print(f"Truncated sequences: {truncated_sequences}")
    print(f"Unmodified sequences: {total_sequences - truncated_sequences}")

if __name__ == "__main__":
    # Execute filtering
    print("Step 1: Filtering short sequences...")
    input_file = "./data/rnacentral_active.fasta"
    filtered_file = "./data/rnacentral_active_filtered.fasta"
    filter_fasta_by_length(input_file, filtered_file, min_length=30)
    
    print("\nStep 2: Truncating long sequences...")
    output_file = "./data/rnacentral_active_processed.fasta"
    truncate_long_sequences(filtered_file, output_file, max_length=1024)
    
    print("\nProcessing completed!")

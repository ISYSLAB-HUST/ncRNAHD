"""
RNA Homolog Detection Tool

Usage examples:
1. Default run:
   python homolog_search.py

2. Custom query file:
   python homolog_search.py --query_fasta my_queries.fasta

3. Custom parameters:
   python homolog_search.py --query_fasta queries.fasta --output_dir results --topk 50000
"""

import argparse
import sys
import os
import time

# Add search directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'search'))

from embedding_generator import RNAEmbeddingGenerator
from faiss_searcher import OptimizedSearcher

def main():
    parser = argparse.ArgumentParser(description='RNA Homolog Detection Tool')
    parser.add_argument('--query_fasta', type=str, default="./examples/query.fasta",
                       help='Query sequence FASTA file path (default: ./examples/query.fasta)')
    parser.add_argument('--whiten_params', type=str, default="./data/whiten_params.npz",
                       help='Whitening parameters file path (default: ./data/whiten_params.npz)')
    parser.add_argument('--trained_index', type=str, default="./data/trained_index.faiss",
                       help='Trained FAISS index file path (default: ./data/trained_index.faiss)')
    parser.add_argument('--database_fasta', type=str, default="./data/rnacentral_active_processed.fasta",
                       help='Database FASTA file path (default: ./data/rnacentral_active_processed.fasta)')
    parser.add_argument('--index_path', type=str, default="./data/sequence_index.json",
                       help='Sequence index file path (default: ./data/sequence_index.json)')
    parser.add_argument('--output_dir', type=str, default="./results",
                       help='Output directory (default: ./results)')
    parser.add_argument('--batch_size', type=int, default=None,
                       help='Processing batch size, default is process all sequences at once')
    parser.add_argument('--topk', type=int, default=100000,
                       help='Number of similar sequences to return (default: 100000)')
    
    args = parser.parse_args()

    # Ensure output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    print("=" * 60)
    print("RNA Homolog Detection Tool")
    print("=" * 60)
    
    total_start_time = time.time()
    
    # Step 1: Generate embeddings
    print("\nStep 1: Generate query sequence embeddings")
    print("-" * 40)
    embedding_generator = RNAEmbeddingGenerator(args.whiten_params)
    query_embeddings, query_identifiers = embedding_generator.generate_embeddings(args.query_fasta)
    
    # Step 2: Initialize searcher
    print("\nStep 2: Initialize FAISS searcher")
    print("-" * 40)
    searcher = OptimizedSearcher(args.trained_index, args.database_fasta, args.index_path)
    
    # Step 3: Batch search
    print("\nStep 3: Execute similarity search")
    print("-" * 40)
    
    num_queries = len(query_embeddings)
    
    # Determine batch size
    if args.batch_size is None:
        BATCH_SIZE = num_queries  # Process all query sequences at once
        print(f"Using default batch size: {BATCH_SIZE} (all query sequences)")
    else:
        BATCH_SIZE = args.batch_size
        print(f"Using custom batch size: {BATCH_SIZE}")
    
    # Process query sequences in batches
    for batch_start in range(0, num_queries, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, num_queries)
        
        print(f"\nProcessing batch: queries {batch_start+1}-{batch_end}/{num_queries}")
        
        # Current batch embeddings and identifiers
        batch_embeddings = query_embeddings[batch_start:batch_end]
        batch_identifiers = query_identifiers[batch_start:batch_end]
        
        # Batch search
        distances, indices_batch = searcher.search_batch(batch_embeddings, topk=args.topk)
        
        # Display similarity scores
        for i, distance_row in enumerate(distances):
            print(f"Query {batch_identifiers[i]} similarity scores:", distance_row[:5])
        
        # Save results
        indices_list = [indices_batch[i] for i in range(len(batch_embeddings))]
        searcher.save_results_with_sequences(indices_list, batch_identifiers, args.output_dir)

    total_time = time.time() - total_start_time
    print("\n" + "=" * 60)
    print(f"All processing completed! Total time taken: {total_time:.2f} seconds")
    print(f"Processed {num_queries} query sequences")
    print(f"Results saved in directory: {args.output_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
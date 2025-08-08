## Methods

### ncRNAHD pipeline for homolog detection and MSA construction

We developed ncRNAHD, a pipeline for homologous non-coding RNA detection and multiple sequence alignment construction. The pipeline leverages our previously developed ncRNABert language model to replace traditional sequence alignment-based searches with efficient vector similarity searches, enabling rapid homolog identification from large-scale sequence databases.

#### Database preprocessing and embedding generation

The reference database was derived from RNACentral, filtered to retain sequences with lengths between 30-1024 nucleotides. The upper limit corresponds to ncRNABert's maximum input length, while the lower limit reduces noise from short fragments. Filtered sequences were converted to high-dimensional embeddings using ncRNABert in a one-time offline preprocessing step.

To optimize embeddings for similarity search, we applied principal component whitening transformation to decorrelate feature dimensions and reduce dimensionality to 384. The transformation was derived by calculating the mean vector and covariance matrix of all database embeddings. Through singular value decomposition of the covariance matrix, we obtained a whitening kernel matrix (W) and bias vector (negative mean). The processed embedding is computed as:

E<sub>processed</sub> = (E<sub>raw</sub> + bias) × W

where E<sub>raw</sub> is the raw ncRNABert output and W is truncated to 384 components.

#### Homolog retrieval via accelerated similarity search

We constructed a FAISS index using L2-normalized processed embeddings with IndexFlatIP, which performs maximum inner product search. Due to normalization, this is mathematically equivalent to cosine similarity search. Query sequences undergo identical preprocessing (ncRNABert encoding, whitening transformation, and L2 normalization) before searching the index to retrieve the top 100k most similar sequences as homolog candidates.

#### MSA construction strategies

Retrieved homologs were used to construct MSAs via two approaches offering different speed-quality trade-offs:

**Default strategy (customized rMSA)**: We modified the rMSA pipeline by removing search modules for Rfam and nt databases while preserving the core RNACentral processing logic. We replaced the full RNACentral database input with our 100k retrieved homologs, leveraging rMSA's sophisticated alignment algorithm on pre-filtered relevant sequences to maintain quality while drastically reducing runtime.

**Alternative strategy (trRosettaRNA2)**: We utilized trRosettaRNA2's search_MSA.sh script, directly substituting the default RNACentral database with our retrieved homolog set for faster processing.

#### MSA quality evaluation

MSA quality was assessed through intrinsic diversity metrics and extrinsic performance evaluation:

**Alignment diversity**: Measured using log(Neff), the logarithm of effective number of sequences after clustering at 80% sequence identity threshold.

**Structure prediction performance**: Generated MSAs served as input for trRosettaRNA structure prediction with default parameters. Predicted models were evaluated against native structures using all-atom RMSD (US-align), with TM-score (US-align) and lDDT (OpenStructure) as supplementary metrics for global and local accuracy assessment.


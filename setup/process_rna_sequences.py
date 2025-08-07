from Bio import SeqIO

def filter_fasta_by_length(input_file, output_file, min_length=30):
    """
    过滤FASTA文件，保留长度大于等于指定长度的序列
    
    参数:
        input_file (str): 输入FASTA文件路径
        output_file (str): 输出FASTA文件路径
        min_length (int): 最小序列长度，默认为30
    """
    # 计数器
    total_sequences = 0
    kept_sequences = 0
    
    # 使用SeqIO过滤序列
    with open(output_file, 'w') as out_handle:
        for record in SeqIO.parse(input_file, "fasta"):
            total_sequences += 1
            if len(record.seq) >= min_length:
                kept_sequences += 1
                SeqIO.write(record, out_handle, "fasta")
    
    # 打印统计信息
    print(f"总序列数: {total_sequences}")
    print(f"保留序列数: {kept_sequences}")
    print(f"过滤掉的序列数: {total_sequences - kept_sequences}")

def truncate_long_sequences(input_file, output_file, max_length=1024):
    """
    处理FASTA文件，将长度超过max_length的序列截断至max_length
    对于长度不超过max_length的序列保持不变
    
    参数:
        input_file (str): 输入FASTA文件路径
        output_file (str): 输出FASTA文件路径
        max_length (int): 最大序列长度，默认为1024
    """
    # 计数器
    total_sequences = 0
    truncated_sequences = 0
    
    # 处理并写入序列
    with open(output_file, 'w') as out_handle:
        for record in SeqIO.parse(input_file, "fasta"):
            total_sequences += 1
            
            # 检查序列是否需要截断
            if len(record.seq) > max_length:
                truncated_sequences += 1
                # 创建截断后的记录
                record.seq = record.seq[:max_length]
                # 可以选择在描述中添加注释，表明序列被截断
                record.description = record.description + f" [Truncated from original length to {max_length}bp]"
                
            # 写入序列（无论是否被截断）
            SeqIO.write(record, out_handle, "fasta")
    
    # 打印统计信息
    print(f"总处理序列数: {total_sequences}")
    print(f"被截断的序列数: {truncated_sequences}")
    print(f"未修改的序列数: {total_sequences - truncated_sequences}")

if __name__ == "__main__":
    # 执行过滤
    print("第一步：过滤短序列...")
    input_file = "./data/rnacentral_active.fasta"
    filtered_file = "./data/rnacentral_active_filtered.fasta"
    filter_fasta_by_length(input_file, filtered_file, min_length=30)
    
    print("\n第二步：截断长序列...")
    output_file = "./data/rnacentral_active_processed.fasta"
    truncate_long_sequences(filtered_file, output_file, max_length=1024)
    
    print("\n处理完成！")
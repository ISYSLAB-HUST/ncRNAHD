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
    # 文件路径
    emb_file = "./data/rna_embeddings.npy"
    
    print("加载完整数据...")
    # 一次性加载所有数据
    embeddings = np.load(emb_file).astype(np.float64)
    total_rows, dim = embeddings.shape
    print(f"数据总量: {total_rows}行, 维度: {dim}")
    
    # 处理NaN值
    print("处理NaN值...")
    # 计算每列的均值（忽略NaN）
    col_mean = np.nanmean(embeddings, axis=0)
    # 用列均值填充NaN
    embeddings = np.where(np.isnan(embeddings), col_mean, embeddings)
    
    # 计算白化参数
    print("计算白化参数...")
    kernel, bias = compute_kernel_bias(embeddings, n_components=384)
    
    # 执行白化变换
    print("执行白化变换...")
    whitened_embeddings = (embeddings + bias).dot(kernel).astype(np.float32)
    del embeddings  # 释放原始数据内存
    
    # L2归一化
    print("L2归一化...")
    faiss.normalize_L2(whitened_embeddings)
    
    # 创建索引
    print("创建索引...")
    dim_whitened = kernel.shape[1]  # 白化后的维度 (384)
    
    index = faiss.IndexFlatIP(dim_whitened)
    
    # 添加数据到索引
    print("添加数据到索引...")
    index.add(whitened_embeddings)
    
    # 保存索引和参数
    print("保存索引和参数...")
    faiss.write_index(index, "./data/trained_index.faiss")
    np.savez("./data/whiten_params.npz", 
             kernel=kernel, bias=bias, col_mean=col_mean)
    
    print("索引构建完成!")

if __name__ == "__main__":
    build_index()
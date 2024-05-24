#!/usr/bin/env python
import argparse
import h5py
import numpy as np
from genslm import GenSLM, SequenceDataset
from torch.utils.data import DataLoader
import torch
import os

description_text = "Script for embedding mRNA sequences using GenSLM and saving in HDF5 format."
parser = argparse.ArgumentParser(description=description_text)
parser.add_argument('-in', '--hdf5In', type=str, required=True, help='Path to the input HDF5 file containing mRNA sequences.')
parser.add_argument('-out','--hdf5Out', type=str, default=None, help='Path to save the embedded sequences in HDF5 format. If not provided, it will overwrite the input HDF5.')
args = parser.parse_args()

model = GenSLM("genslm_25M_patric", model_cache_dir="/project/mayocancerai/GenSLM") # Initialize GenSLM
model.eval()

def embed_with_genslm(seq):
    dataset = SequenceDataset([seq], model.seq_length, model.tokenizer)
    dataloader = DataLoader(dataset, batch_size=1)
    with torch.no_grad():
        for batch in dataloader:
            outputs = model(batch["input_ids"], batch["attention_mask"], output_hidden_states=True)
            emb = outputs.hidden_states[0].detach().cpu().numpy()
            emb = np.mean(emb, axis=1)
    return emb

embedded_sequences = []
with h5py.File(args.hdf5In, 'r') as hdf:
    sequences = hdf['sequence'][:]  # Assuming all sequences are stored in a dataset named 'sequence'
    for seq_bytes in sequences:
        seq = seq_bytes.decode('utf-8')  # Assuming sequences are stored as bytes
        emb = embed_with_genslm(seq)
        embedded_sequences.append(emb)

embedded_sequences_array = np.vstack(embedded_sequences) # Convert list of embeddings to a numpy array (n x 512)
output_hdf5_path = args.hdf5Out

with h5py.File(output_hdf5_path, 'w') as hdf: # Save the embedded sequences array to HDF5
    hdf.create_dataset('embedded_sequences', data=embedded_sequences_array)

print(f"Written to {output_hdf5_path}")

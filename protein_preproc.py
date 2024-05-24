import argparse
import h5py
import pandas as pd

#### PARSING PIPED ARGUMENTS ####
description_text = (
    "Script for loader .feather file of dataframe of gisaid sequences and then "
    "wrangles df to a list of sequences indexing the protein type by the ARRAY_JOB_ID"
)
parser = argparse.ArgumentParser(description=description_text)
parser.add_argument(
    "-in",
    "--featherIn",
    type=str,
    required=True,
    help="Path to the input feather file with original DNA sequences.",
)
parser.add_argument(
    "-out",
    "--hdf5OutputPath",
    type=str,
    required=True,
    help="The root Path to save the output sequences in HDF5 format. ie /user/file/",
)
parser.add_argument(
    "-aid",
    "--arrayId",
    type=int,
    required=True,
    help="adjusted array job id. This value indexes the dataframe column allowing different proteins to get different jobs",
)
args = parser.parse_args()
protien_df = pd.read_feather(args.featherIn)
proteins = ['nsp1', 'nsp2', 'nsp3', 'nsp4', 'nsp5', 'nsp6', 'nsp7', 'nsp8', 'nsp9', 'nsp10', 'nsp11', 'nsp12', 'nsp13', 'nsp14', 'nsp15', 'nsp16', 'E', 'M', 'S', 'N', 'Orf3a', 'Orf3b', 'Orf6', 'Orf7a', 'Orf7b', 'Orf8b', 'Orf9b', 'Orf9c', 'Orf10']

protein_df_single_p = protien_df[proteins[args.arrayId]].tolist()
DNA = protein_df_single_p

# Write the mutated sequences to an HDF5 file:
with h5py.File(args.hdf5OutputPath, "w") as hdf:
    hdf.create_dataset("sequence", data=DNA)

print(f"Written to {args.hdf5OutputPath}")

import argparse
import h5py
import pandas as pd

#### PARSING PIPED ARGUMENTS ####
description_text = (
    "Script for loader .feather file of dataframe of gisaid sequences and then "
    "wrangles df to a list of sequences indexing the variant type by the ARRAY_JOB_ID"
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
    help="adjusted array job id. This value indexes the orfConfig.yml allowing different variants to get different jobs",
)
args = parser.parse_args()
variant_df = pd.read_feather(args.featherIn)
variants = ["alpha", "beta", "gamma", "delta", "epsilon", "omicron", "mu", "lambda"]

variant_df_single_v = variant_df[variant_df["variant"] == variants[args.arrayId]]
variant_df_single_v = variant_df_single_v["sequence"]
variant_list_single_v = variant_df_single_v.tolist()
DNA = variant_list_single_v

# Write the mutated sequences to an HDF5 file:
with h5py.File(args.hdf5OutputPath, "w") as hdf:
    hdf.create_dataset("sequence", data=DNA)

print(f"Written to {args.hdf5OutputPath}")

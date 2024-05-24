#!/bin/bash
#SBATCH --account=mayocancerai
#SBATCH --job-name=dhintz_varaints_npat_400_array
#SBATCH --mail-type=ALL
#SBATCH --mail-user=dhintz1@uwyo.edu
#SBATCH --time=1-00:00:00
#SBATCH --partition=beartooth-hugemem
#SBATCH --error=slurms/%x_%A.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --array=0-7
#SBATCH --mem=60G
#SBATCH --output=/pfs/tc1/project/mayocancerai/GenSLM/job_array_out/arrays_ex01_%A_%a.out

GENSLM_PATH="/pfs/tc1/project/mayocancerai/GenSLM"
INPUT_FEATHER="${GENSLM_PATH}/variant_dfs.feather"
POST_PROC_HDF5_OUT="${GENSLM_PATH}/data_variant/var${SLURM_ARRAY_TASK_ID}_seq_400_patients.h5"
EMBEDDED_HDF5_OUT="${GENSLM_PATH}/data_variant/var${SLURM_ARRAY_TASK_ID}_emb_400_patients.h5"

module load arcc/1.0 miniconda3/23.11.0
conda activate /pfs/tc1/project/mayocancerai/mayocancerai

# Explicitly use the Python interpreter from the specific Conda environment
PYTHON_EXEC="/pfs/tc1/project/mayocancerai/mayocancerai/bin/python"

${PYTHON_EXEC} ${GENSLM_PATH}/variant_preproc.py -in "${INPUT_FEATHER}" -out ${POST_PROC_HDF5_OUT} --arrayId ${SLURM_ARRAY_TASK_ID}
if [ $? -ne 0 ]; then
  echo "Failed to execute variant_preproc.py for Variant ${SLURM_ARRAY_TASK_ID}."
  exit 1
fi

${PYTHON_EXEC} ${GENSLM_PATH}/GenSLM.py -in ${POST_PROC_HDF5_OUT} -out ${EMBEDDED_HDF5_OUT}
if [ $? -ne 0 ]; then
  echo "Failed to execute GenSLM.py for Variant ${SLURM_ARRAY_TASK_ID}."
  exit 1
fi

echo "Emebedding for Variant ${SLURM_ARRAY_TASK_ID} completed successfully!"

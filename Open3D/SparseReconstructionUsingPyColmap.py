import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import pycolmap

print("PyCOLMAP imported successfully")

import os
import open3d as o3d
#
output_path = "workspace"
image_dir = "images"
database_path = os.path.join(output_path, "database.db")
sparse_path = os.path.join(output_path, "sparse")
#
os.mkdir(output_path)
mvs_path = f'{output_path}/mvs'
database_path = f'{output_path}/database.db'
print("Starting Feature Extraction...")
pycolmap.extract_features(database_path, image_dir)
print("Feature Extraction Complete!")
print("Exhaustive Matching Starting ...")
pycolmap.match_exhaustive(database_path)
print("Mapping Starting...")
maps = pycolmap.incremental_mapping(database_path, image_dir, output_path)
print("Mapping Finished!")
# Step 4: Save results
print("Saving Results...")
# maps[0].write(output_path)
print("Results have been saved")
#
#
#
#
#
#
#
# # dense reconstruction
# # pycolmap.undistort_images(mvs_path, output_path, image_dir)
# # pycolmap.patch_match_stereo(mvs_path)  # requires compilation with CUDA
# pycolmap.stereo_fusion('mvs_path / "dense.ply"', mvs_path)
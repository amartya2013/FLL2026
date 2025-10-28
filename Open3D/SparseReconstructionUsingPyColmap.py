import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import pycolmap
#
print("PyCOLMAP imported successfully")
#
import os
import open3d as o3d
import numpy as np
# #
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
sparse_model_path = os.path.join(output_path, "0")  # change if needed
#
print("Loading sparse reconstruction...")
reconstruction = pycolmap.Reconstruction(sparse_model_path)
num_points = len(reconstruction.points3D)
print(f"Loaded reconstruction with {num_points} points.")

# --- Extract 3D points and colors (safe for all versions) ---
points = []
colors = []

for p in reconstruction.points3D.values():
    points.append(p.xyz)
    # handle both possible field names
    if hasattr(p, "rgb"):
        colors.append(np.array(p.rgb) / 255.0)
    elif hasattr(p, "color"):
        colors.append(np.array(p.color) / 255.0)
    else:
        # fallback: default white if no color stored
        colors.append(np.array([1.0, 1.0, 1.0]))

points = np.array(points)
colors = np.array(colors)

# --- Create Open3D point cloud ---
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)

# --- Visualize ---
o3d.visualization.draw_geometries([pcd], window_name="COLMAP Sparse Reconstruction")
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
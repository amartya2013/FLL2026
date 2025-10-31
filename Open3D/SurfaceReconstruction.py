import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OPENMP_NUM_THREADS"] = "1"
import open3d as o3d
import numpy as np

# -------------------------------
# Paths
# -------------------------------
workspace = "workspace"
sparse_ply_path = os.path.join(workspace, "sparse_point_cloud.ply")
dense_mesh_path = os.path.join(workspace, "dense_mesh.ply")

# -------------------------------
# Load point cloud
# -------------------------------
pcd = o3d.io.read_point_cloud(sparse_ply_path)
print(f"Loaded point cloud with {len(pcd.points)} points.")

# -------------------------------
# Preprocess
# -------------------------------
# Optional: downsample for faster processing
voxel_size = 0.01  # adjust depending on scene scale
pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)

# Estimate normals (required for Poisson reconstruction)
pcd_down.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=30)
)
pcd_down.orient_normals_consistent_tangent_plane(100)

# -------------------------------
# Poisson surface reconstruction
# -------------------------------
depth = 14  # higher -> finer mesh, slower
mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd_down, depth=depth
)
print("Poisson reconstruction complete.")

# -------------------------------
# Remove low-density vertices (optional, cleans up mesh)
# -------------------------------
vertices_to_remove = densities < np.quantile(densities, 0.01)
mesh.remove_vertices_by_mask(vertices_to_remove)
print("Removed low-density vertices.")

# -------------------------------
# Visualize mesh
# -------------------------------
o3d.visualization.draw_geometries([mesh], window_name="Dense Mesh")

# -------------------------------
# Save mesh
# -------------------------------
o3d.io.write_triangle_mesh(dense_mesh_path, mesh)
print(f"Dense mesh saved to {dense_mesh_path}")
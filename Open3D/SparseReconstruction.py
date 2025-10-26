import os
import subprocess
import sys

# ---------------------------
# Configuration
# ---------------------------
colmap_executable = "colmap"     # Full path if not in PATH
image_folder = "images"          # Folder with input images
workspace_folder = "workspace"   # Output directory

database_path = os.path.join(workspace_folder, "database.db")
sparse_folder = os.path.join(workspace_folder, "sparse")
sparse_ply_path = os.path.join(sparse_folder, "sparse.ply")

# Create necessary directories
os.makedirs(workspace_folder, exist_ok=True)
os.makedirs(sparse_folder, exist_ok=True)

# ---------------------------
# Helper Function
# ---------------------------
def run_colmap(cmd_args, step_name):
    print(f"\n▶️ Running: {step_name}...")
    try:
        subprocess.run(cmd_args, check=True)
        print(f"✅ {step_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {step_name}: {e}")
        sys.exit(1)

# ---------------------------
# Step 1: Feature Extraction
# ---------------------------
run_colmap([
    colmap_executable, "feature_extractor",
    "--database_path", database_path,
    "--image_path", image_folder
], "Feature Extraction")

# ---------------------------
# Step 2: Feature Matching
# ---------------------------
run_colmap([
    colmap_executable, "exhaustive_matcher",
    "--database_path", database_path
], "Feature Matching")

# ---------------------------
# Step 3: Sparse Reconstruction
# ---------------------------
run_colmap([
    colmap_executable, "mapper",
    "--database_path", database_path,
    "--image_path", image_folder,
    "--output_path", sparse_folder
], "Sparse Reconstruction")

# Detect sparse model folder
sparse_model_subfolder = None
if os.path.exists(os.path.join(sparse_folder, "0", "points3D.bin")):
    sparse_model_subfolder = os.path.join(sparse_folder, "0")
elif os.path.exists(os.path.join(sparse_folder, "points3D.bin")):
    sparse_model_subfolder = sparse_folder
else:
    print("❌ No valid sparse model found. Mapper may have failed.")
    sys.exit(1)

print(f"📁 Using sparse model from: {sparse_model_subfolder}")

# ---------------------------
# Step 4: Export Sparse Point Cloud
# ---------------------------
run_colmap([
    colmap_executable, "model_converter",
    "--input_path", sparse_model_subfolder,
    "--output_path", sparse_ply_path,
    "--output_type", "PLY"
], "Export Sparse Point Cloud")

# ---------------------------
# Done
# ---------------------------
print("\n🎉 Sparse reconstruction complete!")
print(f"📦 Sparse point cloud saved at: {sparse_ply_path}")
print("💡 You can now open it in MeshLab, CloudCompare, or Python (Open3D).")

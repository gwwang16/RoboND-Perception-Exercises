# Import PCL module
import pcl

# Load Point Cloud file
cloud = pcl.load_XYZRGB('tabletop.pcd')

# Voxel Grid filter
# Create a voxelgrid filter object for our input point cloud
vox = cloud.make_voxel_grid_filter()

# Choose a voxel size (leaf size)
LEAF_SIZE = 0.01

# Set the voxel size
vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)

# Call the filter function to obtain the result downsampled point cloud
cloud_filtered = vox.filter()
filename = 'voxel_downsampled.pcd'
pcl.save(cloud_filtered, filename)



# PassThrough filter
passthrough = cloud_filtered.make_passthrough_filter()
# Assign axis and range to the passthrough filter object
filter_axis = 'z'
passthrough.set_filter_field_name(filter_axis)
axis_min = 0.6
axis_max = 1.1
passthrough.set_filter_limits(axis_min, axis_max)
# Finally use the filter function to obtain the resultant point cloud.
cloud_filtered = passthrough.filter()
filename = 'pass_through_filtered.pcd'
pcl.save(cloud_filtered, filename)



# RANSAC plane segmentation
# Create the segmentation object
seg = cloud_filtered.make_segmenter()
# Set the model you wish to fit
seg.set_model_type(pcl.SACMODEL_PLANE)
seg.set_method_type(pcl.SAC_RANSAC)
# Max distance for a point to be considered fitting the model
max_distance = 0.01
seg.set_distance_threshold(max_distance)
# Call the segment function to obtain set of inlier indices and model coefficients
inliers, coefficients = seg.segment()

# Extract inliers
# Save pcd for table
# pcl.save(cloud, filename)
extracted_inliers = cloud_filtered.extract(inliers, negative=False)
filename = 'extracted_inliers.pcd'
pcl.save(extracted_inliers, filename)


# Extract outliers
# Save pcd for tabletop objects
extracted_outliers = cloud_filtered.extract(inliers, negative=True)
filename = 'extracted_outliers.pcd'
pcl.save(extracted_outliers, filename)



# # Outlier removal filter
# # Much like the previous filters, we start by creating a filter object
# outlier_filter = cloud_in.make_statistical_outlier_filter()
# # Set the number of neighboring points to analyze for any given point
# outlier_filter.set_mean_k(50)
# # Any point with a mean distance larger than global (mean distance+x*std_dev)
# # will be considered outlier
# outlier_filter.set_std_dev_mul_thresh(x)
# # Finally call the filter function for magic
# clound_filtered = outlier_filter.filter()
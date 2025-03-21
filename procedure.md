# Protocol for Generating 3D Models on Agisoft Metashape Pro (Version 2.1.1)

## 1. Import Photos
- Import all your images into Agisoft Metashape.
- One colony per chunk.

## 2. Align Photos
- Go to **"Workflow" > "Align Photos"**.
- Configure the alignment parameters (accuracy, key point limit, etc.) and start the alignment.

## 3. Add Markers
- Once the dense point cloud is generated, add markers on an object whose dimensions you know.
- Go to **"Tools" > "Markers" > "Add Marker"** and place them on the images in their respective positions, or directly position the cursor on the point where you want to place the marker, then **right-click > "Add Marker"**. Repeat this process for all the required markers.
- Adjust the positions of the markers on multiple images for greater accuracy (**right-click > "Filter by Markers"**).

## 4. Create the Scale Bar
- Once the markers are placed, go to **"Tools" > "Markers" > "Create Scale Bar"**.
- Select two markers between which you want to create a scale bar.
- Specify the actual distance between these two points (e.g., 4 meters).
- Update (click on the two arrows forming a circle).

## 5. Optimize the Model
- After adding the markers and scale bars, it is important to optimize the cameras to adjust the model's geometry based on the new constraints.
- Go to **"Tools" > "Optimize Cameras"** and check the appropriate parameters (focal length, principal point, etc.) or click directly on the star icon.

## 6. Generate the Dense Point Cloud
- Go to **"Workflow" > "Build Dense Cloud"**.
- Configure the parameters to generate the dense point cloud.

## 7. Build the Mesh
- Go to **"Workflow" > "Build Model"**.
- Configure the parameters to generate the mesh from the dense point cloud.

## 8. Apply the Texture
- Go to **"Workflow" > "Build Texture"**.
- Configure the parameters to generate the model's texture.

## 9. Fill Holes in the 3D Model
- Go to **"Tools" > "Model" > "Close Holes"**.
- In the dialog window, configure the parameters to specify the maximum size of the holes to fill.
- Click **OK** or **Apply** to fill the holes.

## 10. Adjust the Object and Region
- Use the **"Rotate Object"** tool to align the mesh with the X, Y, Z axes. You can do this manually or by entering precise values.
- Adjust the bounding box and align the object to the X-Y plane (important for DEMs).
    - Use **"Rotate Object"**.
    - Use **"Move Region" > "Rotate Region" > "Rotate Region to Local Frame"** and **"Resize Region"**.

## 11. Create the DEM and Orthomosaic
### a) Generate the DEM (Digital Elevation Model):
- Go to **"Workflow" > "Build DEM"**.
- Source Data: Dense Cloud.
- Interpolation: Enabled (to fill gaps in the data).
- DEM Projection: Choose the appropriate coordinate system for your project.

### b) Generate the Orthomosaic:
- Go to **"Workflow" > "Build Orthomosaic"**.
- Surface: DEM (select the DEM you just generated).
- Blending Mode: Mosaic (or another mode depending on your needs).
- Seamline Quality: Default (or adjust as needed).

## 12. Export the DEM in TIFF Format
- Go to **"File" > "Export" > "Export DEM"**.
- Choose the file format **"GeoTIFF (*.tif)"**.
- Specify the location and name of the file where you want to save the DEM.
- Resolution: Set the DEM resolution if necessary.

---

### Python Scripts
Some of the steps have been automated using Python scripts:
- The Python script **"début"** was used for step 2.
- For steps 6 to 9, the Python script **"suite"** was used.
- Finally, for steps 11 and 12, the Python script **"fin"** was used.

The Python scripts are available via this link: [https://github.com/chloebio/Memoire](https://github.com/chloebio/Memoire)

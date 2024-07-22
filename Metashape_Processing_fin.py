import Metashape

doc = Metashape.app.document

for chunk in Metashape.app.document.chunks:

    print("--- Modèle 3D construit. Passons à la génération du DEM ---")

    chunk.buildDem(source_data=Metashape.DataSource.PointCloudData)

    print("--- DEM généré. Passons à la génération de l'orthomosaïque ---")

    chunk.buildOrthomosaic(fill_holes=True)

# Define the output directory
output_directory = "/Users/chloedouady/Desktop/mesures_complexites/data/tif_refaire"

# Loop through all chunks in the project
for chunk in doc.chunks:
    # Export DEM as TIFF (assuming DEM has already been created)
    dem_export_path = output_directory + "/" + chunk.label + "_DEM.tif"
    chunk.exportRaster(dem_export_path, source_data=Metashape.DataSource.ElevationData, image_format=Metashape.ImageFormatTIFF)

    # Print the export path
    print("DEM exported to:", dem_export_path)

Metashape.app.messageBox("DEM export finished for all chunks.")
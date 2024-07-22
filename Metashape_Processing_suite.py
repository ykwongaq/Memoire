"""
This code is intended to be run from the Metashape GUI. As of July 2021, it works with python 3.5 - 3.8. Python 3.9 is
not supported, although this is unlikely to matter for scripts run directly from the GUI.

This script executes over all chunks of data, and expects that there are already multiple chunks in the open project,
each already populated with photographs.

There are several values within the script that are expected to be chosen by the user, which are referred to in
dialogue boxes

In the arguments box, before running the script, be sure to choose a quality threshold below which to disable photos.
The metashape manual recommends 0.5 as a value. In several instances, underwater photographs will be of a lower quality
according to this algorithm due to barrel distortion associated with underwater camera apperatus, as well as bad
visibility. Thus, we often use 0.35.
"""

import Metashape

doc = Metashape.app.document

dcquality = Metashape.app.getInt(label="Pick a dense cloud quality for your chunks.\nHigh = 2\nMedium = 4\nLow = 8", value=4)

for chunk in Metashape.app.document.chunks:

    print("--- Optimisation des caméras ---")
    chunk.optimizeCameras()

    print("--- Construction du nuage de points dense ---")

    chunk.buildDepthMaps(downscale=dcquality, filter_mode=Metashape.MildFiltering)
    chunk.buildPointCloud()

    print("--- Construction du modèle 3D ---")

    chunk.buildModel(surface_type=Metashape.SurfaceType.Arbitrary, interpolation=Metashape.Interpolation.EnabledInterpolation, face_count=Metashape.FaceCount.HighFaceCount)
    chunk.buildUV(mapping_mode=Metashape.MappingMode.GenericMapping)
    chunk.buildTexture(blending_mode=Metashape.BlendingMode.MosaicBlending, texture_size=4096)

    print("--- Remplissage des trous dans le modèle 3D ---")
    chunk.model.closeHoles()  # Remplir les trous

Metashape.app.messageBox("Le traitement est terminé. La prochaine étape consiste à couper manuellement les modèles pour isoler votre objet focal. Ensuite, vous pouvez générer le DEM et l'orthomosaïque.")

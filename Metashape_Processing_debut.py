'''
This code is intended to be run from the Metashape GUI. As of July 2021, it works with python 3.5 - 3.8. Python 3.9 is
not supported, although this is unlikely to matter for scripts run directly from the GUI.

This script executes over all chunks of data, and expects that there are already multiple chunks in the open project,
each already populated with photographs.

There are several values within the script that are expected to be chosen by the user, which are referred to in
dialogue boxes

In the arguments box, before running the script, be sure to choose a quality threshold below which to disable photos.
The metashape manual recommends 0.5 as a value. In several instances, underwater photographs will be of a lower quality
according to this algorithm due to barrel distortion associated with underwater camera apperatus, as  well as bad
visibility. Thus, we often use 0.35.
'''

import Metashape

doc = Metashape.app.document
chunk = doc.chunk

Metashape.app.messageBox("The script that is about to execute will serially process every chunk in the current project using the same settings. The next 3 dialogue boxes present you with choices based on your computing power, available time and required model quality. Ensure all chunks are populated with the correct photographs.\n\n"
                         "We recommend aligning on high quality and processing dense clouds on medium quality. The face count in final meshes is set to high. Each chunk will be processed using the same settings. Sparse cloud cleaning is automatic, removing your need to be at "
                         "the desk whilst processing is occurring. \n\nPhotographs in each chunk will be disabled automatically based on their quality value. This is set to 0.35 by default. You can change this in the arguments box when running the script if you wish."
                         "\n\n*Please note that because different users have different methods for scaling models (marker types are varied), this script does not provide for marker detection and scale bar placement. This should be done manually at the end of processing.")

qualitythresh = Metashape.app.getFloat(label="Please choose a photo quality threshold. Photographs below this threshold will be disabled. We recommend 0.35-0.5 for underwater values. We suggest starting with 0.5, and if too many are disabled, reduce by 0.05 at a time.", value=0.5)
Alignquality = Metashape.app.getInt(label="Pick an alignment quality for your chunks.\nHigh = 1\nMedium = 2\nLow = 4", value=1)
scClean = Metashape.app.getFloat(label="The sparse cloud will be cleaned using 3 iterations of point removal based on reprojection error, projection accuracy and reconstruction "
                                        "uncertainty.\n Each removal will remove the worst x percent of points. Please choose this percentage. We recommend 90-95.", value=95)

for chunk in Metashape.app.document.chunks:
    chunk.analyzeImages()

    camera = chunk.cameras

    below_threshold = 0
    above_threshold = 0

    threshold = float(qualitythresh)

    for camera in chunk.cameras:
        if float(camera.meta["Image/Quality"]) < threshold:
            below_threshold += 1
        else:
            above_threshold += 1

    for camera in chunk.cameras:
        if float(camera.meta["Image/Quality"]) < threshold:
            camera.enabled = False

    chunk.detectMarkers(target_type=Metashape.CircularTarget12bit, tolerance=30)

    chunk.matchPhotos(downscale=Alignquality, generic_preselection=True, reference_preselection=True, keypoint_limit=40000, tiepoint_limit=4000)
    chunk.alignCameras()

    print(" --- Cameras are aligned. Sparse point cloud generated ---")

    points_original = len(chunk.tie_points.points)

    pre_clean_points = len([p for p in chunk.tie_points.points if p.valid])

    TARGET_PERCENT = scClean  # percentage of left points

    points = chunk.tie_points.points
    f = Metashape.TiePoints.Filter()
    f.init(chunk, criterion=Metashape.TiePoints.Filter.ReprojectionError)  # Reprojection Error
    list_values = f.values
    list_values_valid = list()

    for i in range(len(list_values)):
        if points[i].valid:
            list_values_valid.append(list_values[i])

    list_values_valid.sort()
    target = int(len(list_values_valid) * TARGET_PERCENT / 100)
    threshold = list_values_valid[target]
    f.selectPoints(threshold)
    f.removePoints(threshold)

    points = chunk.tie_points.points

    f = Metashape.TiePoints.Filter()
    f.init(chunk, criterion=Metashape.TiePoints.Filter.ReconstructionUncertainty)
    list_values = f.values
    list_values_valid = list()

    for i in range(len(list_values)):
        if points[i].valid:
            list_values_valid.append(list_values[i])

    list_values_valid.sort()
    target = int(len(list_values_valid) * TARGET_PERCENT / 100)
    threshold = list_values_valid[target]
    f.selectPoints(threshold)
    f.removePoints(threshold)

    points = chunk.tie_points.points

    f = Metashape.TiePoints.Filter()
    f.init(chunk, criterion=Metashape.TiePoints.Filter.ProjectionAccuracy)
    list_values = f.values
    list_values_valid = list()

    for i in range(len(list_values)):
        if points[i].valid:
            list_values_valid.append(list_values[i])

    list_values_valid.sort()
    target = int(len(list_values_valid) * TARGET_PERCENT / 100)
    threshold = list_values_valid[target]
    f.selectPoints(threshold)
    f.removePoints(threshold)

print("Première partie du script terminée")

Metashape.app.messageBox("Première partie du traitement terminée. Vous pouvez maintenant ajouter des marqueurs et des échelles avant de continuer.")

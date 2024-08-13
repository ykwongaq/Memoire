# Code pour les mesures de complexités ####

library(raster)
library(parallel) # For faster processing
library(plot3D)
library(mgcv)
library(sgeostat)
library(jpeg)
library(fields)

# Function for calculating variation in windows
fd_func <- function(x, y, s) {
  bx <- extent(cbind(c(x0 + x, y0 + y), c(x0 + x + s, y0 + y + s)))
  return(diff(range(getValues(crop(data, bx)), na.rm=TRUE)))
}

rescale <- function(x, x0, xm, n) {
  (x - x0)/(xm - x0)*n
}

count_filled_cells <- function(dat, xmin, xmax, ymin, ymax, zmin, zmax, ngrid) {
  ret <- table(ceiling(rescale(dat[,1], xmin, xmax, ngrid)), ceiling(rescale(dat[,2], ymin, ymax, ngrid)), ceiling(rescale(dat[,3], zmin, zmax, ngrid)))
  sum(ret > 0)
}

R_func <- function(H0, L0) {
  sqrt((H0^2) / (2 * L0^2) + 1)
}

D_func <- function(H, R, L, L0) {
  3 - log10(H / (sqrt(2) * L0 * sqrt(R^2 - 1))) / log10(L / L0)
}

HL0_func <- function(D, R, L, L0) {
  (3 - D) * log10(L/L0) + 0.5 * log10(R^2 - 1)
}

# Main functions

height_variation <- function(write=TRUE, return=FALSE) {
  # Fractal dimension, D
  temp <- data.frame()
  for (s in scl) {
    inc <- seq(0, L-s, s)
    x <- rep(inc, L/s)
    y <- rep(inc, each=L/s)
    # If you can't get multicore (parallel) package working, change "mcmapply" to "mapply" below:
    temp <- rbind(temp, data.frame(L0=s, x=x, y=y, H0=mcmapply(fd_func, x, y, s)))
  }
  # This variation method is time-consuming, and so save the result to avoid reprocessing if recalculating RDH
  if (write) {
    dir.create(file.path(output), showWarnings = FALSE, recursive = TRUE)
    write.csv(temp, file.path(output, paste0("var_", names(data), "_", sprintf("%04d", rep), ".csv")), row.names=FALSE)
  }
  print(paste0("Complete: ", names(data), "_", sprintf("%04d", rep)))
  # You can return the data and assign to variable if wish
  if (return) {
    return(temp)
  }
}

rdh <- function(hvar) {
  # log10 transform
  hvar$H0 <- log10(hvar$H0)
  hvar$L0 <- log10(hvar$L0)
  # plot(H0 ~ L0, hvar)
  # Mean of scales to avoid biased sampling at smaller scales
  hvar_m <- aggregate(H0 ~ L0, hvar, mean)
  # points(H0 ~ L0, hvar_m, col="red")
  
  # Find the height ranges at both ends of the scale
  H <- 10^hvar_m$H0[hvar_m$L0==log10(L)]
  H0 <- 10^hvar_m$H0[hvar_m$L0==log10(L0)]
  
  # Re-centering, probably unnecessary
  hvar_m$H0 <- hvar_m$H0 - hvar_m$H0[hvar_m$L0==log10(L)]
  hvar_m$L0 <- hvar_m$L0 - log10(L)
  
  # Calculate slopes and minus from 3 (i.e., to get D from S)
  mod <- lm(H0 ~ L0, hvar_m)
  D <- 3 - coef(mod)[2]
  mod_ends <- lm(H0 ~ L0, hvar_m[c(1, nrow(hvar_m)),])
  D_ends <- 3 - coef(mod_ends)[2]
  
  # Calculate rugosity from theory
  R_theory <- R_func(H0, L0)		
  
  # Calculate rugosity from theory (integral)
  HL0 <- 10^hvar$H0[hvar$L0==min(hvar$L0)]
  R_theory2 <-  sum(R_func(HL0, L0)) / (2/L0)^2
  
  R <- NA
  # Optional test: calculating R using another method
  temp3 <- crop(data, extent(x0, x0 + L, y0, y0 + L))
  temp3 <- as(temp3, 'SpatialGridDataFrame')
  R <- surfaceArea(temp3) / L^2
  
  # Calculate D from theory
  D_theory <- D_func(H, R_theory, L, L0)
  
  return(list(D=D, D_ends=D_ends, D_theory=D_theory, R=R, R_theory=R_theory, R_theory2=R_theory2, H=H))
}

# Scope (extent), scales of variation, and resolution (grain)
L <- 4 # Scope, 4 by 4 m reef patches
scl <- L / c(1, 2, 4, 8, 16, 32, 64, 128) # Scales, aim for 2 orders of magnitude
L0 <- min(scl) # Grain, resolution of processing ~ 6 cm

# Example surface (an 8x8m section of Horseshoe from Lizard Island)
output <- "output" # For housekeeping

# Charger le fichier CSV s'il y en a un existant
global_results_moorea_final <- read.csv("/Users/chloedouady/Desktop/mesures_complexites/resultats/global_results_moorea_final.csv")

# Load example geotif
data <- raster("/Users/chloedouady/Desktop/mesures_complexites/data/tif_moorea/C10.D.PIH_DEM.tif")
plot(data)

# Get the center of the image
x_center <- (extent(data)@xmin + extent(data)@xmax) / 2
y_center <- (extent(data)@ymin + extent(data)@ymax) / 2

# Define the bottom-left corner of the patch
x0 <- x_center - L / 2  # ajouter + ou - pour ajuster le carré sur l'axe des x
y0 <- y_center - L / 2 # ajouter + ou - pour ajuster le carré sur l'axe des y

# Draw the rectangle
rect(x0, y0, x0+L, y0+L, border="white", lty=2)

rep <- 1
# Choose patch in which to calculate RDH (rugosity, fractal D and height range).
#x0 <- data@extent[1]
#y0 <- data@extent[3]
#rect(x0, y0, x0+L, y0+L, border="white", lty=2)

# Calculate height variation at different scales (scl) within patch, and save output (because a time-consuming step)
output <- height_variation(write=TRUE, return=TRUE)

# Load the file if starting here:
# output <- read.csv(file.path(output, paste0("var_", names(data), "_0001.csv")), as.is=TRUE)

# Calculate rugosity, fractal dimension and height range (rdh function)
result <- rdh(output)

# Ajoutez la variable sample_code pour le nom du fichier TIF importé
sample_code <- "C10.PIH.D" # Remplacez par le nom approprié du fichier TIF

# Initialiser le tableau global s'il n'existe pas déjà
if (!exists("global_results_moorea_final")) {
  global_results_moorea_final <- data.frame(
    sample_code = character(),
    D = numeric(),
    D_ends = numeric(),
    D_theory = numeric(),
    R = numeric(),
    R_theory = numeric(),
    R_theory2 = numeric(),
    H = numeric(),
    stringsAsFactors = FALSE
  )
}

# Ajouter les nouveaux résultats
new_result <- data.frame(
  sample_code = sample_code,
  D = result$D,
  D_ends = result$D_ends,
  D_theory = result$D_theory,
  R = result$R,
  R_theory = result$R_theory,
  R_theory2 = result$R_theory2,
  H = result$H,
  stringsAsFactors = FALSE
)

# # Pour remplacer une ligne du tableau ####
# # Vérifier si le sample_code existe déjà dans le tableau global
# existing_row_index <- which(global_results$sample_code == sample_code)
# 
# if (length(existing_row_index) > 0) {
#   # Remplacer la ligne existante
#   global_results[existing_row_index, ] <- new_result
# } else {
#   # Ajouter les nouveaux résultats au tableau global
#   global_results <- rbind(global_results, new_result)
# }

# Ajouter les nouveaux résultats au tableau global
global_results_moorea_final <- rbind(global_results_moorea_final, new_result)

resultats <- "/Users/chloedouady/Desktop/mesures_complexites/resultats"

# Enregistrez le tableau global mis à jour
write.csv(global_results_moorea_final, file.path(resultats, "global_results_moorea_final.csv"), row.names=FALSE)

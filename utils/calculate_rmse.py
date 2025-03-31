import numpy as np

def calculate_rmse(img1, img2):
    """Calcula la Raíz del Error Cuadrático Medio (RMSE) entre dos imágenes."""
    if img1 is None or img2 is None:
        return np.nan
    if img1.shape != img2.shape:
        print(f"Error RMSE: Las dimensiones no coinciden - {img1.shape} vs {img2.shape}")
        return np.nan
    return np.sqrt(np.mean((img1.astype(np.float64) - img2.astype(np.float64))**2))

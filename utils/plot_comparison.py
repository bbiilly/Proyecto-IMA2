import numpy as np
import matplotlib.pyplot as plt

def plot_comparison(img_true, img_recon_py, img_recon_matlab, title_py, title_matlab, filename=None):
    """Muestra la imagen verdadera y las reconstrucciones de Python y MATLAB."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    cmap = 'viridis' # o 'gray'

    # Encontrar límites comunes para las barras de color (basado en reconstrucciones)
    vmin = min(np.min(img_recon_py) if img_recon_py is not None else 0,
               np.min(img_recon_matlab) if img_recon_matlab is not None else 0)
    vmax = max(np.max(img_recon_py) if img_recon_py is not None else 1,
               np.max(img_recon_matlab) if img_recon_matlab is not None else 1)
    # Ajustar vmax si es muy pequeño
    if vmax < 1e-6: vmax = 1.0

    im0 = axes[0].imshow(img_true, cmap=cmap)
    axes[0].set_title('Phantom Original (x_true)')
    axes[0].axis('off')
    fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

    if img_recon_py is not None:
        im1 = axes[1].imshow(img_recon_py, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[1].set_title(f'Python: {title_py}')
        fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    else:
        axes[1].set_title(f'Python: {title_py}\n(No disponible)')
    axes[1].axis('off')


    if img_recon_matlab is not None:
        im2 = axes[2].imshow(img_recon_matlab, cmap=cmap, vmin=vmin, vmax=vmax)
        axes[2].set_title(f'MATLAB: {title_matlab}')
        fig.colorbar(im2, ax=axes[2], fraction=0.046, pad=0.04)
    else:
         axes[2].set_title(f'MATLAB: {title_matlab}\n(No disponible)')
    axes[2].axis('off')


    plt.tight_layout()
    if filename:
        plt.savefig(filename)
        print(f"Gráfica guardada en {filename}")
    # plt.show() # Mostrar interactivamente al final


import time
import scipy.io
import numpy as np

def reconstruct_em_py(A, y_noisy, x_init, iterations, nx, ny, total_initial_counts, epsilon=1e-11):
    """
    Implementación del algoritmo ML-EM en Python.
    Normaliza las cuentas en cada iteración para coincidir con Reconstruction_EM.m.

    Args:
        A (scipy.sparse matrix): Matriz de sistema (preferiblemente CSC o CSR).
        y_noisy (np.array): Sinograma ruidoso (vector 1D).
        x_init (np.array): Imagen inicial (matriz 2D o vector 1D).
        iterations (int): Número de iteraciones.
        nx (int): Dimensión x de la imagen.
        ny (int): Dimensión y de la imagen.
        total_initial_counts (float): Suma total de cuentas en la imagen inicial (para normalización).
        epsilon (float): Valor pequeño para estabilidad numérica.

    Returns:
        tuple: (list de imágenes por iteración, imagen de sensibilidad)
    """
    print(f"Ejecutando EM Python con {iterations} iteraciones...")
    # Asegurar formato sparse eficiente y que soporte operaciones
    # Creo que esto sobra porque ya se ha hecho en el main
    if not scipy.sparse.isspmatrix_csc(A) and not scipy.sparse.isspmatrix_csr(A):
         print("Convirtiendo A a formato CSC para EM...")
         try:
            A = scipy.sparse.csc_matrix(A)
         except Exception as e:
            print(f"Error al convertir A a CSC en EM: {e}")
            return [], None # Devuelve vacío si falla

    x = x_init.copy().flatten() # Trabajar con vector 1D
    y_noisy = y_noisy.flatten()

    # Imagen de sensibilidad (A^T * 1)
    print("Calculando imagen de sensibilidad...")
    sensitivity = A.T @ np.ones(A.shape[0], dtype=x.dtype)
    sensitivity[sensitivity <= epsilon] = epsilon # Evitar división por cero
    print("Imagen de sensibilidad calculada.")


    images_em = []
    # rmse_vs_true = [] # Descomentar si se calcula RMSE por iteración

    start_time = time.time()
    for i in range(iterations):
        print(f"  Iteración EM {i+1}/{iterations}")

        # Proyección (A * x)
        y_proj = A @ x
        y_proj[y_proj <= epsilon] = epsilon # Evitar división por cero o negativos

        # Ratio y Retroproyección (A^T * (y / y_proj))
        ratio = y_noisy / y_proj
        backproj = A.T @ ratio

        # Actualización
        x = (x / sensitivity) * backproj
        x[x < 0] = 0 # Asegurar no negatividad

        # Normalizar cuentas (como en Reconstruction_EM.m)
        current_sum = np.sum(x)
        if current_sum > epsilon:
             x = x * (total_initial_counts / current_sum)
        # else: # Manejo opcional si la suma es casi cero
        #     print(f"Advertencia: Suma de imagen casi cero en iteración {i+1}. Saltando normalización.")

        img_iter = x.reshape(nx, ny).T # <<<--- NUEVA LÍNEA: Reshape Y Transponer
        images_em.append(img_iter)
        # Calcular RMSE opcionalmente aquí si se pasa x_true
        # rmse_vs_true.append(calculate_rmse(img_iter, x_true))

    end_time = time.time()
    print(f"EM Python finalizado en {end_time - start_time:.2f} segundos.")

    if not images_em: # Comprobación por si hubo error antes del bucle
         print("Advertencia: No se generaron imágenes EM.")
         return [], sensitivity.reshape(nx,ny) if 'sensitivity' in locals() else None


    return images_em, sensitivity.reshape(nx, ny)


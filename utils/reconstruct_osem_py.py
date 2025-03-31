import time
import scipy.io
import numpy as np

def reconstruct_osem_py(A, y_noisy, x_init, iterations, subsets, nx, ny, total_initial_counts, epsilon=1e-11):
    """
    Implementación del algoritmo OSEM en Python.
    Normaliza las cuentas después de cada iteración completa (todos los subsets).

    Args:
        A (scipy.sparse matrix): Matriz de sistema (CSC o CSR para slicing).
        y_noisy (np.array): Sinograma ruidoso (vector 1D).
        x_init (np.array): Imagen inicial (matriz 2D o vector 1D).
        iterations (int): Número de iteraciones completas.
        subsets (int): Número de subsets.
        nx (int): Dimensión x de la imagen.
        ny (int): Dimensión y de la imagen.
        total_initial_counts (float): Suma total para normalización.
        epsilon (float): Valor pequeño para estabilidad numérica.

    Returns:
        list: Lista de imágenes por sub-iteración.
    """
    print(f"Ejecutando OSEM Python con {iterations} iteraciones y {subsets} subsets...")
    # Asegurar formato que soporte slicing (CSC o CSR)
    if not scipy.sparse.isspmatrix_csc(A) and not scipy.sparse.isspmatrix_csr(A):
        print("Convirtiendo A a formato CSC para OSEM...")
        try:
             A = scipy.sparse.csc_matrix(A)
        except Exception as e:
            print(f"Error al convertir A a CSC en OSEM: {e}")
            return [] # Devuelve vacío si falla

    x = x_init.copy().flatten()
    y_noisy = y_noisy.flatten()
    n_bins_total = A.shape[0]

    # Validar divisibilidad (ya debería estar validado en MATLAB, pero por si acaso)
    if n_bins_total % subsets != 0:
        print(f"Error: El número total de bins ({n_bins_total}) no es divisible por el número de subsets ({subsets}).")
        # raise ValueError(...) # Alternativamente, lanzar excepción
        return [] # Devolver lista vacía en caso de error

    images_osem = [] # Guarda imagen después de cada SUB-iteración
    # rmse_vs_true = [] # Descomentar si se calcula RMSE por sub-iteración

    start_time = time.time()
    total_subiterations = iterations * subsets
    current_subiteration = 0

    for i in range(iterations):
        print(f"  Iteración OSEM {i+1}/{iterations}")
        x_before_iter = x.copy() # Guardar estado al inicio de la iteración para normalización
        for sub in range(subsets):
            current_subiteration += 1
            print(f"    Sub-iteración {current_subiteration}/{total_subiterations} (Subset {sub+1}/{subsets})")

            # Seleccionar índices del subset
            subset_indices = np.arange(sub, n_bins_total, subsets, dtype=np.int64) # Usar int64 explícito por si acaso

            # Intentar slicing con manejo de errores
            try:
                 A_sub = A[subset_indices, :]
            except Exception as e:
                 print(f"Error al hacer slicing de A (formato {type(A)}) en subset {sub+1}: {e}")
                 # Podría intentar convertir a CSR si CSC falla, aunque es raro
                 # if scipy.sparse.isspmatrix_csc(A):
                 #     print("Intentando convertir A a CSR y reintentar slicing...")
                 #     A = A.tocsr()
                 #     A_sub = A[subset_indices, :] # Reintentar
                 # else:
                 #     return [] # Fallar si no se puede
                 return []


            y_sub = y_noisy[subset_indices]

            # Sensibilidad del subset (A_m^T * 1)
            sensitivity_sub = A_sub.T @ np.ones(A_sub.shape[0], dtype=x.dtype)
            sensitivity_sub[sensitivity_sub <= epsilon] = epsilon

            # Proyección (A_m * x)
            y_proj_sub = A_sub @ x
            y_proj_sub[y_proj_sub <= epsilon] = epsilon

            # Ratio y Retroproyección (A_m^T * (y_m / y_proj_m))
            ratio_sub = y_sub / y_proj_sub
            backproj_sub = A_sub.T @ ratio_sub

            # Actualización
            x = (x / sensitivity_sub) * backproj_sub
            x[x < 0] = 0 # Asegurar no negatividad

            img_subiter = x.reshape(nx, ny).T # <<<--- NUEVA LÍNEA: Reshape Y Transponer
            images_osem.append(img_subiter)
            # Calcular RMSE opcionalmente aquí
            # rmse_vs_true.append(calculate_rmse(img_subiter, x_true))

        # Normalizar cuentas al final de cada iteración completa (todos los subsets)
        # Nota: Se usa el total_initial_counts original, no el de x_before_iter, para ser consistente con EM
        current_sum = np.sum(x)
        if current_sum > epsilon:
            x = x * (total_initial_counts / current_sum)
        # else:
        #     print(f"Advertencia: Suma de imagen casi cero en iteración OSEM {i+1}. Saltando normalización.")


    end_time = time.time()
    print(f"OSEM Python finalizado en {end_time - start_time:.2f} segundos.")

    if not images_osem:
        print("Advertencia: No se generaron imágenes OSEM.")


    return images_osem

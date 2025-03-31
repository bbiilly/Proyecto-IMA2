import numpy as np
import matplotlib
matplotlib.use("Agg") # Usar backend no ineractivo para guardar las imágenes
import matplotlib.pyplot as plt
import scipy.io
from utils.plot_comparison import plot_comparison
from utils.reconstruct_em_py import reconstruct_em_py
from utils.reconstruct_osem_py import reconstruct_osem_py
from utils.calculate_rmse import calculate_rmse

# CONSTANTES
FILE_PATH = 'pet_data_for_python.mat'
EM_ITERATIONS = 30
OSEM_ITERATIONS = 3
OSEM_SUBSETS = 12

# 1. Cargar Datos desde MATLAB
print(f"Cargando datos desde {FILE_PATH}...")
try:
    data = scipy.io.loadmat(FILE_PATH)
    print("Variables cargadas:", list(data.keys()))
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {FILE_PATH}.")
    print("Asegúrate de ejecutar primero el script de MATLAB para generar los datos.")
    exit()
except Exception as e:
    print(f"Error al cargar el archivo .mat: {e}")
    exit()

# Extraer variables con comprobación de existencia
try:
    A_loaded = data['A']

    x_true = data['x_true'].astype(np.float64)
    y_noisy_sino = data['y_noisy_sino'].astype(np.float64)
    x_em_matlab = data['x_em_matlab'].astype(np.float64)
    x_osem_matlab = data['x_osem_matlab'].astype(np.float64)

    y_noisy_vec = data['y_noisy_vec'].flatten().astype(np.float64)
    nx = int(data['nx'][0, 0])
    ny = int(data['ny'][0, 0])
    nphi = int(data['nphi'][0, 0])
    ns = int(data['ns'][0, 0])
    # Si quisiéramos usar las variables procedentes de MATLAB para EM y OSEM, descomentar las siguientes tres líneas:
    # em_iterations = int(data['em_iterations'][0, 0]) # 30
    # osem_iterations = int(data['osem_iterations'][0, 0]) # 3
    # osem_subsets = int(data['osem_subsets'][0, 0]) # 12
except KeyError as e:
    print(f"Error: Falta la variable '{e}' en el archivo {FILE_PATH}.")
    print("Asegúrate de que el script MATLAB guarda todas las variables necesarias.")
    exit()
except Exception as e:
      print(f"Error inesperado al extraer variables del .mat: {e}")
      exit()

print("Datos cargados.")

# Asegurar que A está en formato CSC (Compressed Sparse Column)
print(f"Formato original de A al cargar: {type(A_loaded)}")
if scipy.sparse.isspmatrix_coo(A_loaded):
    print("Convirtiendo A de COO a formato CSC...")
    A = A_loaded.tocsc()
elif scipy.sparse.isspmatrix_csc(A_loaded) or scipy.sparse.isspmatrix_csr(A_loaded):
    print("A ya estaba en formato CSC o CSR.")
    A = A_loaded # Usar directamente
    if scipy.sparse.isspmatrix_csr(A):
          print("Convirtiendo A de CSR a CSC para consistencia...")
          A = A.tocsc() # Preferir CSC para @ (producto matricial)
elif scipy.sparse.issparse(A_loaded):
    print(f"A está en otro formato sparse ({type(A_loaded)}). Convirtiendo a CSC...")
    A = A_loaded.tocsc()
elif isinstance(A_loaded, np.ndarray):
    print("A no es sparse, sino ndarray). Intentando convertir a CSC...")
    try:
        A = scipy.sparse.csc_matrix(A_loaded)
    except Exception as e:
        print(f"No se pudo convertir A (ndarray) a CSC: {e}")
        exit()
else:
    print(f"Error: Tipo inesperado para A: {type(A_loaded)}")
    exit()
# ---------------------------------------------------

print(f"Tamaño imagen: {nx}x{ny}, Tamaño sinograma: {nphi}x{ns}")
print(f"Forma final de A: {A.shape}, Formato: {type(A)}")


# 2. Definir imagen inicial y cuentas totales
total_counts_in_noisy_sino = np.sum(y_noisy_vec)
x_init = np.ones((nx, ny), dtype=np.float64)
# Normalizar imagen inicial a suma total de cuentas (importante para comparación)
x_init_sum = np.sum(x_init)
if x_init_sum > 1e-9:
      x_init = x_init / x_init_sum * total_counts_in_noisy_sino
else:
      print("Advertencia: Suma inicial de x_init es cero. Usando imagen de unos sin normalizar.")
      x_init = np.ones((nx, ny), dtype=np.float64) # O manejar como error
print(f"Suma total de cuentas en sinograma ruidoso: {total_counts_in_noisy_sino:.2f}")
print(f"Suma total de imagen inicial: {np.sum(x_init):.2f}")


# 3. Ejecutar Reconstrucción EM en Python
images_em_py, sensitivity_em = reconstruct_em_py(A, y_noisy_vec, x_init, EM_ITERATIONS, nx, ny, total_counts_in_noisy_sino)
if not images_em_py:
    print("Fallo en la reconstrucción EM Python.")
    x_em_python = None # Marcar como no disponible
else:
    x_em_python = images_em_py[-1] # Última iteración


# 4. Ejecutar Reconstrucción OSEM en Python
images_osem_py = reconstruct_osem_py(A, y_noisy_vec, x_init, OSEM_ITERATIONS, OSEM_SUBSETS, nx, ny, total_counts_in_noisy_sino)
if not images_osem_py:
    print("Fallo en la reconstrucción OSEM Python.")
    x_osem_python = None # Marcar como no disponible
else:
    x_osem_python = images_osem_py[-1] # Última sub-iteración

# 5. Comparación y Resultados
print("\n--- Comparación de Resultados ---")

# Comparación EM
rmse_py_vs_mat_em = calculate_rmse(x_em_python, x_em_matlab)
rmse_py_vs_true_em = calculate_rmse(x_em_python, x_true)
rmse_mat_vs_true_em = calculate_rmse(x_em_matlab, x_true)
print(f"\nEM ({EM_ITERATIONS} iteraciones):")
print(f"  RMSE(Python vs MATLAB): {rmse_py_vs_mat_em:.6g}")
print(f"  RMSE(Python vs True)  : {rmse_py_vs_true_em:.6g}")
print(f"  RMSE(MATLAB vs True)  : {rmse_mat_vs_true_em:.6g}")

# Comparación OSEM
rmse_py_vs_mat_osem = calculate_rmse(x_osem_python, x_osem_matlab)
rmse_py_vs_true_osem = calculate_rmse(x_osem_python, x_true)
rmse_mat_vs_true_osem = calculate_rmse(x_osem_matlab, x_true)
print(f"\nOSEM ({OSEM_ITERATIONS}x{OSEM_SUBSETS} sub-iteraciones):")
print(f"  RMSE(Python vs MATLAB): {rmse_py_vs_mat_osem:.6g}")
print(f"  RMSE(Python vs True)  : {rmse_py_vs_true_osem:.6g}")
print(f"  RMSE(MATLAB vs True)  : {rmse_mat_vs_true_osem:.6g}")

# 6. Visualización
print("\nGenerando gráficas de comparación...")

# Gráfica: Phantom y Sinograma
try:
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(x_true, cmap='viridis')
    plt.title('Phantom Original (x_true)')
    plt.colorbar(fraction=0.046, pad=0.04)
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(y_noisy_sino, cmap='viridis')
    plt.title(f'Sinograma Ruidoso ({nphi}x{ns})')
    plt.xlabel('Bin Radial (ns)')
    plt.ylabel('Ángulo (nphi)')
    plt.colorbar(fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig('./plots/fig_input_data.png')
    print("Gráfica guardada en ./plots/fig_input_data.png")
except Exception as e:
    print(f"Error al generar gráfica de datos de entrada: {e}")


# Gráfica: Comparación EM
try:
    plot_comparison(x_true, x_em_python, x_em_matlab,
                    f'EM ({EM_ITERATIONS} iter)', f'EM ({EM_ITERATIONS} iter)',
                    filename='./plots/fig_comparison_em.png')
except Exception as e:
    print(f"Error al generar gráfica de comparación EM: {e}")


# Gráfica: Comparación OSEM
try:
    plot_comparison(x_true, x_osem_python, x_osem_matlab,
                    f'OSEM ({OSEM_ITERATIONS}x{OSEM_SUBSETS} subiter)', f'OSEM ({OSEM_ITERATIONS}x{OSEM_SUBSETS} subiter)',
                    filename='./plots/fig_comparison_osem.png')
except Exception as e:
      print(f"Error al generar gráfica de comparación OSEM: {e}")


# Opcional: Gráfica de convergencia RMSE vs Iteración/Subiteración
try:
    if images_em_py and images_osem_py: # Solo si ambas reconstrucciones funcionaron
        plt.figure(figsize=(10, 6))
        rmse_em_py_per_iter = [calculate_rmse(img, x_true) for img in images_em_py]
        rmse_osem_py_per_subiter = [calculate_rmse(img, x_true) for img in images_osem_py]
        iter_em = np.arange(1, len(rmse_em_py_per_iter) + 1)
        subiter_osem = np.arange(1, len(rmse_osem_py_per_subiter) + 1)

        plt.plot(iter_em, rmse_em_py_per_iter, 'o-', label=f'EM Python ({EM_ITERATIONS} iter)', markersize=4)
        # Graficar OSEM vs sub-iteración, tal vez con marcas cada 'subsets' sub-iteraciones
        plt.plot(subiter_osem, rmse_osem_py_per_subiter, 's-', label=f'OSEM Python ({OSEM_ITERATIONS}x{OSEM_SUBSETS} subiter)', markersize=3, alpha=0.7)

        # Marcar fin de iteraciones completas OSEM
        iter_marks = np.arange(OSEM_SUBSETS, len(rmse_osem_py_per_subiter) + 1, OSEM_SUBSETS)
        plt.plot(iter_marks, np.array(rmse_osem_py_per_subiter)[iter_marks-1], 'r*', markersize=8, label='Fin Iter OSEM')


        plt.xlabel('Iteración (EM) / Sub-iteración (OSEM)')
        plt.ylabel('RMSE vs True')
        plt.legend()
        plt.title('Convergencia RMSE')
        plt.grid(True)
        plt.ylim(bottom=0) # Asegurar que el eje Y empiece en 0
        plt.xlim(left=0)
        plt.savefig('./plots/fig_convergence.png')
        print("Gráfica guardada en ./plots/fig_convergence.png")
except Exception as e:
      print(f"Error al generar gráfica de convergencia: {e}")

# Comparación de resultados entre MATLAB y Python elemento a elemento
print("¿Son iguales las reconstrucciones EM con MATLAB que con Python?", np.allclose(x_em_matlab, x_em_python, rtol=1e-5, atol=1e-8))
print("¿Son iguales las reconstrucciones OSEM con MATLAB que con Python?", np.allclose(x_osem_matlab, x_osem_python, rtol=1e-5, atol=1e-8))

print("\nScript finalizado.")
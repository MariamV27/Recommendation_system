![enter image description here](https://assets.soyhenry.com/LOGO-REDES-01_og.jpg)


#  Sistema de recomendaciones - Primer proyecto invidivual.

Hola, mi nombre es **Mariam** y en este primer proyecto individual para la carrera de Data Science en Soy Henry, se realizó un proceso de ETL (extract, transform and load) utilizando tres datasets. Se extrajo la información de un juego para identificar otros juegos similares. El proyecto incluye funciones para los endpoints que se utilizarán en la API y cuenta con un notebook que contiene el ETL, el análisis exploratorio de datos (EDA) y la creación de dichas funciones. Además, posee un archivo main.py con la información de las APIs y una carpeta data con los archivos parquet del proyecto.

# Preprocesamiento de Datos en formato json.
Los datos utilizados provienen de la siguiente [Google Drive](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj) e incluyen tres conjuntos de datos: uno con información de reseñas, otro con detalles de los ítems y un tercero con datos de los juegos de la plataforma de juegos Steam, junto con un **diccionario** para facilitar la comprensión del contenido.

Durante la limpieza de datos, se desanidaron varias columnas que contenían diccionarios, se eliminaron columnas innecesarias, se corrigieron los formatos de fecha y se ajustaron los tipos de datos en algunas columnas. En el conjunto de datos de reseñas de usuarios (df_user_reviews), se eliminó la columna de reseñas y se creó una nueva columna con un análisis de sentimiento para determinar si las reseñas eran negativas, positivas o neutrales. Los conjuntos de datos modificados son los siguientes.
  
# Resumen del Código
Este código crea una API con FastAPI para recomendar juegos similares a un juego dado, utilizando técnicas de procesamiento de texto y cálculo de similitud.

1.  **Importaciones y Configuración Inicial**:
    
    -   Se importan librerías necesarias: `FastAPI`, `TfidfVectorizer`, `cosine_similarity`, y `pandas`.
    -   Se inicializa la aplicación FastAPI.
    -   Se carga el DataFrame `df_steam_games` desde un archivo Parquet.
2.  **Endpoint de Recomendación**:
    
    -   Se define el endpoint `/recomendacion_juego/{product_id}` que recibe un `product_id` como parámetro.
3.  **Procesamiento y Cálculo de Similitud**:
    
    -   Se busca el juego con el `product_id` en el DataFrame.
    -   Se combinan las etiquetas y géneros del juego de referencia en una cadena de texto.
    -   Se crea un vectorizador TF-IDF.
    -   Se procesan los juegos en lotes y se calcula la similitud entre el juego de referencia y cada lote utilizando la similitud del coseno.
4.  **Selección y Retorno de Juegos Similares**:
    
    -   Se obtienen los índices de los juegos más similares.
    -   Se seleccionan y devuelven los juegos más similares (nombres, etiquetas y géneros).
5.  **Manejo de Errores**:
    
    -   Se manejan excepciones y se retorna un mensaje de error en caso de fallo.

### Funcionalidad

-   **Carga de Datos**: Se carga un DataFrame con los datos de los juegos.
-   **Recomendación**: El endpoint recibe un `product_id` y recomienda juegos con etiquetas y géneros similares usando TF-IDF y similitud del coseno.
-   **Resultados**: Se retornan los nombres, etiquetas y géneros de los juegos recomendados.

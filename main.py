from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
   
#app = FastAPI()

#@app.get("/df_steam_games.parquet")
#def read_root():
#    return {"Hello": "World"}

app = FastAPI()

# Cargar el DataFrame df_steam desde tu archivo CSV
df_steam_games = pd.read_parquet('./df_steam_games.parquet')

@app.get("/recomendacion_juego/{product_id}")
async def recomendacion_juego(product_id: int):
    try:
        # Obtén el juego de referencia
        target_game = df_steam_games[df_steam_games['id'] == product_id]

        if target_game.empty:
            return {"message": "No se encontró el juego de referencia."}

        # Combina las etiquetas (tags) y géneros en una sola cadena de texto
        target_game_tags_and_genres = ' '.join(target_game['tags'].fillna('').astype(str) + ' ' + target_game['genres'].fillna('').astype(str))

        # Crea un vectorizador TF-IDF
        tfidf_vectorizer = TfidfVectorizer()

        # Configura el tamaño del lote para la lectura de juegos
        chunk_size = 100  # Tamaño del lote 
        similarity_scores = None

        # Procesa los juegos por lotes utilizando chunks
        for chunk in pd.read_parquet('./df_steam_games.parquet', chunksize=chunk_size):
            # Combina las etiquetas (tags) y géneros de los juegos en una sola cadena de texto
            chunk_tags_and_genres = ' '.join(chunk['tags'].fillna('').astype(str) + ' ' + chunk['genres'].fillna('').astype(str))

            # Aplica el vectorizador TF-IDF al lote actual de juegos y al juego de referencia
            tfidf_matrix = tfidf_vectorizer.fit_transform([target_game_tags_and_genres, chunk_tags_and_genres])

            # Calcula la similitud entre el juego de referencia y los juegos del lote actual
            if similarity_scores is None:
                similarity_scores = cosine_similarity(tfidf_matrix)
            else:
                similarity_scores = cosine_similarity(tfidf_matrix, X=similarity_scores)

        if similarity_scores is not None:
            # Obtiene los índices de los juegos más similares
            similar_games_indices = similarity_scores[0].argsort()[::-1]

            # Recomienda los juegos más similares (puedes ajustar el número de recomendaciones)
            num_recommendations = 5
            recommended_games = df_steam_games.loc[similar_games_indices[1:num_recommendations + 1]]

            # Devuelve la lista de juegos recomendados
            return recommended_games[['app_name', 'tags', 'genres']].to_dict(orient='records')

        return {"message": "No se encontraron juegos similares."}

    except Exception as e:
        return {"message": f"Error: {str(e)}"}
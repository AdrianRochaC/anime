import requests

def buscar_anime(nombre):
    url = "https://graphql.anilist.co"

    query = """
    query ($search: String) {
      Media(search: $search, type: ANIME) {
        title {
          romaji
          english
        }
        description(asHtml: false)
        episodes
        coverImage {
          large
        }
        genres
        averageScore
        siteUrl
      }
    }
    """

    variables = {
        "search": nombre
    }

    response = requests.post(url, json={"query": query, "variables": variables})
    
    if response.status_code == 200:
        data = response.json()["data"]["Media"]
        return {
            "titulo": data["title"]["romaji"],
            "titulo_en": data["title"]["english"],
            "descripcion": data["description"],
            "episodios": data["episodes"],
            "imagen": data["coverImage"]["large"],
            "generos": data["genres"],
            "score": data["averageScore"],
            "url": data["siteUrl"]
        }
    else:
        return None

import requests

def obtener_top_animes():
    url = "https://api.jikan.moe/v4/top/anime"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"][:5]  # Top 5 animes
    except Exception as e:
        print("Error al obtener top animes:", e)
    return []

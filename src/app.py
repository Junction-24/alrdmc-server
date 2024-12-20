import flask
import threading
from flask_openapi3 import OpenAPI
import logging
from config.config import PORT
from config.openapi_config import semantic_vector_tag, semantic_vector_summary, \
                            info, SemanticVectorObject
from db_logic.poller import poller as poller_euci
from db_logic.get_vectors import fetch_all_vectors, fetch_all_titles, fetch_all_urls, \
                            fetch_all_descriptions, fetch_all_original_descriptions, fetch_all_original_titles                        
from db_logic.scrapers.scraper_otakantaa import fetch_otakantaa

logger = logging.getLogger("flask.app")

poller = threading.Thread(target=poller_euci, args=(logger,))
poller.start()

app = OpenAPI(__name__, info=info)
@app.get("/semantic_vectors", summary=semantic_vector_summary, tags=[semantic_vector_tag])
def get_semantic_vectors():
    """
    A GET endpoint to fetch all semantic vectors
    from the database
    """
    logger.info(f"fetching semantic vectors from DB")

    semantic_vector_list = fetch_all_vectors()
    titles_list = fetch_all_titles()
    original_titles_list = fetch_all_original_titles()
    url_list = fetch_all_urls()
    descriptions_list = fetch_all_descriptions()
    original_descriptions_list = fetch_all_original_descriptions()


    semantic_vector_objects = [
        SemanticVectorObject(
            semantic_vector=vector,
            semantic_vector_url=url,
            description=description,
            original_description=original_description,
            title=title,
            original_title=original_title
        )
        for vector, url, description, original_description, title, original_title in zip(semantic_vector_list, url_list, descriptions_list, original_descriptions_list, titles_list, original_titles_list)
    ]
    
    logger.info(f"got {len(semantic_vector_objects)} semantic vectors from DB")

    return flask.jsonify([ semantic_vector_object.__dict__ for semantic_vector_object in semantic_vector_objects])
 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
import getpass
import os
import openai
from llama_index.vector_stores.elasticsearch import (
    ElasticsearchStore,
    AsyncDenseVectorStrategy,
)
from llama_index.core.schema import TextNode
from llama_index.legacy import VectorStoreIndex
from llama_index.core import StorageContext


def getMovies() -> list[TextNode]:
    movies = [
        TextNode(
            text="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
            metadata={"title": "Pulp Fiction"},
        ),
        TextNode(
            text="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
            metadata={"title": "The Dark Knight"},
        ),
        TextNode(
            text="An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.",
            metadata={"title": "Fight Club"},
        ),
        TextNode(
            text="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into thed of a C.E.O.",
            metadata={"title": "Inception"},
        ),
        TextNode(
            text="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
            metadata={"title": "The Matrix"},
        ),
        TextNode(
            text="Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.",
            metadata={"title": "Se7en"},
        ),
        TextNode(
            text="An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.",
            metadata={"title": "The Godfather", "theme": "Mafia"},
        ),
    ]
    return movies


def print_results(results):
    for rank, result in enumerate(results, 1):
        print(
            f"{rank}. title={result.metadata['title']} score={result.get_score()} text={result.get_text()}"
        )


def search(vector_store: ElasticsearchStore, nodes: list[TextNode], query: str):
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    print(">>> Documents:")
    retriever = index.as_retriever()
    results = retriever.retrieve(query)
    print_results(results)

    print("\n>>> Answer:")
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    print(response)


def setUpConnection(esurl: str, espass: str) -> ElasticsearchStore:
    es = ElasticsearchStore(
        index_name="my_index",
        es_url=esurl,
        es_user="elastic",
        es_password=espass,
        retrieval_strategy=AsyncDenseVectorStrategy(),
    )
    return es


if __name__ == "__main__":
    # os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
    # openai.api_key = os.environ["OPENAI_API_KEY"]

    denseVectorStore = setUpConnection("https://es01:9200", os.environ["ES_PASS"])
    # search(denseVectorStore, getMovies(), "which movie involves dreaming?")

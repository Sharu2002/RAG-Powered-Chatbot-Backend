from services.GeminiApiService import call_gemini_api
from services.RagService import retrieve_top_k_passages
from services.embeddingService import generate_embedding
from services.connectDbService import connect_db

def construct_context(passages):
    """ Construct context from retrieved passages """
    context = "\n\n".join([p["content"] for p in passages])
    return context.strip()

def process_query(query, k=5):
    """ Process query to generate response using retrieved passages and Gemini API """
    conn = connect_db()
    if not conn:
        print("Database connection failed.")
        return

    try:
        # Generate query embedding
        query_embedding = generate_embedding(query)

        # Retrieve top-k passages
        passages = retrieve_top_k_passages(conn, query_embedding, k)

        # Construct context from retrieved passages
        context = construct_context(passages)

        # Call Gemini API with query and context
        final_response = call_gemini_api(query, context)

        print(f"Final Response from Gemini:\n{final_response}")
        return final_response

    finally:
        conn.close()
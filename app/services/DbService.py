def store_embeddings_in_db(conn, documents, embeddings):
    """ Store embeddings in pgvector table """
    try:
        cursor = conn.cursor()

        for doc, embedding in zip(documents, embeddings):
            # Ensure the embedding is in a PostgreSQL-compatible format
            embedding_vector = list(map(float, embedding))

            cursor.execute(
                """
                INSERT INTO embeddings (source_url, content, embedding)
                VALUES (%s, %s, %s);
                """,
                (doc.metadata["source"], doc.page_content, embedding_vector)
            )
            print(f"Stored embedding for {doc.metadata['source']}")
        # Commit the transaction
        conn.commit()
        print("Embeddings stored successfully.")

    except Exception as e:
        print(f"Error storing embeddings: {e}")
        conn.rollback()

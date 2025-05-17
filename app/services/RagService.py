def retrieve_top_k_passages(conn, query_embedding, k=5):
    """ Retrieve top-K passages using vector similarity """
    try:
        cursor = conn.cursor()

        # Convert query embedding to VECTOR type
        query_embedding_vector = f"ARRAY[{','.join(map(str, query_embedding))}]::vector"

        query = f"""
            SELECT content, source_url, embedding <-> {query_embedding_vector} AS similarity
            FROM embeddings
            ORDER BY similarity ASC
            LIMIT %s;
        """

        cursor.execute(query, (k,))
        results = cursor.fetchall()

        passages = [{"content": row[0], "source": row[1], "similarity": row[2]} for row in results]
        # print(f"Retrieved Top-{k} Passages: {passages}")
        return passages

    except Exception as e:
        print(f"Error retrieving passages: {e}")
        return []

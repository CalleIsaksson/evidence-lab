from evidence_lab.retrieval import retrieve_most_relevant_chunks


def main() -> None:
    try:
        document = input("Document: ")
        query = input("Query: ")
        chunk_size = int(input("Chunk size: "))
        num_chunks = int(input("Number of Chunks: "))

        best_chunks = retrieve_most_relevant_chunks(
            document,
            query,
            chunk_size,
            num_chunks,
        )

        print(f"Most relevant chunks: {best_chunks}")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()

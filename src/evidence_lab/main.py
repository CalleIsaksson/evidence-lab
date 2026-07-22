from evidence_lab.retrieval import retrieve_most_relevant_chunk


def main() -> None:
    try:
        document = input("Document: ")
        query = input("Query: ")
        chunk_size = int(input("Chunk size: "))

        best_chunk = retrieve_most_relevant_chunk(
            document,
            query,
            chunk_size,
        )

        print(f"Most relevant chunk: {best_chunk}")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()

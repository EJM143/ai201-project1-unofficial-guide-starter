import os
import re
import random

"""
Milestone 3: Document Ingestion + Chunking

Loads professor review files from the documents/ folder and turns each
individual student review into one chunk.

File format (one professor per .txt file):
    Line 1     -> professor name
    Remaining  -> student reviews, separated by blank lines

No embeddings or vector database here -- just clean ingestion + chunking.
"""

import os


def load_parse_chunks(folder="documents"):
    """Load every .txt file in `folder` and return a list of chunk dicts.

    Each chunk looks like:
        {
            "professor": "Kevin Lin",
            "review": "Disaster. DO NOT TAKE IT...",
            "source": "kevin_lin.txt",
        }
    """
    chunks = []

    # Go through every file in the folder, one at a time.
    for filename in sorted(os.listdir(folder)):

        # Skip anything that isn't a text file.
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(folder, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Split the file into "blocks" wherever there are blank lines.
        # A blank line means one or more newlines surrounded by whitespace,
        # so we split on double newlines and clean up each piece.
        blocks = [block.strip() for block in re.split(r"\n\s*\n", text)]

        # Drop any empty blocks caused by extra blank lines.
        blocks = [block for block in blocks if block != ""]

        if not blocks:
            continue  # File was empty, nothing to do.

        # The first block is the professor name.
        professor = blocks[0]

        # Every block after the name is one student review = one chunk.
        for review in blocks[1:]:
            chunks.append(
                {
                    "professor": professor,
                    "review": review,
                    "source": filename,
                }
            )

    return chunks


if __name__ == "__main__":
    chunks = load_parse_chunks("documents")

    print(f"Total number of chunks: {len(chunks)}")
    print()

    print("--- 5 random chunks ---")
    sample = random.sample(chunks, 5)

    for chunk in sample:
        print(f"Professor: {chunk['professor']}")
        print(f"Source:    {chunk['source']}")
        print(f"Review:    {chunk['review']}")
        print("-" * 40)

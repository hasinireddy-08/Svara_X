"""
Speaker embedding similarity utilities.

This module compares two speaker embeddings using cosine similarity.
"""

import torch
import torch.nn.functional as F


def cosine_similarity(
    embedding_a: torch.Tensor,
    embedding_b: torch.Tensor,
) -> float:
    """
    Calculate cosine similarity between two speaker embeddings.

    Args:
        embedding_a: First speaker embedding.
        embedding_b: Second speaker embedding.

    Returns:
        Cosine similarity as a float.
    """

    # Flatten embeddings so the function works with
    # embeddings returned in slightly different shapes.
    embedding_a = embedding_a.reshape(1, -1)
    embedding_b = embedding_b.reshape(1, -1)

    similarity = F.cosine_similarity(
        embedding_a,
        embedding_b,
        dim=1,
    )

    return float(similarity.item())
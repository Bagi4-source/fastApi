import os
import re
import numpy as np
import torch
from PIL import Image
from pkg_resources import packaging
import clip
from pydantic import BaseModel
from models import ClipResult

model, preprocess = clip.load("ViT-B-32.pt")
model.cpu().eval()

stop_words = ["a", "and", "an", "at"]


def compare(labels: list, descriptions: list) -> ClipResult:
    # Prepare labels
    for word in stop_words:
        for i, label in enumerate(labels):
            label = re.sub(r'[\W]', ' ', label)
            label = re.sub(rf'\s+{word}\s+', ' ', label)
            labels[i] = label
    labels_tokens = clip.tokenize(["This is " + l for l in labels]).cpu()
    descriptions_tokens = clip.tokenize(descriptions).cpu()

    with torch.no_grad():
        descriptions_features = model.encode_text(descriptions_tokens).float()
        labels_features = model.encode_text(labels_tokens).float()

    labels_features /= labels_features.norm(dim=-1, keepdim=True)
    descriptions_features /= descriptions_features.norm(dim=-1, keepdim=True)
    similarity = descriptions_features.cpu().numpy() @ labels_features.cpu().numpy().T

    labels_results = {}
    results = {}

    result_similarity = {}

    for i, row in enumerate(similarity):
        result_similarity[descriptions[i]] = [float(x) for x in row]

        j = list(row).index(max(row))
        res = labels_results.setdefault(labels[j], 0)
        if res < similarity[i][j]:
            labels_results[labels[j]] = similarity[i][j]
            results[labels[j]] = descriptions[i]

    x = [None] * len(labels)
    for key, value in results.items():
        x[labels.index(key)] = descriptions.index(value)

    result = ClipResult(
        similarity=result_similarity,
        labels=labels,
        result=x,
        compares=results
    )

    return result

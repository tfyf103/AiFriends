#!/usr/bin/env python3
"""Run a small retrieval-only RAG evaluation set.

This script deliberately evaluates retrieval without asking the chat LLM to generate
an answer. That makes it easier to distinguish:

* retrieval failure: the correct evidence never entered top-k;
* generation failure: evidence was present but the LLM used it poorly.

Usage from repository root:

    python scripts/eval_rag.py --cases evals/rag_cases.example.json --k 3

Real embeddings/LanceDB are required, so configure API_KEY/API_BASE/EMBEDDING_MODEL
and build the knowledge base first.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / 'backend'
sys.path.insert(0, str(BACKEND))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django  # noqa: E402

django.setup()

from web.documents.retrieval import document_source, search_documents  # noqa: E402


def evaluate_case(case, k):
    documents = search_documents(case['question'], k=k)
    combined = '\n'.join(document.page_content for document in documents).lower()
    sources = [document_source(document) for document in documents]

    keywords = case.get('expected_keywords', [])
    keyword_hits = [keyword for keyword in keywords if keyword.lower() in combined]
    keyword_score = len(keyword_hits) / len(keywords) if keywords else 1.0

    expected_source = case.get('expected_source_contains')
    source_hit = True
    if expected_source:
        source_hit = any(expected_source.lower() in source.lower() for source in sources)

    passed = keyword_score == 1.0 and source_hit
    return {
        'passed': passed,
        'keyword_score': keyword_score,
        'keyword_hits': keyword_hits,
        'sources': sources,
        'documents': documents,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cases', default='evals/rag_cases.example.json')
    parser.add_argument('--k', type=int, default=3)
    parser.add_argument('--show-content', action='store_true')
    args = parser.parse_args()

    cases_path = ROOT / args.cases
    cases = json.loads(cases_path.read_text(encoding='utf8'))

    passed = 0
    for index, case in enumerate(cases, start=1):
        result = evaluate_case(case, args.k)
        passed += int(result['passed'])
        icon = '✓' if result['passed'] else '✗'
        print(f"[{icon}] {index}. {case['question']}")
        print(f"    keyword score: {result['keyword_score']:.0%}")
        print(f"    sources: {', '.join(result['sources']) or '(none)'}")

        if args.show_content:
            for rank, document in enumerate(result['documents'], start=1):
                compact = document.page_content.replace('\n', ' ')[:240]
                print(f'    top{rank}: {compact}')

    total = len(cases)
    print(f'\nRetrieval eval: {passed}/{total} passed ({passed / total:.0%})')
    return 0 if passed == total else 1


if __name__ == '__main__':
    raise SystemExit(main())

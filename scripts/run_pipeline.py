#!/usr/bin/env python3
"""Chatbot -- index documents into vector store."""
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).parent.parent))
import logging
logging.basicConfig(level=logging.INFO)
logging.info("Chatbot pipeline -- document indexing into ChromaDB")

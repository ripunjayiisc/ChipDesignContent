"""Bootstrap: put the shared toolkit on the path and point it at this topic's img/."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("CDA_IMG_DIR", os.path.join(HERE, "img"))
os.makedirs(os.environ["CDA_IMG_DIR"], exist_ok=True)
sys.path.insert(0, os.path.dirname(HERE))     # ../  -> dsl.py, deckkit.py, wbkit.py
sys.path.insert(0, HERE)

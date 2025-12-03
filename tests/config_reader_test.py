import os
import json
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ComfyUI_RN_Translator.node import RN_Translator_Node


def main():
    node = RN_Translator_Node()
    cfg = node._load_llm_config()
    print(json.dumps({
        "has_config": bool(cfg),
        "base_url": cfg.get("base_url"),
        "api_key_masked": (cfg.get("api_key")[:6] + "***") if cfg.get("api_key") else None,
        "model": cfg.get("model"),
        "temperature": cfg.get("temperature"),
        "max_tokens": cfg.get("max_tokens"),
        "top_p": cfg.get("top_p"),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

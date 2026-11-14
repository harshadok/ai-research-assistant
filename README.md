# AI Research Assistant

A bounded research agent that searches, fetches source text, synthesizes a brief, verifies exact supporting quotes, saves results, and exports Markdown.

**Implemented local portfolio application**, with source, persistent storage, runnable API, synthetic examples, automated tests, and a demo script. The interactive API at `/docs` is the included client. This repository does not claim a production deployment, a native mobile client, or previously measured customer usage.

## Features

- Live Wikipedia search integration with a declared User-Agent; no paid search API key.
- Bounded agent pipeline: search → fetch → synthesize → verify, with per-tool traces.
- Maximum one search, five source fetches, and one model call per request.
- Source URLs, retrieval timestamps, content hashes, exact quotes, and source IDs.
- Unknown citations or quotes absent from the source are rejected from findings.
- Explicit sources-only mode, insufficient-evidence results, saved failures, and Markdown export.

## Install and run

Use Python 3.9–3.12 (developed/tested here with 3.9.6; Python 3.11 is recommended for a new environment).

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

For AI operations, install [Ollama](https://ollama.com/download), start its local server, and pull a model:

```sh
ollama serve
# In a second terminal:
ollama pull qwen2.5:1.5b
export AI_MODEL=qwen2.5:1.5b
./scripts/start.sh
```

Open [interactive API docs](http://127.0.0.1:8103/docs). The default service port is 8103; override with `PORT`. Keep one API worker bound to localhost. This single-user application has no authentication and stores development data in ignored `data/`; do not expose it as a multi-user public service.

Configuration is read from environment variables. `.env.example` documents them but is not automatically executed or loaded. `OLLAMA_BASE_URL` defaults to `http://127.0.0.1:11434`; `AI_MODEL` selects the installed local model. Providers run on the backend computer; the initial model downloads need internet. No paid API credentials are required.

`requirements.txt` contains portable version ranges; `requirements-lock.txt`, when present, records the exact versions installed in this macOS development environment.

## Walkthrough

1. `POST /research` with `{"question":"Retrieval-augmented generation","max_sources":1,"synthesize":true}`.
2. Inspect `sources`, accepted `claims`, `rejected_claims`, `uncertainties`, and `traces`.
3. Each accepted claim has a known source and a quote present in its fetched text.
4. `GET /research` lists saved runs; `GET /research/{id}` reopens one.
5. `GET /research/{id}/export` returns a Markdown brief containing accepted findings, sources, and uncertainty.
6. Set `synthesize:false` to run real search/retrieval without requiring a model.

With the API running, execute the synthetic walkthrough in another terminal:

```sh
source .venv/bin/activate
python scripts/demo.py
```

Use `--url http://127.0.0.1:PORT` to target a different local port. `/docs` exposes the full request and response schemas for manual testing.

## Tests

```sh
python -m pytest -q
```

The current automated suite has **4 passing tests** covering workflow behaviour and important failures. Tests inject provider doubles to remain deterministic; `VERIFICATION.md` separately records real-provider checks. Automated CI runs the deterministic suite without model credentials. The synthetic demo is not a production accuracy benchmark.

## Agent design

`ResearchAgent` is a deliberately finite, tool-using agent rather than an unbounded recursive loop. Its tool traces show what was searched, fetched, synthesized, and verified. The local model supplies structured claims; deterministic code checks source IDs and normalized exact-quote inclusion before accepting them.

`WikipediaSearch` uses the public MediaWiki API. There is no API key or paid search dependency. Sources-only mode works independently of Ollama.

Modules: `app/main.py` contains search tools, the agent, schema and verification, persistence endpoints, and export.

## Operational boundaries

- Wikipedia is the search corpus; this is not an unrestricted web search crawler. Fetched URLs are constructed by the server from Wikipedia page IDs, preventing arbitrary internal URL fetches.
- A source's accessibility and a quote's presence are checked. This does not establish factual truth, independent corroboration, or logical entailment. The API and exports label that scope explicitly.
- Source extracts are capped at 12,000 characters. Fetching has a 75-second budget plus bounded HTTP request timeouts; one synthesis call has its own 180-second timeout.
- Source instructions are treated as untrusted text. Prompt injection and model synthesis errors remain possible; review important findings against the sources.
- A failed provider run is saved as failed and cannot be exported as a completed brief.

## Technical references

- [FastAPI](https://fastapi.tiangolo.com/)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)

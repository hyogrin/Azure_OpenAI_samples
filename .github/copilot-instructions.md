# Copilot instructions for Azure_OpenAI_samples

Always response in 한국어

all source code and comment in English


## Repo layout you should know
- `GPT-5/` – Azure OpenAI GPT‑5 basic tests (Chat Completions + Responses API). Uses `openai` Python SDK v1.x with `AzureOpenAI` client.
- `O1 MultiModal/` – o1 GA multimodal tests (vision, structured output, gradio). Requires preview API versions.
- `AI Search with AOAI/` – Azure AI Search + AOAI query patterns, hybrid/vector/reranking. Uses `azure-search-documents` (11.6.0b4).
- `Azure AI Evaluation SDK/` – Evaluators/simulators, batch evaluation, scheduling with tracing. Uses `azure.ai.projects`, `azure.ai.evaluation`, `azure.ai.ml`.
- `Azure AI Foundry Trace/` – How to instrument and view traces for AOAI/Inference SDK.
- `Azure Custom Speech/` – End‑to‑end STT custom model data gen, training, eval, deploy. Uses `azure.cognitiveservices.speech` and Storage SDK.

## Environment and secrets conventions
- Each scenario dir usually ships a `.env.sample` or `sample.env`; copy to `.env` in the same folder and fill values. Notebooks load with `load_dotenv(override=True)`.
- Common Azure OpenAI vars (seen across notebooks):
  - `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_API_VERSION` (often `2025-03-01-preview`)
  - `AZURE_OPENAI_DEPLOYMENT_NAME` (used as `model` for AzureOpenAI calls)
  - Some older notebooks also use `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
- Other scenarios add:
  - AI Projects/Eval: `AZURE_AI_PROJECT_CONN_STR` in the form `<region>.api.azureml.ms;<subscription>;<resourceGroup>;<projectName>`
  - AI Search: endpoint/key in that folder’s README/.env; uses `AzureKeyCredential`
  - Speech: `AZURE_AI_SPEECH_API_KEY`, `AZURE_AI_SPEECH_REGION`, and language/locale settings
  - Optional: `TEST_IMAGE_URL` for vision tests
- Never print keys; show only boolean “set” flags when troubleshooting.

## Azure OpenAI usage patterns in this repo
- Client: `from openai import AzureOpenAI` then `client = AzureOpenAI(azure_endpoint=..., api_key=..., api_version=...)`
- Chat Completions: `client.chat.completions.create(model=<deployment>, messages=[...], temperature=..., stream=True|False)`
  - Function Calling via `tools=[{type:"function", function:{name, parameters}}]`, `tool_choice="auto"`
  - Streaming: iterate chunks; print `chunk.choices[0].delta.content`
- Responses API: `client.responses.create(model=<deployment>, input=...)`
  - Structured output: `response_format={"type":"json_schema", "json_schema": {...}}`
  - Multimodal input: `input=[{"role":"user","content":[{"type":"text","text":"..."},{"type":"input_image","image_url":URL}]}]`
- API versions vary by model (e.g., o1 notebooks cite preview versions). Pick from the folder’s README or `.env.sample`—don’t hardcode globally.

## Developer workflows (per scenario)
- Python: use 3.10+ and install per-folder dependencies, e.g. `pip install -r <folder>/requirements.txt`.
- Run notebooks in VS Code; select the correct interpreter; `.env` lives in the same folder as the notebook.
- Tracing/Evaluation flows often require Azure login (`DefaultAzureCredential`) and a valid `AZURE_AI_PROJECT_CONN_STR`.

## Project-specific conventions
- Azure OpenAI “model” parameter is the deployment name (not the base model string). Many folders print the endpoint/version/deployment for sanity checks.
- Notebooks may mix English/Korean prompts; keep outputs concise unless a tutorial step asks for detail.
- Some folders keep multiple environment variable spellings (e.g., `AZURE_OPENAI_DEPLOYMENT_NAME` vs `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`). When editing, support both if already present.

## Integration highlights and examples
- AI Search examples (in `AI Search with AOAI/`) use `VectorizedQuery`, hybrid search, filters, cross-field; ensure `azure-search-documents==11.6.0b4` as in the folder’s requirements.
- Evaluation SDK notebooks configure `AIProjectClient.from_connection_string(...)` and `MLClient` to run cloud evals and schedules, and often call AOAI via the same env vars.
- Custom Speech flows upload data to Storage, call REST for endpoints; long‑running operations are polled with progress bars.

## Guidance for AI agents making edits
- For notebooks: preserve existing cells’ `metadata.id`; add `metadata.language`. Keep edits self‑contained by scenario folder.
- Add/update `.env.sample` when introducing new required variables; mirror naming used in that folder.
- Prefer updating per‑folder `requirements.txt` over repo‑wide changes. Do not leak secrets in output or logs.

If any scenario’s env vars or API versions are unclear, open an issue or ask the repo owner which deployment/model versions are currently active.

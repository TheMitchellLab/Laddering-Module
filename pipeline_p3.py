"""
LadderChat Interview Pipeline Human-in-the-Loop
"""

import asyncio
import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
import openai
import time as _time
from ladderchat_interview_p3 import _AnthropicClientShim
from dataclasses import asdict
import time as _time_pr
import re as _re_fn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ladderchat_interview_p3 import (
    run_interview, InterviewSession,
    InterviewType, LadderingMethod, encode_image,
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("ladderchat_interview_p3").setLevel(logging.WARNING)
logger = logging.getLogger("pipeline")

_SCRIPT_DIR = Path(__file__).parent
AVAILABLE_WIREFRAME_IMAGES: list[str] = [
    str(_SCRIPT_DIR / "u1.png"),
    str(_SCRIPT_DIR / "u2.png"),
    str(_SCRIPT_DIR / "u3.png"),
    str(_SCRIPT_DIR / "u4.png"),
    str(_SCRIPT_DIR / "u5.png"),
]
_PROVIDER_CONFIG = {
    "openai":      {"base_url": "https://api.openai.com/v1",
                    "api_key_env": "OPENAI_API_KEY",
                    "model": "gpt-5.5",
                    "client_type": "openai"},
    "gemini":      {"base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
                    "api_key_env": "GEMINI_API_KEY",
                    "model": "gemini-2.5-pro",
                    "client_type": "openai"},
    "anthropic":   {"base_url": None,
                    "api_key_env": "ANTHROPIC_API_KEY",
                    "model": "claude-sonnet-4-6",
                    "client_type": "anthropic"},
    "together":    {"base_url": "https://api.together.xyz/v1",
                    "api_key_env": "TOGETHER_API_KEY",
                    "model": "Qwen/Qwen2.5-72B-Instruct",
                    "client_type": "openai"},
    "openrouter":  {"base_url": "https://openrouter.ai/api/v1",
                    "api_key_env": "OPENROUTER_API_KEY",
                    "model": "qwen/qwen2.5-vl-72b-instruct",
                    "client_type": "openai"},
    "dashscope":   {"base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                    "api_key_env": "DASHSCOPE_API_KEY",
                    "model": "qwen-max",
                    "client_type": "openai"},
    "ollama":      {"base_url": os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                    "api_key_env": None,
                    "model": "gemma4:12b",
                    "client_type": "openai"},
}

_LOCAL_INTERVIEWER_DEFAULT = "gemma4:12b"
_LOCAL_FAST_INTERVIEWER_DEFAULT = "qwen2.5:7b"
DEBUG_LOCAL = False
_CLOUD_PROVIDER_DEFAULT    = "openai"
_CLOUD_INTERVIEWER_DEFAULT = "gpt-5.5"
_CLOUD_JUDGE_PROVIDER_DEFAULT = "anthropic"
_CLOUD_JUDGE_DEFAULT          = "claude-sonnet-4-6"
_LOCAL_JUDGE_DEFAULT          = "qwen3.6:27b"
_PROVIDER = os.environ.get("LADDERCHAT_PROVIDER", _CLOUD_PROVIDER_DEFAULT).lower()
if _PROVIDER not in _PROVIDER_CONFIG:
    _PROVIDER = _CLOUD_PROVIDER_DEFAULT
_CFG = _PROVIDER_CONFIG[_PROVIDER]
MODEL             = os.environ.get("LADDERCHAT_MODEL", _CFG["model"])
INTERVIEWER_MODEL = os.environ.get("INTERVIEWER_MODEL", MODEL)
_INTERVIEWER_PROVIDER = os.environ.get("INTERVIEWER_PROVIDER", _PROVIDER).lower()
if _INTERVIEWER_PROVIDER not in _PROVIDER_CONFIG:
    _INTERVIEWER_PROVIDER = _PROVIDER
_INTERVIEWER_CFG = _PROVIDER_CONFIG[_INTERVIEWER_PROVIDER]
if os.environ.get("INTERVIEWER_MODEL"):
    INTERVIEWER_MODEL = os.environ["INTERVIEWER_MODEL"]
INTERVIEW_TEMP_I = 0.3
INTERVIEW_TEMP_P = 0.4

class PipelineReport:
    def __init__(self, output_dir: str = "results", output_filename: str = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_filename = output_filename
        self.records = []
    def add_run(self, record: dict):
        self.records.append(record)
    def save(self):
        fname = self.output_filename if self.output_filename else f"run_{self.timestamp}.json"
        path = self.output_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2, default=str, ensure_ascii=False)
        logger.info(f"Results saved → {path}")
        self._print_summary()
        return path
    def _print_summary(self):
        print("\n" + "="*65)
        print("PIPELINE SUMMARY")
        print("="*65)
        for r in self.records:
            depth    = r.get("interview_depth", "N/A")
            drifts   = r.get("drift_events_count", 0)
            print(f"\n  Product:     {r.get('product_description', '(not recorded)')[:70]}")
            print(f"  Interview depth:   {depth}  |  Drift events: {drifts}")
            summary = r.get("interview_summary", {})
            if summary:
                print(f"\n  Interview summary:")
                orig = summary.get('original_response', summary.get('trigger', ''))
                print(f"    Original response: {orig[:80]}{'…' if len(orig) > 80 else ''}")
                print(f"    Vague seed:        {summary.get('vague_seed', '')}")
                print(f"    Confirmed attr:    {summary.get('confirmed_attribute', summary.get('specific_concern', ''))}")
                print(f"    Total chains:      {summary.get('total_chains', '')}")
                print(f"    Total steps:       {summary.get('total_steps', '')}")
                print(f"    Stopping reason:   {summary.get('stopping_reason', '')}")
                for i, chain in enumerate(summary.get("chains", []), 1):
                    steps = " → ".join(
                        f'[L{s["ladder"]}][{s["type"]}] {s["text"]}'
                        for s in chain["steps"]
                    )
                    print(f"    Chain {i}: {steps}")
                    print(f"             Endpoint: {chain.get('endpoint_type', '')}")
        print("="*65 + "\n")

async def run_single(
    interviewer_client: openai.AsyncOpenAI,
    interview_type: InterviewType,
    product_label: str,
    prior_response: str,
    vague_seed: str,
    report: PipelineReport,
    image_b64: str = "",
    image_media_type: str = "image/png",
    image_path: str = "",
    product_description: str = "",
    wireframe_images: list = None,  #list of (b64, media_type) tuples, flow order
    run_interview_flag: bool = True,
    is_ollama: bool = False,
    skip_judge: bool = False,
    shadow_mode: bool = True,
    judge_model: str = "",
    judge_client=None,
    laddering_method: LadderingMethod = LadderingMethod.ACV,
):
    record = {
        "persona": "Human",
        "interview_type": interview_type.value,
        "product_label": product_label,
        "image_path": image_path,
        "product_description": product_description,
        "prior_response": prior_response,
        "vague_seed": vague_seed,
        "model": MODEL,
    }
    session = None
    if run_interview_flag:
        logger.info(f"\n{'─'*50}")
        logger.info(f"[Interview] {interview_type.value.title()} | {laddering_method.value.upper()}")
        logger.info(f"  Product:    {product_label}")
        logger.info(f"  Prior resp: {prior_response[:70]}{'…' if len(prior_response)>70 else ''}")
        logger.info(f"  Seed:       {vague_seed}")
        logger.info(f"{'─'*50}")
        session = await run_interview(
            interviewer_client, INTERVIEWER_MODEL,
            interview_type=interview_type,
            product_label=product_label,
            prior_response=prior_response,
            vague_seed=vague_seed,
            image_b64=image_b64,
            image_media_type=image_media_type,
            wireframe_images=wireframe_images or [],
            product_description=product_description,
            image_path=image_path,
            is_ollama=is_ollama,
            min_depth=3,
            temperature_interviewer=INTERVIEW_TEMP_I,
            skip_judge=skip_judge,
            shadow_mode=shadow_mode,
            judge_model=judge_model,
            judge_client=judge_client,
            laddering_method=laddering_method,
        )
        record["interview_depth"] = session.final_depth
        record["terminated_naturally"] = session.terminated_naturally
        record["drift_events_count"] = len(session.drift_events)
        record["drift_events"] = session.drift_events
        record["interview_summary"] = session.interview_summary
        record["turns"] = [
            {"turn": t["turn"], "q": t["question"], "a": t["answer"]}
            for t in session.turns
        ]
        if session.judge_log and session.judge_log.scores:
            record["judge_log"] = asdict(session.judge_log)
        if session.judge_report:
            record["judge_report"] = session.judge_report
        _judge_by_turn = {}
        if session.judge_log and session.judge_log.scores:
            for fb in session.judge_log.scores:
                _judge_by_turn[fb.turn] = fb
        print(f"\n  --- Ladder Chain ---")
        for t in session.turns:
            print(f"  Q{t['turn']}: {t['question']}")
            print(f"  A{t['turn']}: {t['answer']}")
            fb = _judge_by_turn.get(t["turn"])
            if fb:
                prox_icon = {"far": "○", "approaching": "◑", "near": "●"}.get(fb.unlock_proximity, "?")
                print(
                    f"       [JUDGE t{fb.turn}] "
                    f"ladder={fb.ladder_score}/3  defl={fb.deflection_score}/3  "
                    f"composite={fb.composite_score}  "
                    f"unlock={prox_icon}{fb.unlock_proximity}  "
                    f"signal={'✓' if fb.extracted_signal else '✗'}  "
                    f"rep={'⚑' if fb.repetition_flag else '—'}"
                )
                print(f"       [JUDGE tactic] {fb.suggested_tactic}")
        if session.judge_report:
            jr = session.judge_report
            print(f"\n  --- Judge Report ---")
            print(f"  Efficiency      : {jr.get('laddering_efficiency', 'N/A')}")
            print(f"  Assessment      : {jr.get('overall_assessment', 'N/A')}")
            missed = jr.get('missed_unlock_opportunities', [])
            if missed:
                for m in missed:
                    print(f"  Missed unlock   : {m}")
            uncountered = jr.get('deflection_patterns_uncountered', [])
            if uncountered:
                for d in uncountered:
                    print(f"  Uncountered def : {d}")
        print()
    report.add_run(record)
    return record

def parse_args():
    parser = argparse.ArgumentParser(
        description="LadderChat human-in-the-loop interview pipeline")
    parser.add_argument("--interview-type", default="wireframe",
                        choices=["wireframe"],
                        help="Interview input type (wireframe only)")
    parser.add_argument("--laddering-method", default="acv",
                        choices=["acv", "5whys", "jtbd"],
                        help=(
                            "Probing methodology: acv (Attribute→Consequence→Value, default) | "
                            "5whys (5-Whys sequential causal chain) | "
                            "jtbd (Job Story Ladder: Situation→Job→Outcome→Barrier). "
                            "acv: surfaces actionable UX requirements from user reactions. "
                            "5whys: traces root cause behind a confirmed friction point. "
                            "jtbd: surfaces complete job stories with desired outcomes and barriers."))
    parser.add_argument("--wireframe-images", nargs="+", default=None,
                        help="Paths to wireframe screen(s) to use for this run (e.g. alpine/u1.png). "
                             "Available: u1.png u2.png u3.png u4.png u5.png. "
                             "Pass one screen per run for isolated testing, or multiple in flow order. "
                             "Required on Alpine — no auto-defaults.")
    parser.add_argument("--product", default=None,
                        help="Product description text. Used for fidelity/launch types.")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--local", action="store_true",
                        help=(
                            "Run fully locally via Ollama. "
                            "Default: gemma4:31b for both roles. Requires ~20GB RAM."))
    mode_group.add_argument("--cloud", action="store_true",
                        help=(
                            "Run via cloud APIs (default). "
                            "Interviewer+Persona: OpenAI gpt-4o. Judge: Claude claude-sonnet-4-5. "
                            "Requires OPENAI_API_KEY and ANTHROPIC_API_KEY env vars."))
    parser.add_argument("--provider", default=None,
                        choices=list(_PROVIDER_CONFIG.keys()),
                        help=(
                            "API provider for interviewer + persona. "
                            "Default cloud: openai. Default local: ollama. "
                            "Options: openai | anthropic | gemini | ollama | openrouter | together | dashscope"))
    parser.add_argument("--judge-provider", default=None,
                        choices=list(_PROVIDER_CONFIG.keys()),
                        help=(
                            "API provider for the judge. "
                            "Default cloud: anthropic (Claude). Default local: ollama. "
                            "Options: anthropic | openai | gemini | ollama | openrouter"))
    parser.add_argument("--model", default=None,
                        help=(
                            "Model ID for BOTH interviewer and persona (always the same). "
                            "Defaults to the selected provider's default model. "
                            "Must support vision for wireframe interviews. "
                            "Cloud examples: gpt-5.5, gemini-2.5-pro, claude-sonnet-4-6"))
    parser.add_argument("--fast", action="store_true",
                        help=("Debug/fast-local mode (only applies with --local). "
                            "Swaps both roles to qwen2.5:7b for parsing verification. "
                            "Pull once with: ollama pull qwen2.5:7b"))
    parser.add_argument("--skip-judge", action="store_true",
                        help="Disable judge entirely.")
    parser.add_argument("--judge-shadow", action="store_true",
                        help="Judge scores silently, no injection (DEFAULT).")
    parser.add_argument("--judge-active", action="store_true",
                        help="Judge injects feedback into generate_question().")
    parser.add_argument("--judge-model", default=None,
                        help=("Override judge model ID. "
                            "Cloud default: claude-sonnet-4-5 (Anthropic). "
                            "Local default: qwen2.5:7b. "
                            "Gemini example: gemini-2.0-flash"))
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--output-filename", default=None,
                        help="Override the output JSON filename (e.g. 06_10_26_u1.json). "
                             "If omitted, defaults to run_{timestamp}.json.")
    parser.add_argument("--iterations", type=int, default=1,
                        help="Number of complete interview runs to execute. Each iteration is "
                             "saved as a separate JSON file. Prior response and vague seed are "
                             "collected once and reused across all iterations.")
    parser.add_argument("--vague-seed", default=None,
                        help="Pre-collected vague seed phrase. Skips interactive prompt.")
    parser.add_argument("--prior-response", default=None,
                        help="Pre-collected prior response text. Skips generate_prior_response().")
    parser.add_argument("--prior-response-file", default=None,
                        help="Path to file containing prior response text (one per line or multi-line). "
                             "Safer than --prior-response for long text with special characters.")
    parser.add_argument("--seed-only", action="store_true",
                        help="Seed collection mode: generate prior_response, prompt for vague seed, "
                             "print JSON to stdout, then exit. No interview runs.")
    return parser.parse_args()

async def main():
    args = parse_args()
    global MODEL, INTERVIEWER_MODEL, _PROVIDER, _CFG, _INTERVIEWER_CFG
    interviewer_client = None
    image_b64 = ""
    image_media_type = "image/png"
    image_path = ""
    product_description = ""
    product_label = ""
    interview_type = InterviewType(args.interview_type)
    laddering_method = LadderingMethod(args.laddering_method)
    use_local = args.local or (not args.cloud and _PROVIDER == "ollama")
    if use_local:
        _PROVIDER        = "ollama"
        _CFG             = _PROVIDER_CONFIG["ollama"]
        _INTERVIEWER_CFG = _PROVIDER_CONFIG["ollama"]
        _use_fast = DEBUG_LOCAL or args.fast
        _shared_model = (
            args.model
            or (_LOCAL_FAST_INTERVIEWER_DEFAULT if _use_fast else _LOCAL_INTERVIEWER_DEFAULT)
        )
    else:
        _use_fast = False
        if args.provider:
            _PROVIDER        = args.provider
            _CFG             = _PROVIDER_CONFIG[_PROVIDER]
            _INTERVIEWER_CFG = _CFG
        else:
            _PROVIDER        = _CLOUD_PROVIDER_DEFAULT
            _CFG             = _PROVIDER_CONFIG[_PROVIDER]
            _INTERVIEWER_CFG = _CFG
        _shared_model = args.model or _CFG.get("model", _CLOUD_INTERVIEWER_DEFAULT)

    INTERVIEWER_MODEL = _shared_model
    MODEL             = _shared_model
    if use_local:
        _judge_provider = "ollama"
    else:
        _judge_provider = args.judge_provider or _CLOUD_JUDGE_PROVIDER_DEFAULT
    _judge_cfg   = _PROVIDER_CONFIG.get(_judge_provider, _PROVIDER_CONFIG["anthropic"])
    _skip_judge  = args.skip_judge
    _shadow_mode = not args.judge_active
    if use_local:
        _judge_model = args.judge_model or _LOCAL_JUDGE_DEFAULT
    else:
        _judge_model = args.judge_model or _judge_cfg.get("model", _CLOUD_JUDGE_DEFAULT)
    if not _skip_judge:
        _same_model    = (_judge_model.strip().lower() == INTERVIEWER_MODEL.strip().lower())
        _same_provider = (_judge_provider == _PROVIDER)
        if _same_model and _same_provider:
            print("\nERROR: Judge model must differ from the interviewer model.")
            print(f"  Interviewer : {INTERVIEWER_MODEL} [{_PROVIDER}]")
            print(f"  Judge       : {_judge_model} [{_judge_provider}]")
            print("\nFix options:")
            print("  --judge-provider anthropic --judge-model claude-sonnet-4-6  (default)")
            print("  --judge-provider gemini    --judge-model gemini-2.5-pro")
            print("  --judge-model <any-different-model-id>")
            print("  --skip-judge  (disable judge entirely)")
            sys.exit(1)
    def _make_client(cfg: dict):
        client_type = cfg.get("client_type", "openai")
        if client_type == "anthropic":
            key_env = cfg.get("api_key_env", "ANTHROPIC_API_KEY")
            key = os.environ.get(key_env, "")
            if not key:
                print(f"ERROR: {key_env} not set.")
                print(f"  export {key_env}=<your-anthropic-key>")
                sys.exit(1)
            return _AnthropicClientShim(api_key=key)
        if cfg.get("api_key_env") is None:
            return openai.AsyncOpenAI(api_key="ollama", base_url=cfg["base_url"])
        key = os.environ.get(cfg["api_key_env"], "")
        if not key:
            env_name = cfg["api_key_env"]
            print(f"ERROR: {env_name} not set.")
            print(f"  export {env_name}=<your-key>")
            sys.exit(1)
        return openai.AsyncOpenAI(api_key=key, base_url=cfg["base_url"])
    interviewer_client = _make_client(_INTERVIEWER_CFG)
    _judge_client = None
    if not _skip_judge:
        _judge_client = _make_client(_judge_cfg)
    sep = "=" * 60
    mode_label = "LOCAL (Ollama)" if use_local else f"CLOUD ({_PROVIDER})"
    if use_local and (DEBUG_LOCAL or args.fast):
        mode_label += " [DEBUG]"
    print(f"\n{sep}")
    print(f"  LadderChat  |  {mode_label}")
    print(f"  Interviewer : {INTERVIEWER_MODEL} [{_PROVIDER}]")
    print(f"  Interviewee : real human (terminal input)")
    if args.iterations > 1:
        print(f"  Iterations  : {args.iterations}")
    if not _skip_judge:
        print(f"  Judge       : {_judge_model} [{_judge_provider}]")
    print(f"  Local mode  : {'yes (Ollama)' if use_local else 'no'}")
    print(f"{sep}\n")
    wireframe_images = []
    if interview_type == InterviewType.WIREFRAME:
        image_paths_raw = args.wireframe_images or []
        if not image_paths_raw:
            avail = [os.path.basename(p) for p in AVAILABLE_WIREFRAME_IMAGES if os.path.isfile(p)]
            print("ERROR: --wireframe-images is required on Alpine.")
            print(f"  Available screens: {', '.join(avail) if avail else '(none found)'}")
            print("  Example: --wireframe-images alpine/u1.png")
            print("  Multiple: --wireframe-images alpine/u1.png alpine/u2.png")
            sys.exit(1)
        if not image_paths_raw:
            print("ERROR: No wireframe images provided.")
            sys.exit(1)
        for p in image_paths_raw:
            if not os.path.isfile(p):
                print(f"ERROR: Image not found: {p}")
                sys.exit(1)
        wireframe_images = [encode_image(p) for p in image_paths_raw]
        image_b64, image_media_type = wireframe_images[0]
        image_path = image_paths_raw[0]
        product_label = f"Wireframe UI ({len(wireframe_images)} screens)"
        logger.info(f"[Wireframe] Loaded {len(wireframe_images)} screen(s): {[os.path.basename(p) for p in image_paths_raw]}")
    _wf_stem = os.path.splitext(os.path.basename(image_path))[0] if image_path else "run"
    report = PipelineReport(output_dir=args.output_dir, output_filename=args.output_filename)
    print(f"\n{'─'*55}")
    print(f"  Prior response + vague seed")
    print(f"{'─'*55}")
    _provided_prior = args.prior_response
    if not _provided_prior and args.prior_response_file:
        with open(args.prior_response_file, "r", encoding="utf-8") as _f:
            _provided_prior = _f.read().strip()
    if _provided_prior:
        prior_response = _provided_prior
        print(f"\n  [Using provided prior response]")
        print(f"  {prior_response[:120]}{'…' if len(prior_response)>120 else ''}\n")
    else:
        _time_pr.sleep(1)
        sys.stdout.flush()
        sys.stderr.flush()
        print("\n" + "-" * 60)
        print("  WIREFRAMES FOR INTERVIEWEE TO REVIEW")
        print("-" + "─" * 59)
        for _wp in (args.wireframe_images or []):
            print(f"  Screen: {_wp}")
        print("-")
        print("  Please review the wireframe screens listed above,")
        print("  then type your initial reaction (3–5 sentences,")
        print("  vague / surface-level impression).")
        print("-" * 60)
        sys.stdout.flush()
        try:
            prior_response = input("\n  ▶ Initial reaction > ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        if not prior_response:
            prior_response = "(no initial reaction provided)"
        _preview = prior_response[:80]
        _ellipsis = "…" if len(prior_response) > 80 else ""
        print(f"\n  Recorded: \"{_preview}{_ellipsis}\"\n")
    if args.vague_seed:
        vague_seed = args.vague_seed
        print(f"  Using provided seed: \"{vague_seed}\"")
    else:
        _time.sleep(2)
        sys.stdout.flush()
        sys.stderr.flush()
        print("\n" + "-" * 60)
        print("  VAGUE SEED INPUT REQUIRED")
        print("-" + "─" * 59)
        print(f"  Response: {prior_response[:80]}…")
        print("-")
        print("  Identify the vague phrase to probe (3–12 words")
        print("  from the response above). Press Enter for auto-extract.")
        print("-" * 60)
        try:
            raw_seed = input("\n  >> Vague seed > ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        if not raw_seed:
            raw_seed = prior_response[:120]
            print(f"  (auto-extracted from prior response)")
        vague_seed = raw_seed
        print(f"\n  !! Seed: \"{vague_seed}\"")
    if args.seed_only:
        seeds_out = {
            "prior_response": prior_response,
            "vague_seed": vague_seed,
        }
        print("\n__SEEDS_JSON_START__")
        print(json.dumps(seeds_out, indent=2, ensure_ascii=False))
        print("__SEEDS_JSON_END__")
        logger.info("Seed collection complete. Exiting.")
        return
    n_iter = max(1, args.iterations)
    for _iter in range(n_iter):
        if n_iter > 1:
            print(f"\n{'═'*60}")
            print(f"  ITERATION {_iter + 1} / {n_iter}")
            print(f"{'═'*60}")
        if args.output_filename:
            _base, _ext = os.path.splitext(args.output_filename)
            _iter_filename = f"{_base}_iter{_iter + 1}{_ext}"
        else:
            _model_slug = (_re_fn.match(r'^([a-zA-Z]+)', INTERVIEWER_MODEL) or _re_fn.match(r'.', 'x')).group(1).lower()
            _iter_filename = f"results_{_wf_stem}_{args.laddering_method}_{_model_slug}_iter{_iter + 1}.json"

        _iter_report = PipelineReport(
            output_dir=args.output_dir,
            output_filename=_iter_filename,
        )
        await run_single(
            interviewer_client,
            interview_type, product_label, prior_response, vague_seed, _iter_report,
            image_b64=image_b64, image_media_type=image_media_type,
            image_path=image_path, product_description=product_description,
            wireframe_images=wireframe_images,
            run_interview_flag=True,
            is_ollama=use_local,
            skip_judge=_skip_judge, shadow_mode=_shadow_mode,
            judge_model=_judge_model, judge_client=_judge_client,
            laddering_method=laddering_method,
        )
        _iter_report.save()


if __name__ == "__main__":
    asyncio.run(main())

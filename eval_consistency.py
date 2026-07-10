#!/usr/bin/env python3
"""
Consistency and efficacy evaluation for LadderTeam interview transcripts.
Outputs:results/reluctant/consistency_eval_{gt}.json, results/reluctant/consistency_eval_all.json
"""

import argparse
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
GT_ROOT    = SCRIPT_DIR / "ground_truth"
RESULTS_ROOT: Path
OUTPUT_DIR:   Path

GT_ISSUES = {
    "u1_gt1": "'Place Order' CTA is gray on gray and 12px — nearly invisible",
    "u1_gt2": "'Continue Shopping' is the most dominant visual element",
    "u1_gt3": "Price breakdown mixes 8–22px type — no typographic scale",
}
EXPECTED_TERMINAL: dict[str, str] = {
    "acv":   "V",
    "5whys": "ROOT_CAUSE",
    "jtbd":  "B",
}
_GT_SECTION_HEADERS = {
    "acv":   "## ACV GROUND TRUTH SCRIPT",
    "5whys": "## 5-WHYS GROUND TRUTH SCRIPT",
    "jtbd":  "## JTBD GROUND TRUTH SCRIPT",
}
def parse_method(dir_name: str) -> str:
    n = dir_name.lower()
    if "5whys" in n:
        return "5whys"
    if "jtbd" in n:
        return "jtbd"
    if "acv" in n:
        return "acv"
    return "unknown"

def parse_model(dir_name: str) -> str:
    for suffix in ("_5whys", "_acv", "_jtbd"):
        if dir_name.lower().endswith(suffix):
            return dir_name[: -len(suffix)]
    return dir_name

def _extract_say_text(turn_section: str) -> str | None:
    # Trim off ROTATION/SOFTEN blocks only want the primary SAY
    for trim_at in ("**ROTATION", "**SOFTEN", "**What breaks"):
        pos = turn_section.find(trim_at)
        if pos != -1:
            turn_section = turn_section[:pos]
    say_pos = turn_section.find("\nSAY:\n")
    if say_pos == -1:
        return None
    say_block = turn_section[say_pos + len("\nSAY:\n"):]
    lines: list[str] = []
    for line in say_block.split("\n"):
        stripped = line.strip()
        if stripped.startswith("> "):
            lines.append(stripped[2:].strip())
        elif stripped == ">":
            pass  # empty blockquote line — skip
        elif stripped.startswith(">"):
            lines.append(stripped[1:].strip())
        elif lines and not stripped:
            break
        elif lines:
            break
    if not lines:
        return None
    text = " ".join(lines).strip()
    return text

def parse_gt_terminal_responses(gt_path: Path, method: str) -> list[str]:
    if not gt_path.exists():
        return []
    text = gt_path.read_text(encoding="utf-8")
    hdr = _GT_SECTION_HEADERS.get(method)
    if not hdr:
        return []
    start_idx = text.find(hdr)
    if start_idx == -1:
        return []
    end_idx = len(text)
    candidates = list(_GT_SECTION_HEADERS.values()) + [
        "## JTBD QUESTION CLASSIFICATION TABLE",
        "## CONVERGENCE CHECK",
    ]
    for candidate in candidates:
        if candidate == hdr:
            continue
        idx = text.find(candidate, start_idx + 1)
        if idx != -1 and idx < end_idx:
            end_idx = idx

    section = text[start_idx:end_idx]
    design_match = re.search(r"Turn\s+(\d+)\s*[–—\-]\s*(\d+)", section)
    if not design_match:
        return []
    t_start = int(design_match.group(1))
    t_end   = int(design_match.group(2))
    terminal_turn_nums = list(range(t_start, t_end + 1))
    if method == "acv":
        for mirror_match in re.finditer(r"### T(\d+) — IF \[V:MIRROR\]", section):
            t_num = int(mirror_match.group(1))
            if t_num not in terminal_turn_nums:
                terminal_turn_nums.append(t_num)
    if method == "jtbd":
        for stall_match in re.finditer(r"### T(\d+) — IF \[B\] PROBE[^#]*stall broken", section):
            t_num = int(stall_match.group(1))
            if t_num not in terminal_turn_nums:
                terminal_turn_nums.append(t_num)
    responses: list[str] = []
    for t_num in terminal_turn_nums:
        t_header = f"### T{t_num} —"
        t_pos = section.find(t_header)
        if t_pos == -1:
            # Fallback: try plain hyphen form
            t_pos = section.find(f"### T{t_num} -")
        if t_pos == -1:
            continue
        next_pos = section.find("### ", t_pos + len(t_header))
        t_block = section[t_pos: next_pos if next_pos != -1 else len(section)]
        say_text = _extract_say_text(t_block)
        if say_text:
            responses.append(say_text)
    return responses


def _normalize(text: str) -> str:
    #Normalize a response string for comparison
    text = unicodedata.normalize("NFC", text)
    text = text.strip().strip('"').strip("'").strip()
    text = " ".join(text.split())
    return text

def _responses_match(result_text: str, gt_text: str) -> bool:
    r = _normalize(result_text)
    g = _normalize(gt_text)
    if r == g:
        return True
    ratio = SequenceMatcher(None, r, g).ratio()
    return ratio >= 0.85


def check_terminal_gt_match(all_answers: list[str], gt_responses: list[str]) -> bool:
    if not all_answers or not gt_responses:
        return False
    for answer in reversed(all_answers):
        if not answer:
            continue
        for gt_resp in gt_responses:
            if _responses_match(answer, gt_resp):
                return True
    return False

def get_terminal_category(data: dict) -> str:
    summary = data.get("interview_summary") or {}
    if not isinstance(summary, dict):
        return "UNKNOWN"
    stopping_reason = summary.get("stopping_reason") or ""
    if "root-cause" in stopping_reason:
        return "ROOT_CAUSE"
    chains = summary.get("chains") or []
    if chains:
        ep = (chains[0].get("endpoint_type") or "").lower()
        if "root cause" in ep:
            return "ROOT_CAUSE"
        steps = chains[0].get("steps") or []
        if steps:
            t = steps[-1].get("type") or "UNKNOWN"
            return t
    return "UNKNOWN"

def extract_efficacy(data: dict) -> dict:
    jl     = data.get("judge_log")    or {}
    jr     = data.get("judge_report") or {}
    scores = jl.get("scores")         or []
    n      = len(scores)
    defl_vals = [s["deflection_score"] for s in scores if s.get("deflection_score") is not None]
    mean_deflection = round(sum(defl_vals) / len(defl_vals), 3) if defl_vals else None
    rep_flags       = [bool(s.get("repetition_flag", False)) for s in scores]
    repetition_rate = round(sum(rep_flags) / n, 3) if n > 0 else None
    prox_vals = [s.get("unlock_proximity", "") for s in scores]
    proximity_dist = {
        "far":        prox_vals.count("far"),
        "approaching": prox_vals.count("approaching"),
        "near":       prox_vals.count("near"),
    }
    escalation_triggered = bool(jl.get("escalation_triggered", False))
    escalation_at_turn   = jl.get("escalation_at_turn")
    leff = jr.get("laddering_efficiency")
    laddering_efficiency = round(leff, 3) if leff is not None else None
    drift_count = int(data.get("drift_events_count") or 0)
    depth       = int(data.get("interview_depth")    or 0)
    drift_rate  = round(drift_count / depth, 3) if depth > 0 else 0.0
    return {
        "mean_deflection_score":         mean_deflection,
        "repetition_rate":               repetition_rate,
        "unlock_proximity_distribution": proximity_dist,
        "escalation_triggered":          escalation_triggered,
        "escalation_at_turn":            escalation_at_turn,
        "laddering_efficiency":          laddering_efficiency,
        "drift_rate":                    drift_rate,
    }


def load_run(path: Path) -> dict:
    for enc in ("utf-8", "latin-1"):
        try:
            with open(path, encoding=enc) as f:
                data = json.load(f)
            return data[0] if isinstance(data, list) else data
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    raise ValueError(f"Cannot parse {path}")


def iter_json_files(directory: Path) -> list[Path]:
    return sorted(
        p for p in directory.iterdir()
        if p.is_file() and p.suffix == ".json" and not p.name.startswith(".")
    )

def process_run(path: Path, gt_responses: list[str] | None = None) -> dict:
    data = load_run(path)
    converged    = bool(data.get("terminated_naturally", False))
    terminal_cat = get_terminal_category(data)
    turn_count   = int(data.get("interview_depth") or 0)
    turns        = data.get("turns") or []
    final_answer = turns[-1]["a"] if turns else None
    all_answers  = [t["a"] for t in turns if t.get("a")]
    terminal_gt_match: bool | None = None
    if gt_responses is not None:
        terminal_gt_match = check_terminal_gt_match(all_answers, gt_responses)
    record = {
        "file":               path.name,
        "converged":          converged,
        "terminal_category":  terminal_cat,
        "terminal_gt_match":  terminal_gt_match,
        "turn_count":         turn_count,
        "final_answer":       final_answer,
    }
    record.update(extract_efficacy(data))
    return record

def _safe_mean(vals: list) -> float | None:
    clean = [v for v in vals if v is not None]
    return round(sum(clean) / len(clean), 3) if clean else None


def aggregate_group(model: str, method: str, iterations: list) -> dict:
    expected = EXPECTED_TERMINAL.get(method, "UNKNOWN")

    converged_count = sum(1 for it in iterations if it["converged"])
    terminal_cats   = [it["terminal_category"] for it in iterations]
    match_count     = sum(1 for cat in terminal_cats if cat == expected)
    gt_match_vals  = [it["terminal_gt_match"] for it in iterations if it["terminal_gt_match"] is not None]
    gt_match_count = sum(1 for v in gt_match_vals if v)
    gt_match_denom = len(gt_match_vals)
    turn_counts = [it["turn_count"] for it in iterations if it.get("turn_count") is not None]
    prox_mean: dict[str, float] = {}
    for key in ("far", "approaching", "near"):
        vals = [
            it["unlock_proximity_distribution"][key]
            for it in iterations
            if "unlock_proximity_distribution" in it
        ]
        prox_mean[key] = round(sum(vals) / len(vals), 2) if vals else 0.0

    return {
        "model":  model,
        "method": method,
        "expected_terminal_category": expected,
        "convergence_rate": f"{converged_count}/{len(iterations)}",
        "all_converged":    converged_count == len(iterations),
        "terminal_categories":   terminal_cats,
        "category_match_rate":   f"{match_count}/{len(iterations)}",
        "all_match_expected":    match_count == len(iterations),
        "categories_consistent": len(set(terminal_cats)) == 1,
        "terminal_gt_match_rate": f"{gt_match_count}/{gt_match_denom}" if gt_match_denom > 0 else "N/A",
        "all_gt_match":           gt_match_count == gt_match_denom if gt_match_denom > 0 else None,
        "turn_counts":      [it["turn_count"] for it in iterations],
        "turn_count_mean":  _safe_mean(turn_counts),
        "turn_count_min":   min(turn_counts)                          if turn_counts else None,
        "turn_count_max":   max(turn_counts)                          if turn_counts else None,
        "turn_count_range": (max(turn_counts) - min(turn_counts))     if len(turn_counts) > 1 else 0,
        "mean_deflection_score_mean":         _safe_mean([it.get("mean_deflection_score")  for it in iterations]),
        "repetition_rate_mean":               _safe_mean([it.get("repetition_rate")         for it in iterations]),
        "escalation_triggered_any":           any(it.get("escalation_triggered", False)     for it in iterations),
        "laddering_efficiency_mean":          _safe_mean([it.get("laddering_efficiency")    for it in iterations]),
        "drift_rate_mean":                    _safe_mean([it.get("drift_rate")              for it in iterations]),
        "unlock_proximity_distribution_mean": prox_mean,
        "iterations": iterations,
    }


def evaluate_gt(gt_dir: Path, gt_name: str) -> dict:
    persona = RESULTS_ROOT.name  # e.g. "reluctant"
    gt_path = GT_ROOT / f"{persona}_{gt_name}.md"
    gt_responses_by_method: dict[str, list[str]] = {}
    for method in ("acv", "5whys", "jtbd"):
        responses = parse_gt_terminal_responses(gt_path, method)
        gt_responses_by_method[method] = responses
        if not responses:
            print(f"  [warn] no GT terminal responses parsed for {gt_name}/{method}", file=sys.stderr)
    groups: list[dict] = []
    for mm_dir in sorted(gt_dir.iterdir()):
        if not mm_dir.is_dir() or mm_dir.name.startswith(".") or mm_dir.name == "removed":
            continue
        method = parse_method(mm_dir.name)
        model  = parse_model(mm_dir.name)
        if method == "unknown":
            continue
        run_files = iter_json_files(mm_dir)
        if not run_files:
            print(f"  [skip] {gt_name}/{mm_dir.name} — no JSON files", file=sys.stderr)
            continue
        gt_responses = gt_responses_by_method.get(method, [])
        iterations: list[dict] = []
        for path in run_files:
            try:
                iterations.append(process_run(path, gt_responses=gt_responses))
            except Exception as exc:
                print(f"  [warn] {path.name}: {exc}", file=sys.stderr)
                iterations.append({
                    "file":               path.name,
                    "error":              str(exc),
                    "converged":          False,
                    "terminal_category":  "ERROR",
                    "terminal_gt_match":  None,
                    "turn_count":         None,
                    "final_answer":       None,
                    "mean_deflection_score":          None,
                    "repetition_rate":                None,
                    "unlock_proximity_distribution":  {"far": 0, "approaching": 0, "near": 0},
                    "escalation_triggered":           False,
                    "escalation_at_turn":             None,
                    "laddering_efficiency":           None,
                    "drift_rate":                     None,
                })
        groups.append(aggregate_group(model, method, iterations))
    total       = len(groups)
    fully_ok    = sum(1 for g in groups if g["all_converged"] and g["all_match_expected"] and g["categories_consistent"])
    total_iters = sum(len(g["iterations"]) for g in groups)
    conv_iters  = sum(sum(1 for it in g["iterations"] if it["converged"]) for g in groups)
    match_iters = sum(
        sum(1 for it in g["iterations"] if it["terminal_category"] == g["expected_terminal_category"])
        for g in groups
    )
    gt_match_iters = sum(
        sum(1 for it in g["iterations"] if it.get("terminal_gt_match") is True)
        for g in groups
    )
    gt_match_eligible = sum(
        sum(1 for it in g["iterations"] if it.get("terminal_gt_match") is not None)
        for g in groups
    )
    return {
        "ground_truth": gt_name,
        "issue":        GT_ISSUES.get(gt_name, ""),
        "groups":       groups,
        "summary": {
            "total_groups":                    total,
            "fully_consistent_groups":         f"{fully_ok}/{total}",
            "overall_convergence_rate":        f"{conv_iters}/{total_iters}",
            "overall_category_match_rate":     f"{match_iters}/{total_iters}",
            "overall_gt_response_match_rate":  f"{gt_match_iters}/{gt_match_eligible}" if gt_match_eligible > 0 else "N/A",
        },
    }

def print_table(all_results: list[dict], persona: str = "") -> None:
    W = 155
    label = persona.upper() if persona else "ALL"
    print("\n" + "=" * W)
    print(f"LADDERCHAT CONSISTENCY + EFFICACY EVALUATION — {label} PERSONA")
    print("=" * W)
    print(
        f"  {'GT':<8} {'Model':<14} {'Method':<8} "
        f"{'Converge':<10} {'CatMatch':<10} {'GTMatch':<9} {'Consist':<9} "
        f"{'Turns(avg)':<12} {'LEff':<7} {'Defl':<6} {'RepRate':<9} "
        f"{'Escal':<7} {'Drift':<7}  Cats"
    )
    print("-" * W)
    for gt_data in all_results:
        gt = gt_data["ground_truth"]
        print(f"\n  {gt}  —  {gt_data['issue']}")
        for g in sorted(gt_data["groups"], key=lambda x: (x["method"], x["model"])):
            esc  = "YES" if g["escalation_triggered_any"]  else "no"
            cons = "YES" if g["categories_consistent"]     else "NO "
            def _fmt(v) -> str:
                return "N/A" if v is None else str(v)
            print(
                f"  {gt:<8} {g['model']:<14} {g['method']:<8} "
                f"{g['convergence_rate']:<10} {g['category_match_rate']:<10} "
                f"{g['terminal_gt_match_rate']:<9} {cons:<9} "
                f"{_fmt(g['turn_count_mean']):<12} "
                f"{_fmt(g.get('laddering_efficiency_mean')):<7} "
                f"{_fmt(g.get('mean_deflection_score_mean')):<6} "
                f"{_fmt(g.get('repetition_rate_mean')):<9} "
                f"{esc:<7} {_fmt(g.get('drift_rate_mean')):<7}  "
                f"{g['terminal_categories']}"
            )
        s = gt_data["summary"]
        print(
            f"  {'':8} {'── TOTALS ──':14} {'':8} "
            f"conv={s['overall_convergence_rate']:<8} "
            f"cat={s['overall_category_match_rate']:<9} "
            f"gt={s['overall_gt_response_match_rate']:<9} "
            f"fully_ok={s['fully_consistent_groups']}"
        )
    print()


def main() -> None:
    global RESULTS_ROOT, OUTPUT_DIR
    parser = argparse.ArgumentParser(description="LadderChat consistency + efficacy evaluator")
    parser.add_argument(
        "--persona",
        default="reluctant",
        help="Persona subdirectory under results/ to evaluate (default: reluctant)",
    )
    args = parser.parse_args()
    persona = args.persona.lower()
    RESULTS_ROOT = SCRIPT_DIR / "results" / persona
    OUTPUT_DIR   = RESULTS_ROOT
    if not RESULTS_ROOT.exists():
        print(f"ERROR: results directory not found: {RESULTS_ROOT}", file=sys.stderr)
        sys.exit(1)
    all_results: list[dict] = []
    for gt_dir in sorted(RESULTS_ROOT.iterdir()):
        if not gt_dir.is_dir() or gt_dir.name.startswith("."):
            continue
        gt_name = gt_dir.name
        if gt_name not in GT_ISSUES:
            continue
        print(f"Evaluating {gt_name}…")
        result = evaluate_gt(gt_dir, gt_name)
        all_results.append(result)
        out_path = OUTPUT_DIR / f"consistency_eval_{gt_name}.json"
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"  → {out_path.relative_to(SCRIPT_DIR)}")
    combined_path = OUTPUT_DIR / "consistency_eval_all.json"
    with open(combined_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"  → {combined_path.relative_to(SCRIPT_DIR)}")
    print_table(all_results, persona=persona)
    print("Done.")


if __name__ == "__main__":
    main()

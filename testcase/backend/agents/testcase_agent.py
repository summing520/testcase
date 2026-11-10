from backend.tools.task_tools import (
    evaluate_testcase,
    generate_draft,
    load_task_bundle,
    log_agent_run,
    load_single_markdown_doc,
    revise_testcase,
    save_generated_result,
    supplement_db_testcases,
    supplement_institution_db_testcases,
)

_DB_DOC_APP = "docs/knowledge/db/APP用户流程涉及表.md"
_DB_DOC_HUB = "docs/knowledge/db/HUB用户流程涉及表.md"
_INSTITUTION_DB_VALIDATION_DOC = "docs/rules/机构对接落表数据验证项.md"


def _db_phase1_message(inferred_kind: str) -> str:
    if inferred_kind == "institution":
        return (
            "已勾选数据库表：将先生成接口流程用例，随后依据《机构对接落表数据验证项》"
            "按当前流程涉及接口范围补充落库数据测试用例"
        )
    return "已勾选数据库表：将先生成接口流程用例，随后再补齐 DB 表用例"


def _strip_db_docs_from_bundle(bundle: dict) -> None:
    """Ensure DB table knowledge docs are NOT injected during base flow generation."""
    kd = bundle.get("knowledge_docs") or {}
    if not isinstance(kd, dict) or not kd:
        return
    for p in (_DB_DOC_APP, _DB_DOC_HUB):
        if p in kd:
            kd.pop(p, None)
    bundle["knowledge_docs"] = kd


def _institution_db_scope(bundle: dict, markdown: str) -> dict:
    from backend.services.institution_db_scope import resolve_institution_db_validation_scope

    gen_opts = bundle.get("generation_options") or {}
    req_title = (
        str(gen_opts.get("requirement_title") or "").strip()
        if isinstance(gen_opts, dict)
        else ""
    )
    knowledge = bundle.get("knowledge_docs") or {}
    external_md = (
        knowledge.get("external_cooperation_markdown", "")
        if isinstance(knowledge, dict)
        else ""
    )
    if not str(external_md or "").strip():
        probe = resolve_institution_db_validation_scope(
            check_items=bundle.get("check_items") or [],
            requirement_markdown=bundle.get("requirement_markdown") or "",
            requirement_title=req_title,
            external_cooperation_markdown="",
            generated_testcase_markdown=markdown,
        )
        iface_path = probe.get("interface_doc_path") or ""
        if iface_path:
            try:
                external_md = load_single_markdown_doc(iface_path, kind="knowledge")
            except Exception:  # noqa: BLE001
                external_md = ""

    return resolve_institution_db_validation_scope(
        check_items=bundle.get("check_items") or [],
        requirement_markdown=bundle.get("requirement_markdown") or "",
        requirement_title=req_title,
        external_cooperation_markdown=str(external_md or ""),
        generated_testcase_markdown=markdown,
    )


def _institution_db_start_message(scope: dict) -> str:
    included = scope.get("included_stages") or []
    excluded = scope.get("excluded_stages") or []
    msg = (
        "开始补充生成落库数据测试用例（依据机构对接落表数据验证项；"
        f"涉及环节：{'、'.join(included) or '无'}"
    )
    if excluded:
        msg += f"；跳过：{'、'.join(excluded)}"
    return msg + "）"


def _run_db_supplement(
    *,
    task_id: str,
    iteration: int,
    markdown: str,
    inferred_kind: str,
    bundle: dict,
    llm,
    reporter,
    score: int = 0,
) -> None:
    """Phase 2: supplement DB / 落库 testcases after flow generation completed."""
    if inferred_kind == "institution":
        action_label = "落库数据测试用例补充完成"
        fail_label = "落库数据测试用例补充失败"
        scope = _institution_db_scope(bundle, markdown)
        start_message = _institution_db_start_message(scope)

        def _generate() -> str:
            validation_doc = load_single_markdown_doc(_INSTITUTION_DB_VALIDATION_DOC, kind="rule")
            flow_tables_doc = load_single_markdown_doc(_DB_DOC_APP, kind="knowledge")
            return supplement_institution_db_testcases(
                markdown,
                validation_doc,
                flow_tables_doc,
                llm,
                scope_context=scope.get("scope_summary") or "",
            ).strip()

    elif inferred_kind == "channel":
        action_label = "数据库表相关用例补充完成"
        fail_label = "数据库表用例补充失败"
        start_message = "开始补充生成数据库表相关测试用例"

        def _generate() -> str:
            db_doc_text = load_single_markdown_doc(_DB_DOC_HUB, kind="knowledge")
            return supplement_db_testcases(markdown, db_doc_text, llm).strip()

    else:
        return

    if reporter:
        reporter({"stage": "db", "iteration": iteration, "message": start_message})

    try:
        addition = _generate()
    except Exception as exc:  # noqa: BLE001
        log_agent_run(task_id, iteration, "db_supplement", f"{fail_label}：{exc}")
        if reporter:
            reporter({"stage": "db", "iteration": iteration, "message": f"{fail_label}：{exc}"})
        return

    if not addition:
        return

    try:
        merged = (markdown.rstrip() + "\n\n---\n\n" + addition + "\n").strip() + "\n"
        save_generated_result(
            task_id,
            merged,
            {"stage": "db_supplement", "iteration": iteration, "score": score, "pass": False},
            status="generated",
        )
        log_agent_run(task_id, iteration, "db_supplement", action_label)
        if reporter:
            reporter({"stage": "db", "iteration": iteration, "message": action_label})
    except Exception as exc:  # noqa: BLE001
        log_agent_run(task_id, iteration, "db_supplement", f"{fail_label}：{exc}")
        if reporter:
            reporter({"stage": "db", "iteration": iteration, "message": f"{fail_label}：{exc}"})


def run_testcase_agent(task_id: str, llm, max_iterations: int = 3, pass_score: int = 85) -> dict:
    return run_testcase_agent_with_reporter(
        task_id, llm, max_iterations=max_iterations, pass_score=pass_score, reporter=None
    )


def run_testcase_agent_with_reporter(
    task_id: str,
    llm,
    *,
    max_iterations: int = 3,
    pass_score: int = 85,
    reporter=None,
) -> dict:
    bundle = load_task_bundle(task_id)
    gen_opts = bundle.get("generation_options") or {}
    tc_types = (gen_opts.get("testcase_types") or {}) if isinstance(gen_opts, dict) else {}
    include_db = bool(tc_types.get("db"))
    inferred_kind = gen_opts.get("inferred_kind") if isinstance(gen_opts, dict) else None
    if inferred_kind not in ("institution", "channel"):
        req_kind = bundle.get("requirement_kind")
        if req_kind in ("institution", "channel"):
            inferred_kind = req_kind
        else:
            inferred_kind = "unknown"

    if inferred_kind not in ("institution", "channel"):
        if include_db and reporter:
            reporter(
                {
                    "stage": "db",
                    "iteration": 0,
                    "message": "其它需求未勾选专用库表文档，将仅基于需求正文生成",
                }
            )
        draft = generate_draft(bundle, llm)
        log_agent_run(task_id, 0, "generate", "其它需求：初稿生成完成")
        save_generated_result(
            task_id,
            draft,
            {"stage": "generate", "iteration": 0, "score": 0, "pass": True},
            status="generated",
        )
        if reporter:
            reporter(
                {
                    "stage": "complete",
                    "iteration": 0,
                    "message": "其它需求：已直接生成测试用例（未使用业务规则与 Demo）",
                }
            )
        return {"pass": True, "score": 0, "feedback": []}

    # Phase 1: always generate the flow testcases first; never inject the DB table docs here.
    if include_db:
        _strip_db_docs_from_bundle(bundle)
        if reporter:
            reporter({"stage": "db", "iteration": 0, "message": _db_phase1_message(inferred_kind)})

    draft = generate_draft(bundle, llm)
    log_agent_run(task_id, 0, "generate", "初稿生成完成")
    # Persist an early checkpoint so preview isn't empty if streaming stops mid-run.
    save_generated_result(task_id, draft, {"stage": "generate", "iteration": 0, "score": 0, "pass": False}, status="generating")
    if reporter:
        reporter({"stage": "generate", "iteration": 0, "message": "初稿生成完成"})

    best_markdown = draft
    best_eval = {"score": 0, "pass": False, "feedback": []}

    current = draft
    for i in range(1, max_iterations + 1):
        evaluation = evaluate_testcase(current, bundle, llm)
        log_agent_run(task_id, i, "evaluate", f"评估完成，score={evaluation.get('score')}", evaluation)
        if reporter:
            reporter(
                {
                    "stage": "evaluate",
                    "iteration": i,
                    "message": f"评估完成，score={evaluation.get('score')}",
                    "evaluation": evaluation,
                }
            )

        score = evaluation.get("score", 0)
        if score >= best_eval.get("score", 0):
            best_eval = evaluation
            best_markdown = current
            # Keep checkpoint synced with the best-so-far result for preview/debugging.
            save_generated_result(task_id, best_markdown, best_eval, status="generating")

        passed = bool(evaluation.get("pass")) or score >= pass_score
        if passed:
            save_generated_result(task_id, current, evaluation, status="generated")
            log_agent_run(task_id, i, "complete", "达到通过阈值，结束")
            if reporter:
                reporter({"stage": "complete", "iteration": i, "message": "达到通过阈值，结束"})
            # Phase 2 (optional): supplement DB table related testcases after flow generation completed.
            if include_db:
                _run_db_supplement(
                    task_id=task_id,
                    iteration=i,
                    markdown=current,
                    inferred_kind=inferred_kind,
                    bundle=bundle,
                    llm=llm,
                    reporter=reporter,
                    score=evaluation.get("score", 0),
                )
            return evaluation

        feedback = evaluation.get("feedback", [])
        current = revise_testcase(current, feedback, bundle, llm)
        log_agent_run(task_id, i, "revise", "按反馈修订完成")
        # Persist checkpoint after revise as well (useful if next evaluate hangs).
        save_generated_result(
            task_id,
            current,
            {"stage": "revise", "iteration": i, "score": best_eval.get("score", 0), "pass": False},
            status="generating",
        )
        if reporter:
            reporter({"stage": "revise", "iteration": i, "message": "按反馈修订完成", "feedback": feedback})

    # Use current as the latest full text after the last revise; best_markdown is "best score so far".
    final_markdown = current
    final_eval = best_eval
    save_generated_result(task_id, final_markdown, final_eval, status="generated")
    log_agent_run(task_id, max_iterations, "complete", "达到最大迭代次数，输出最佳结果", best_eval)
    if reporter:
        reporter(
            {
                "stage": "complete",
                "iteration": max_iterations,
                "message": "达到最大迭代次数，输出最佳结果",
                "evaluation": best_eval,
            }
        )

    # Phase 2 (optional): supplement DB table related testcases after flow generation completed.
    if include_db:
        _run_db_supplement(
            task_id=task_id,
            iteration=max_iterations,
            markdown=final_markdown,
            inferred_kind=inferred_kind,
            bundle=bundle,
            llm=llm,
            reporter=reporter,
            score=final_eval.get("score", 0),
        )

    return best_eval

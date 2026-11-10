-- =============================================================================
-- SQLite → MySQL 数据迁移 — 第 3 步：清理 staging 与临时函数
-- =============================================================================

USE `qa`;

DROP FUNCTION IF EXISTS `qa_fn_iso_to_datetime`;
DROP FUNCTION IF EXISTS `qa_fn_text_to_json`;
DROP FUNCTION IF EXISTS `qa_fn_text_to_json_nullable`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `_stg_tasks`;
DROP TABLE IF EXISTS `_stg_task_check_items`;
DROP TABLE IF EXISTS `_stg_test_case_library`;
DROP TABLE IF EXISTS `_stg_task_agent_runs`;
DROP TABLE IF EXISTS `_stg_checklist_item_memory`;
DROP TABLE IF EXISTS `_stg_pipeline_config`;

SET FOREIGN_KEY_CHECKS = 1;

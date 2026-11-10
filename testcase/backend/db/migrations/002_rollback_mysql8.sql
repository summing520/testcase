-- =============================================================================
-- Test Case Generator — MySQL 8 回滚脚本（删除 testcase_ 前缀表）
-- 警告：将永久删除本应用全部持久化数据，生产环境慎用。
-- =============================================================================

SET NAMES utf8mb4;

USE `qa`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `testcase_task_check_items`;
DROP TABLE IF EXISTS `testcase_test_case_library`;
DROP TABLE IF EXISTS `testcase_task_agent_runs`;
DROP TABLE IF EXISTS `testcase_checklist_item_memory`;
DROP TABLE IF EXISTS `testcase_pipeline_config`;
DROP TABLE IF EXISTS `testcase_tasks`;

SET FOREIGN_KEY_CHECKS = 1;

-- 若需连库一并删除，取消下一行注释：
-- DROP DATABASE IF EXISTS `qa`;

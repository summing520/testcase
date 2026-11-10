-- =============================================================================
-- SQLite → MySQL 数据迁移 — 第 1 步：创建临时 staging 表
-- 库名：qa
--
-- 执行顺序：
--   001_init_mysql8.sql          建目标表 testcase_*
--   003_sqlite_staging_tables.sql  本文件
--   （把 SQLite 数据导入 staging，见下方说明）
--   004_migrate_staging_to_qa.sql  转换并写入 testcase_*
--   005_drop_staging_tables.sql    可选，清理 staging
--
-- =============================================================================
-- 如何把 SQLite 数据放进 staging（任选一种）
-- =============================================================================
--
-- 【方式 A — 推荐】sqlite3 导出 CSV，MySQL LOAD DATA
--
--   在项目根目录，SQLite 文件默认路径 data/test_case_generation.db
--
--   sqlite3 -header -csv data/test_case_generation.db ^
--     "SELECT id, status, requirement_url, COALESCE(external_cooperation_url,''), selected_knowledge_docs, selected_checklist_docs, selected_rule_docs, requirement_markdown, external_cooperation_markdown, confirmed_check_items, generated_testcase_markdown, created_at, updated_at, COALESCE(requirement_kind,''), COALESCE(inferred_checklist_doc,''), generation_options_json FROM tasks;" ^
--     > _stg_tasks.csv
--   sqlite3 -header -csv data/test_case_generation.db "SELECT id, task_id, item_key, item_text, matched_text, confirmed_text, match_source, is_edited, created_at, updated_at FROM task_check_items;" > _stg_task_check_items.csv
--   sqlite3 -header -csv data/test_case_generation.db "SELECT id, task_id, title, content_markdown, adopted_at FROM test_case_library;" > _stg_test_case_library.csv
--   sqlite3 -header -csv data/test_case_generation.db "SELECT id, task_id, iteration, action, observation, score_json, created_at FROM task_agent_runs;" > _stg_task_agent_runs.csv
--   sqlite3 -header -csv data/test_case_generation.db "SELECT checklist_fingerprint, item_text, remembered_value, source_task_id, updated_at FROM checklist_item_memory;" > _stg_checklist_item_memory.csv
--   sqlite3 -header -csv data/test_case_generation.db "SELECT id, config_json, updated_at FROM pipeline_config;" > _stg_pipeline_config.csv
--
--   然后在 MySQL 客户端执行（路径按实际修改；Windows 注意反斜杠或正斜杠）：
--
--   LOAD DATA LOCAL INFILE 'D:/git/ai/testcase/_stg_tasks.csv'
--     INTO TABLE `_stg_tasks`
--     CHARACTER SET utf8mb4
--     FIELDS TERMINATED BY ',' ENCLOSED BY '"' ESCAPED BY '\\'
--     LINES TERMINATED BY '\n'
--     IGNORE 1 LINES;
--   （对其余 5 张 staging 表重复 LOAD DATA）
--
-- 【方式 B】用任意 SQL 客户端，把 SQLite 各表数据手工 INSERT 进 `_stg_*` 表
--
-- 【方式 C】若 staging 表已有数据需重导，先 TRUNCATE `_stg_*` 再导入
-- =============================================================================

SET NAMES utf8mb4;
SET time_zone = '+00:00';

USE `qa`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `_stg_tasks`;
DROP TABLE IF EXISTS `_stg_task_check_items`;
DROP TABLE IF EXISTS `_stg_test_case_library`;
DROP TABLE IF EXISTS `_stg_task_agent_runs`;
DROP TABLE IF EXISTS `_stg_checklist_item_memory`;
DROP TABLE IF EXISTS `_stg_pipeline_config`;

-- 列名与 SQLite 原表一致；类型统一 LONGTEXT 便于 CSV 导入
CREATE TABLE `_stg_tasks` (
  `id` LONGTEXT NULL,
  `status` LONGTEXT NULL,
  `requirement_url` LONGTEXT NULL,
  `external_cooperation_url` LONGTEXT NULL,
  `selected_knowledge_docs` LONGTEXT NULL,
  `selected_checklist_docs` LONGTEXT NULL,
  `selected_rule_docs` LONGTEXT NULL,
  `requirement_markdown` LONGTEXT NULL,
  `external_cooperation_markdown` LONGTEXT NULL,
  `confirmed_check_items` LONGTEXT NULL,
  `generated_testcase_markdown` LONGTEXT NULL,
  `created_at` LONGTEXT NULL,
  `updated_at` LONGTEXT NULL,
  `requirement_kind` LONGTEXT NULL,
  `inferred_checklist_doc` LONGTEXT NULL,
  `generation_options_json` LONGTEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `_stg_task_check_items` (
  `id` LONGTEXT NULL,
  `task_id` LONGTEXT NULL,
  `item_key` LONGTEXT NULL,
  `item_text` LONGTEXT NULL,
  `matched_text` LONGTEXT NULL,
  `confirmed_text` LONGTEXT NULL,
  `match_source` LONGTEXT NULL,
  `is_edited` LONGTEXT NULL,
  `created_at` LONGTEXT NULL,
  `updated_at` LONGTEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `_stg_test_case_library` (
  `id` LONGTEXT NULL,
  `task_id` LONGTEXT NULL,
  `title` LONGTEXT NULL,
  `content_markdown` LONGTEXT NULL,
  `adopted_at` LONGTEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `_stg_task_agent_runs` (
  `id` LONGTEXT NULL,
  `task_id` LONGTEXT NULL,
  `iteration` LONGTEXT NULL,
  `action` LONGTEXT NULL,
  `observation` LONGTEXT NULL,
  `score_json` LONGTEXT NULL,
  `created_at` LONGTEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `_stg_checklist_item_memory` (
  `checklist_fingerprint` LONGTEXT NULL,
  `item_text` LONGTEXT NULL,
  `remembered_value` LONGTEXT NULL,
  `source_task_id` LONGTEXT NULL,
  `updated_at` LONGTEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `_stg_pipeline_config` (
  `id` LONGTEXT NULL,
  `config_json` LONGTEXT NULL,
  `updated_at` LONGTEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

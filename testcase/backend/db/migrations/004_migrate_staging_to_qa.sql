-- =============================================================================
-- SQLite → MySQL 数据迁移 — 第 2 步：staging → testcase_* 目标表
-- 前置：001 已执行；003 已执行且 `_stg_*` 中已有数据
-- =============================================================================

SET NAMES utf8mb4;
SET time_zone = '+00:00';

USE `qa`;

-- ---------------------------------------------------------------------------
-- 辅助函数（迁移完成后由 005 删除）
-- ---------------------------------------------------------------------------
DROP FUNCTION IF EXISTS `qa_fn_iso_to_datetime`;
DROP FUNCTION IF EXISTS `qa_fn_text_to_json`;
DROP FUNCTION IF EXISTS `qa_fn_text_to_json_nullable`;

DELIMITER //

CREATE FUNCTION `qa_fn_iso_to_datetime`(iso_str TEXT)
RETURNS DATETIME(3)
DETERMINISTIC
NO SQL
BEGIN
  DECLARE s VARCHAR(64);
  IF iso_str IS NULL OR TRIM(iso_str) = '' THEN
    RETURN UTC_TIMESTAMP(3);
  END IF;
  SET s = TRIM(iso_str);
  SET s = REPLACE(s, 'T', ' ');
  SET s = REPLACE(s, 'Z', '');
  SET s = REPLACE(s, '+00:00', '');
  RETURN CAST(s AS DATETIME(3));
END//

CREATE FUNCTION `qa_fn_text_to_json`(txt TEXT)
RETURNS JSON
DETERMINISTIC
NO SQL
BEGIN
  IF txt IS NULL OR TRIM(txt) = '' THEN
    RETURN JSON_ARRAY();
  END IF;
  IF JSON_VALID(txt) THEN
    RETURN CAST(txt AS JSON);
  END IF;
  RETURN JSON_ARRAY();
END//

CREATE FUNCTION `qa_fn_text_to_json_nullable`(txt TEXT)
RETURNS JSON
DETERMINISTIC
NO SQL
BEGIN
  IF txt IS NULL OR TRIM(txt) = '' THEN
    RETURN NULL;
  END IF;
  IF JSON_VALID(txt) THEN
    RETURN CAST(txt AS JSON);
  END IF;
  RETURN NULL;
END//

DELIMITER ;

-- ---------------------------------------------------------------------------
-- 清空目标表（若需保留已有 MySQL 数据，请注释掉本段）
-- ---------------------------------------------------------------------------
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE `testcase_task_check_items`;
TRUNCATE TABLE `testcase_test_case_library`;
TRUNCATE TABLE `testcase_task_agent_runs`;
TRUNCATE TABLE `testcase_checklist_item_memory`;
TRUNCATE TABLE `testcase_pipeline_config`;
TRUNCATE TABLE `testcase_tasks`;

SET FOREIGN_KEY_CHECKS = 1;

-- ---------------------------------------------------------------------------
-- 1. tasks → testcase_tasks
-- ---------------------------------------------------------------------------
INSERT INTO `testcase_tasks` (
  `id`, `status`, `requirement_url`, `external_cooperation_url`,
  `selected_knowledge_docs`, `selected_checklist_docs`, `selected_rule_docs`,
  `requirement_markdown`, `external_cooperation_markdown`,
  `confirmed_check_items`, `generated_testcase_markdown`,
  `requirement_kind`, `inferred_checklist_doc`, `generation_options_json`,
  `created_at`, `updated_at`
)
SELECT
  TRIM(`id`),
  TRIM(`status`),
  TRIM(`requirement_url`),
  COALESCE(TRIM(`external_cooperation_url`), ''),
  `qa_fn_text_to_json`(`selected_knowledge_docs`),
  `qa_fn_text_to_json`(`selected_checklist_docs`),
  `qa_fn_text_to_json`(`selected_rule_docs`),
  `requirement_markdown`,
  `external_cooperation_markdown`,
  `qa_fn_text_to_json_nullable`(`confirmed_check_items`),
  `generated_testcase_markdown`,
  COALESCE(NULLIF(TRIM(`requirement_kind`), ''), ''),
  COALESCE(NULLIF(TRIM(`inferred_checklist_doc`), ''), ''),
  `qa_fn_text_to_json_nullable`(`generation_options_json`),
  `qa_fn_iso_to_datetime`(`created_at`),
  `qa_fn_iso_to_datetime`(`updated_at`)
FROM `_stg_tasks`
WHERE `id` IS NOT NULL AND TRIM(`id`) <> '';

-- ---------------------------------------------------------------------------
-- 2. task_check_items → testcase_task_check_items（保留原 id）
-- ---------------------------------------------------------------------------
INSERT INTO `testcase_task_check_items` (
  `id`, `task_id`, `item_key`, `item_text`,
  `matched_text`, `confirmed_text`, `match_source`, `is_edited`,
  `created_at`, `updated_at`
)
SELECT
  CAST(`id` AS UNSIGNED),
  TRIM(`task_id`),
  TRIM(`item_key`),
  `item_text`,
  `matched_text`,
  `confirmed_text`,
  NULLIF(TRIM(`match_source`), ''),
  CASE WHEN TRIM(COALESCE(`is_edited`, '0')) IN ('1', 'true', 'TRUE') THEN 1 ELSE 0 END,
  `qa_fn_iso_to_datetime`(`created_at`),
  `qa_fn_iso_to_datetime`(`updated_at`)
FROM `_stg_task_check_items`
WHERE `task_id` IS NOT NULL AND TRIM(`task_id`) <> ''
  AND `item_key` IS NOT NULL AND TRIM(`item_key`) <> ''
  AND EXISTS (SELECT 1 FROM `testcase_tasks` t WHERE t.`id` = TRIM(`task_id`));

SET @max_ci := (SELECT COALESCE(MAX(`id`), 0) FROM `testcase_task_check_items`);
SET @sql_ci := CONCAT('ALTER TABLE `testcase_task_check_items` AUTO_INCREMENT = ', @max_ci + 1);
PREPARE stmt_ci FROM @sql_ci;
EXECUTE stmt_ci;
DEALLOCATE PREPARE stmt_ci;

-- ---------------------------------------------------------------------------
-- 3. test_case_library → testcase_test_case_library
-- ---------------------------------------------------------------------------
INSERT INTO `testcase_test_case_library` (
  `id`, `task_id`, `title`, `content_markdown`, `adopted_at`
)
SELECT
  CAST(`id` AS UNSIGNED),
  TRIM(`task_id`),
  TRIM(`title`),
  `content_markdown`,
  `qa_fn_iso_to_datetime`(`adopted_at`)
FROM `_stg_test_case_library`
WHERE `task_id` IS NOT NULL AND TRIM(`task_id`) <> ''
  AND EXISTS (SELECT 1 FROM `testcase_tasks` t WHERE t.`id` = TRIM(`task_id`));

SET @max_lib := (SELECT COALESCE(MAX(`id`), 0) FROM `testcase_test_case_library`);
SET @sql_lib := CONCAT('ALTER TABLE `testcase_test_case_library` AUTO_INCREMENT = ', @max_lib + 1);
PREPARE stmt_lib FROM @sql_lib;
EXECUTE stmt_lib;
DEALLOCATE PREPARE stmt_lib;

-- ---------------------------------------------------------------------------
-- 4. task_agent_runs → testcase_task_agent_runs
-- ---------------------------------------------------------------------------
INSERT INTO `testcase_task_agent_runs` (
  `id`, `task_id`, `iteration`, `action`, `observation`, `score_json`, `created_at`
)
SELECT
  CAST(`id` AS UNSIGNED),
  TRIM(`task_id`),
  CAST(`iteration` AS SIGNED),
  TRIM(`action`),
  `observation`,
  `qa_fn_text_to_json_nullable`(`score_json`),
  `qa_fn_iso_to_datetime`(`created_at`)
FROM `_stg_task_agent_runs`
WHERE `task_id` IS NOT NULL AND TRIM(`task_id`) <> ''
  AND EXISTS (SELECT 1 FROM `testcase_tasks` t WHERE t.`id` = TRIM(`task_id`));

SET @max_run := (SELECT COALESCE(MAX(`id`), 0) FROM `testcase_task_agent_runs`);
SET @sql_run := CONCAT('ALTER TABLE `testcase_task_agent_runs` AUTO_INCREMENT = ', @max_run + 1);
PREPARE stmt_run FROM @sql_run;
EXECUTE stmt_run;
DEALLOCATE PREPARE stmt_run;

-- ---------------------------------------------------------------------------
-- 5. checklist_item_memory → testcase_checklist_item_memory
--    跳过 item_text 超过 2000 字符的行（可在迁移后查 _stg 对比行数）
-- ---------------------------------------------------------------------------
INSERT INTO `testcase_checklist_item_memory` (
  `checklist_fingerprint`, `item_text`, `remembered_value`, `source_task_id`, `updated_at`
)
SELECT
  TRIM(`checklist_fingerprint`),
  LEFT(TRIM(`item_text`), 2000),
  `remembered_value`,
  NULLIF(TRIM(`source_task_id`), ''),
  `qa_fn_iso_to_datetime`(`updated_at`)
FROM `_stg_checklist_item_memory`
WHERE `checklist_fingerprint` IS NOT NULL AND TRIM(`checklist_fingerprint`) <> ''
  AND `item_text` IS NOT NULL AND TRIM(`item_text`) <> ''
  AND CHAR_LENGTH(`item_text`) <= 2000
ON DUPLICATE KEY UPDATE
  `remembered_value` = VALUES(`remembered_value`),
  `source_task_id` = VALUES(`source_task_id`),
  `updated_at` = VALUES(`updated_at`);

-- ---------------------------------------------------------------------------
-- 6. pipeline_config → testcase_pipeline_config
-- ---------------------------------------------------------------------------
INSERT INTO `testcase_pipeline_config` (`id`, `config_json`, `updated_at`)
SELECT
  TRIM(`id`),
  `qa_fn_text_to_json`(`config_json`),
  `qa_fn_iso_to_datetime`(`updated_at`)
FROM `_stg_pipeline_config`
WHERE `id` IS NOT NULL AND TRIM(`id`) <> ''
  AND `config_json` IS NOT NULL AND TRIM(`config_json`) <> ''
ON DUPLICATE KEY UPDATE
  `config_json` = VALUES(`config_json`),
  `updated_at` = VALUES(`updated_at`);

-- ---------------------------------------------------------------------------
-- 迁移结果校验（可选，执行后看 row_count）
-- ---------------------------------------------------------------------------
SELECT 'testcase_tasks' AS tbl, COUNT(*) AS row_count FROM `testcase_tasks`
UNION ALL SELECT 'testcase_task_check_items', COUNT(*) FROM `testcase_task_check_items`
UNION ALL SELECT 'testcase_test_case_library', COUNT(*) FROM `testcase_test_case_library`
UNION ALL SELECT 'testcase_task_agent_runs', COUNT(*) FROM `testcase_task_agent_runs`
UNION ALL SELECT 'testcase_checklist_item_memory', COUNT(*) FROM `testcase_checklist_item_memory`
UNION ALL SELECT 'testcase_pipeline_config', COUNT(*) FROM `testcase_pipeline_config`;

SELECT 'skipped_checklist_memory_long_item_text' AS note, COUNT(*) AS row_count
FROM `_stg_checklist_item_memory`
WHERE `item_text` IS NOT NULL AND CHAR_LENGTH(`item_text`) > 2000;

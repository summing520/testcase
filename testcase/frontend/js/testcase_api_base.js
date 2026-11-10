/**
 * 解析测试用例工作台后端 API 根地址。
 * 优先级：localStorage.testCaseApiBase > URL ?apiBase= > 非本机访问时用当前主机:8000 > 127.0.0.1:8000
 */
(function (global) {
  const DEFAULT_PORT = "8000";

  function resolveTestCaseApiBase() {
    if (typeof localStorage !== "undefined") {
      const stored = localStorage.getItem("testCaseApiBase");
      if (stored && String(stored).trim()) {
        return String(stored).trim().replace(/\/$/, "");
      }
    }
    if (typeof location !== "undefined") {
      const q = new URLSearchParams(location.search).get("apiBase");
      if (q && String(q).trim()) {
        return String(q).trim().replace(/\/$/, "");
      }
      const { protocol, hostname } = location;
      if (hostname && hostname !== "localhost" && hostname !== "127.0.0.1") {
        return `${protocol}//${hostname}:${DEFAULT_PORT}`;
      }
    }
    return `http://127.0.0.1:${DEFAULT_PORT}`;
  }

  global.resolveTestCaseApiBase = resolveTestCaseApiBase;
})(typeof window !== "undefined" ? window : globalThis);

"use strict";
// Local shell only; README animation lives entirely inside the SVG images.
const query = new URLSearchParams(location.search);
const mode = query.get("mode") === "design" ? "design" : "parity";
let theme = query.get("theme") === "light" ? "light" : "dark";
const themeButton = document.querySelector("#theme-toggle");
function applyTheme() {
  document.documentElement.dataset.colorMode = theme;
  themeButton.innerHTML = theme === "dark" ? "☀ <span>Light theme</span>" : "☾ <span>Dark theme</span>";
  themeButton.setAttribute("aria-label", `Switch to ${theme === "dark" ? "light" : "dark"} theme`);
  document.querySelectorAll("#readme source").forEach(source => {
    const original = source.dataset.originalMedia ?? source.getAttribute("media") ?? "";
    source.dataset.originalMedia = original;
    if (mode === "parity") {
      // Observed GitHub themed-picture behavior: entire theme media replaced.
      const selected = original.match(/prefers-color-scheme:\s*(dark|light)/)?.[1];
      source.media = selected ? (selected === theme
        ? "(prefers-color-scheme: light),(prefers-color-scheme: dark)" : "not all") : original;
    } else {
      source.media = original.replace(/\(prefers-color-scheme:\s*(dark|light)\)/g,
        (_, value) => value === theme ? "(min-width: 0px)" : "not all");
    }
  });
  document.querySelectorAll("#readme img").forEach(img => {
    if (img.src.includes("/generated/")) img.src = img.src.replace(/\/generated\/(dark|light)\//, `/generated/${theme}/`);
  });
}
themeButton.addEventListener("click", () => {
  theme = theme === "dark" ? "light" : "dark";
  const url = new URL(location.href); url.searchParams.set("theme", theme);
  history.replaceState(null, "", url); applyTheme();
});
const notice = document.createElement("p");
notice.id = "preview-mode";
notice.style.cssText = "font-size:12px;padding:8px;border-bottom:1px solid var(--border)";
notice.innerHTML = `<strong>${mode === "parity" ? "Production Parity" : "Design Preview"}</strong> | Local only | <a href="?theme=${theme}&mode=${mode === "parity" ? "design" : "parity"}">Switch preview mode</a>`;
document.querySelector("#readme").before(notice);
applyTheme();
fetch("/preview/readme.html", {cache: "no-store"}).then(response => {
  if (!response.ok) throw new Error(`README fragment: HTTP ${response.status}`);
  return response.text();
}).then(markup => {
  const article = document.querySelector("#readme");
  article.innerHTML = markup;
  article.querySelectorAll("[src],[srcset]").forEach(element => {
    for (const attribute of ["src", "srcset"]) {
      const value = element.getAttribute(attribute);
      if (value && /^(?:\.\/|\.\.\/)?generated\//.test(value)) element.setAttribute(attribute, "/" + value.replace(/^(?:\.\/|\.\.\/)/, ""));
    }
  });
  applyTheme(); article.setAttribute("aria-busy", "false");
  window.previewReady = true;
}).catch(error => {
  document.querySelector("#readme").textContent = "Generate the README fragment first: python scripts/build.py";
  document.querySelector("#readme").setAttribute("aria-busy", "false");
  window.previewError = error.message;
});

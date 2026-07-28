window.toggleTheme = function () {
  const html = document.documentElement;
  let targetTheme = "dark";

  if (html.classList.contains("dark")) {
    html.classList.remove("dark");
    html.classList.add("light");
    html.style.colorScheme = "light";
    targetTheme = "light";
  } else {
    html.classList.remove("light");
    html.classList.add("dark");
    html.style.colorScheme = "dark";
    targetTheme = "dark";
  }

  localStorage.setItem("site-theme", targetTheme);
  localStorage.setItem("theme", targetTheme);
  localStorage.setItem("last_compiled_theme", targetTheme);

  if (window.preview) {
    window.preview.applyAll();
  }
};

document.addEventListener("keydown", (e) => {
  if (
    e.target instanceof HTMLInputElement ||
    e.target instanceof HTMLTextAreaElement ||
    e.target.isContentEditable
  ) {
    return;
  }

  if (e.ctrlKey || e.metaKey || e.altKey) {
    return;
  }

  if (e.key.toLowerCase() === "d") {
    e.preventDefault();
    window.toggleTheme();
  }
});

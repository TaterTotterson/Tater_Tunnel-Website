(() => {
  const navToggle = document.querySelector(".nav-toggle");
  const siteNav = document.querySelector(".site-nav");

  if (navToggle && siteNav) {
    navToggle.addEventListener("click", () => {
      const isOpen = siteNav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    document.addEventListener("click", (event) => {
      if (!siteNav.classList.contains("is-open")) {
        return;
      }
      const target = event.target;
      if (target instanceof Node && !siteNav.contains(target) && !navToggle.contains(target)) {
        siteNav.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  const closeNav = (restoreFocus = false) => {
    siteNav?.classList.remove("is-open");
    navToggle?.setAttribute("aria-expanded", "false");
    if (restoreFocus) navToggle?.focus();
  };
  siteNav?.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeNav();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && siteNav?.classList.contains("is-open")) closeNav(true);
  });
  window.matchMedia("(min-width: 761px)").addEventListener("change", () => closeNav());

  document.querySelectorAll("[data-tabs]").forEach((group) => {
    const tabs = Array.from(group.querySelectorAll('[role="tab"]'));
    const panels = tabs.map((tab) => document.getElementById(tab.getAttribute("aria-controls")));
    const select = (index, focus = false) => {
      tabs.forEach((tab, i) => {
        tab.setAttribute("aria-selected", String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
      if (focus) {
        tabs[index].focus();
        tabs[index].scrollIntoView({ block: "nearest", inline: "nearest" });
      }
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener("click", (event) => {
        event.preventDefault(); select(index);
      });
      tab.addEventListener("keydown", (event) => {
        let next = index;
        if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
        else if (event.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === "Home") next = 0;
        else if (event.key === "End") next = tabs.length - 1;
        else if (event.key !== " " && event.key !== "Enter") return;
        event.preventDefault(); select(next, true);
      });
    });
    const hashIndex = panels.findIndex((panel) => `#${panel.id}` === window.location.hash);
    select(hashIndex >= 0 ? hashIndex : 0);
    group.classList.add("tabs-ready");
  });

  const guideSearch = document.querySelector("[data-guide-search]");
  const guides = Array.from(document.querySelectorAll("[data-guide]"));
  guideSearch?.addEventListener("input", () => {
    const words = guideSearch.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    guides.forEach((guide) => {
      const text = `${guide.textContent} ${guide.dataset.keywords || ""}`.toLowerCase();
      guide.hidden = !words.every((word) => text.includes(word));
      if (!guide.hidden) visible++;
    });
    document.querySelector("[data-guide-count]").textContent = `${visible} ${visible === 1 ? "guide" : "guides"}${words.length ? " found." : " to help you get connected."}`;
    document.querySelector("[data-guide-empty]").hidden = visible !== 0;
  });

  document.querySelectorAll("[data-copy-code]").forEach((button) => {
    button.addEventListener("click", async () => {
      const box = button.closest(".command-box");
      const code = box?.querySelector("code")?.textContent || "";
      if (!code.trim()) {
        return;
      }
      try {
        await navigator.clipboard.writeText(code);
        button.textContent = "Copied";
        window.setTimeout(() => {
          button.textContent = "Copy";
        }, 1200);
      } catch {
        button.textContent = "Select";
        const range = document.createRange();
        const selection = window.getSelection();
        const codeElement = box?.querySelector("code");
        if (codeElement && selection) {
          range.selectNodeContents(codeElement);
          selection.removeAllRanges();
          selection.addRange(range);
        }
      }
    });
  });
})();

(() => {
  "use strict";

  document.documentElement.classList.add("has-js");

  document.querySelectorAll("[data-current-year]").forEach((node) => {
    node.textContent = String(new Date().getFullYear());
  });

  const revealNodes = [...document.querySelectorAll("[data-reveal]")];
  if (!("IntersectionObserver" in window)) {
    revealNodes.forEach((node) => node.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -4%", threshold: 0.06 },
  );

  revealNodes.forEach((node) => observer.observe(node));
})();

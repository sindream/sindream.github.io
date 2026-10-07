(() => {
  "use strict";

  document.documentElement.classList.add("has-js");

  const now = new Date();
  document.querySelectorAll("[data-current-year]").forEach((node) => {
    node.textContent = String(now.getFullYear());
  });

  document.querySelectorAll("[data-age][data-birthdate]").forEach((node) => {
    const [year, month, day] = node.dataset.birthdate.split("-").map(Number);
    let age = now.getFullYear() - year;
    const birthdayHasPassed = now.getMonth() + 1 > month || (now.getMonth() + 1 === month && now.getDate() >= day);
    if (!birthdayHasPassed) age -= 1;
    node.textContent = String(age);
  });

  const revealNodes = [...document.querySelectorAll("[data-reveal]")];
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8%", threshold: 0.08 },
    );
    revealNodes.forEach((node, index) => {
      node.style.transitionDelay = `${Math.min(index % 4, 3) * 55}ms`;
      observer.observe(node);
    });
  } else {
    revealNodes.forEach((node) => node.classList.add("is-visible"));
  }

  const canvas = document.querySelector("[data-trajectory-field]");
  if (!canvas) return;

  const context = canvas.getContext("2d", { alpha: true });
  if (!context) return;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let width = 0;
  let height = 0;
  let scale = 1;
  let agents = [];
  let animationFrame = 0;

  const createAgent = (index, count) => {
    const rightBias = index < count * 0.7;
    return {
      x: width * (rightBias ? 0.48 + Math.random() * 0.5 : Math.random()),
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.24,
      vy: (Math.random() - 0.5) * 0.24,
      radius: index % 7 === 0 ? 2.2 : 1.15,
      phase: Math.random() * Math.PI * 2,
    };
  };

  const resize = () => {
    const bounds = canvas.getBoundingClientRect();
    width = Math.max(1, bounds.width);
    height = Math.max(1, bounds.height);
    scale = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * scale);
    canvas.height = Math.round(height * scale);
    context.setTransform(scale, 0, 0, scale, 0, 0);
    const count = width < 720 ? 18 : 36;
    agents = Array.from({ length: count }, (_, index) => createAgent(index, count));
    draw(0, true);
  };

  const drawAgent = (agent, time) => {
    const pulse = 0.65 + Math.sin(time * 0.0013 + agent.phase) * 0.25;
    context.beginPath();
    context.arc(agent.x, agent.y, agent.radius, 0, Math.PI * 2);
    context.fillStyle = `rgba(99, 215, 209, ${pulse})`;
    context.fill();

    if (agent.radius > 2) {
      context.beginPath();
      context.arc(agent.x, agent.y, 9 + pulse * 4, 0, Math.PI * 2);
      context.strokeStyle = `rgba(99, 215, 209, ${0.12 + pulse * 0.1})`;
      context.lineWidth = 1;
      context.stroke();
    }
  };

  const drawConnections = () => {
    const maxDistance = Math.min(170, width * 0.12);
    for (let first = 0; first < agents.length; first += 1) {
      for (let second = first + 1; second < agents.length; second += 1) {
        const dx = agents[first].x - agents[second].x;
        const dy = agents[first].y - agents[second].y;
        const distance = Math.hypot(dx, dy);
        if (distance >= maxDistance) continue;
        context.beginPath();
        context.moveTo(agents[first].x, agents[first].y);
        context.lineTo(agents[second].x, agents[second].y);
        context.strokeStyle = `rgba(99, 215, 209, ${(1 - distance / maxDistance) * 0.16})`;
        context.lineWidth = 0.7;
        context.stroke();
      }
    }
  };

  function draw(time, staticFrame = false) {
    context.clearRect(0, 0, width, height);

    if (!staticFrame) {
      agents.forEach((agent) => {
        agent.x += agent.vx;
        agent.y += agent.vy;
        if (agent.x < -20) agent.x = width + 20;
        if (agent.x > width + 20) agent.x = -20;
        if (agent.y < -20) agent.y = height + 20;
        if (agent.y > height + 20) agent.y = -20;
      });
    }

    drawConnections();
    agents.forEach((agent) => drawAgent(agent, time));

    if (!reducedMotion && !staticFrame) {
      animationFrame = window.requestAnimationFrame((nextTime) => draw(nextTime));
    }
  }

  let resizeTimer = 0;
  window.addEventListener("resize", () => {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(() => {
      window.cancelAnimationFrame(animationFrame);
      resize();
      if (!reducedMotion) animationFrame = window.requestAnimationFrame((time) => draw(time));
    }, 120);
  });

  resize();
  if (!reducedMotion) animationFrame = window.requestAnimationFrame((time) => draw(time));
})();

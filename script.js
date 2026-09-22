document.querySelectorAll("#year").forEach((year) => {
  year.textContent = new Date().getFullYear();
});

const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");
const insuranceDropdown = document.querySelector(".nav-dropdown");
const insuranceTrigger = document.querySelector(".nav-dropdown-trigger");

if (insuranceDropdown && insuranceTrigger) {
  insuranceTrigger.setAttribute("aria-haspopup", "true");
  insuranceTrigger.setAttribute("aria-expanded", "false");

  const closeInsuranceDropdown = () => {
    insuranceDropdown.classList.remove("open");
    insuranceTrigger.setAttribute("aria-expanded", "false");
  };

  insuranceTrigger.addEventListener("click", (event) => {
    if (window.matchMedia("(min-width: 981px)").matches) {
      event.preventDefault();
      const isOpen = insuranceDropdown.classList.toggle("open");
      insuranceTrigger.setAttribute("aria-expanded", String(isOpen));
    }
  });

  document.addEventListener("click", (event) => {
    if (!insuranceDropdown.contains(event.target)) {
      closeInsuranceDropdown();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeInsuranceDropdown();
      insuranceTrigger.blur();
    }
  });
}

if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");
    document.body.classList.toggle("nav-open", isOpen);
    menuToggle.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      if (link.classList.contains("nav-dropdown-trigger")) return;
      navLinks.classList.remove("open");
      document.body.classList.remove("nav-open");
      menuToggle.setAttribute("aria-expanded", "false");
    });
  });
}

const revealTargets = document.querySelectorAll(
  ".section, .stats, .dark-section, .trusted-partners, .cta, .card, .trusted-logo-card, .form, .resource-card, .article-aside, .article-inline-cta, .article-related-bottom, .local-proof"
);

if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.14 }
  );

  revealTargets.forEach((target) => {
    target.classList.add("reveal");
    revealObserver.observe(target);
  });
} else {
  revealTargets.forEach((target) => target.classList.add("in-view"));
}

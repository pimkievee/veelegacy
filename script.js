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
      insuranceTrigger.blur();
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

const quoteIntroVideo = document.querySelector(".quote-intro-video");

if (quoteIntroVideo) {
  quoteIntroVideo.muted = true;

  const allowManualAudio = () => {
    quoteIntroVideo.defaultMuted = false;
    quoteIntroVideo.removeAttribute("muted");
    quoteIntroVideo.muted = true;
  };

  const playPromise = quoteIntroVideo.play();

  if (playPromise && typeof playPromise.then === "function") {
    playPromise.then(allowManualAudio).catch(() => {});
  } else {
    quoteIntroVideo.addEventListener("playing", allowManualAudio, { once: true });
  }
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


// Text content gently slides into view throughout the website.
// Keeping text nodes and markup intact preserves accessibility, links and SEO.
const textSlideElements = document.querySelectorAll(
  [
    "main h1", "main h2", "main h3", "main h4",
    "main p", "main li", "main blockquote",
    "main .eyebrow", "main .stats strong", "main .stats span",
    "main .feature-list > div", "main .card > span",
    "main .quote-info-card > strong",
    ".trusted-partners h2", ".trusted-partners p", ".trusted-logo-card > span",
    ".footer h3", ".footer p", ".footer .footer-links a",
    ".footer .footer-contact > a", ".footer .footer-contact > span",
    ".footer .footer-cta", ".footer-bottom p"
  ].join(", ")
);

const reduceTextMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (!reduceTextMotion && "IntersectionObserver" in window) {
  const textSlideObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("text-in-view");
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -10px 0px", threshold: 0.08 }
  );

  textSlideElements.forEach((element, index) => {
    // Interactive form fields and anything explicitly hidden must remain usable.
    if (element.closest("[hidden], [aria-hidden='true'], .sr-only, .honeypot")) return;

    element.classList.add("text-slide-in");
    element.style.setProperty("--text-slide-delay", `${(index % 3) * 55}ms`);
    textSlideObserver.observe(element);
  });
}

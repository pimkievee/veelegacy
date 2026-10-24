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


// Sitewide discreet question form. The existing email/lead processing service is reused.
(() => {
  if (document.querySelector(".vl-contact")) return;
  const root = document.createElement("aside");
  root.className = "vl-contact";
  root.setAttribute("aria-label", "Contact VeeLegacy");
  root.innerHTML = `
    <div class="vl-contact-teaser" role="status">
      Have a question? I'm here to help you find your next step.
      <button type="button" class="vl-teaser-x" aria-label="Dismiss welcome message">×</button>
    </div>
    <div class="vl-contact-panel" id="veelegacy-contact-panel" aria-label="Ask VeeLegacy a question">
      <div class="vl-contact-panel-header">
        <img src="/assets/profile.jpg" alt="" width="47" height="47" decoding="async">
        <div><strong>Have a question?</strong><small>VeeLegacy · Financial guidance</small></div>
        <button class="vl-contact-close" type="button" aria-label="Close question form">×</button>
      </div>
      <div class="vl-contact-content">
        <p class="vl-contact-intro">Tell me what you're exploring and I'll follow up personally.</p>
        <form class="vl-contact-form" action="https://formspree.io/f/mojblekj" method="POST">
          <input type="hidden" name="formType" value="Website floating question">
          <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
          <label>Your name<input type="text" name="fullName" autocomplete="name" required placeholder="Full name"></label>
          <label>Email address<input type="email" name="email" autocomplete="email" required placeholder="you@example.com"></label>
          <label>How can I help?<textarea name="message" required rows="3" maxlength="1200" placeholder="I'd like to know more about…"></textarea></label>
          <label class="vl-contact-consent"><input type="checkbox" name="consent" required><span>I agree to be contacted about my request and to the <a href="/privacy-policy/">Privacy Policy</a>.</span></label>
          <button class="vl-contact-submit" type="submit">Send my question →</button>
          <p class="vl-contact-status" role="status" aria-live="polite" hidden></p>
          <p class="vl-contact-note">Please don't include sensitive medical, banking or identification details.</p>
        </form>
      </div>
    </div>
    <button type="button" class="vl-contact-launch" aria-controls="veelegacy-contact-panel" aria-expanded="false">
      <img src="/assets/profile.jpg" alt="" width="44" height="44" decoding="async">
      <span>Have a question?</span><span class="vl-launch-dot" aria-hidden="true"></span>
    </button>`;
  document.body.appendChild(root);

  const launcher = root.querySelector(".vl-contact-launch");
  const close = root.querySelector(".vl-contact-close");
  const panel = root.querySelector(".vl-contact-panel");
  const form = root.querySelector(".vl-contact-form");
  const status = root.querySelector(".vl-contact-status");
  const submit = root.querySelector(".vl-contact-submit");
  const hideTeaser = () => {
    root.classList.remove("show-teaser");
    try { sessionStorage.setItem("vl-contact-teaser", "seen"); } catch (_) {}
  };
  const openPanel = () => {
    hideTeaser();
    root.classList.add("is-open");
    launcher.setAttribute("aria-expanded", "true");
    panel.querySelector('input[name="fullName"]').focus();
  };
  const closePanel = () => {
    root.classList.remove("is-open");
    launcher.setAttribute("aria-expanded", "false");
    launcher.focus();
  };
  launcher.addEventListener("click", () => {
    if (root.classList.contains("is-open")) closePanel();
    else openPanel();
  });
  close.addEventListener("click", closePanel);
  root.querySelector(".vl-teaser-x").addEventListener("click", hideTeaser);
  document.querySelectorAll("[data-open-contact-widget]").forEach((button) => {
    button.addEventListener("click", openPanel);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && root.classList.contains("is-open")) closePanel();
  });
  let alreadySeen = false;
  try { alreadySeen = sessionStorage.getItem("vl-contact-teaser") === "seen"; } catch (_) {}
  if (!alreadySeen) {
    window.setTimeout(() => {
      if (!root.classList.contains("is-open")) root.classList.add("show-teaser");
    }, 1700);
  }
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    status.hidden = true;
    submit.disabled = true;
    submit.textContent = "Sending…";
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      });
      if (!response.ok) throw new Error("Unable to send");
      form.reset();
      status.hidden = false;
      status.textContent = "Thank you! Your question has been sent. I'll follow up by email.";
    } catch (_) {
      status.hidden = false;
      status.textContent = "We couldn't send your message. Please email valerie@veelegacy.ca instead.";
    } finally {
      submit.disabled = false;
      submit.textContent = "Send my question →";
    }
  });
})();

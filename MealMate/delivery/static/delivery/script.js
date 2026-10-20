
document.addEventListener("DOMContentLoaded", () => {
  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  // Footer year
  const year = document.getElementById("currentYear");
  if (year) year.textContent = new Date().getFullYear();

  // Toast notifications
  const toast = document.getElementById("toast");
  let toastTimer;

  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 2800);
  }

  // Mobile navigation
  const menuToggle = document.getElementById("menuToggle");
  const navLinks = document.getElementById("navLinks");

  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
      const open = navLinks.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", String(open));
      menuToggle.setAttribute(
        "aria-label",
        open ? "Close navigation" : "Open navigation"
      );
      menuToggle.innerHTML = open
        ? '<i class="fa-solid fa-xmark"></i>'
        : '<i class="fa-solid fa-bars"></i>';
    });

    navLinks.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        navLinks.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
      });
    });

    document.addEventListener("click", event => {
      if (
        navLinks.classList.contains("open") &&
        !navLinks.contains(event.target) &&
        !menuToggle.contains(event.target)
      ) {
        navLinks.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
      }
    });
  }

  // Horizontal category slider
  const categoryTrack = document.getElementById("categoryTrack");

  function moveCategories(direction) {
    if (!categoryTrack) return;

    const item = categoryTrack.querySelector(".category-item");
    const distance = item
      ? (item.getBoundingClientRect().width + 15) * 2
      : 250;

    categoryTrack.scrollBy({
      left: direction * distance,
      behavior: reduceMotion ? "auto" : "smooth"
    });
  }

  document.getElementById("categoryPrev")?.addEventListener(
    "click", () => moveCategories(-1)
  );

  document.getElementById("categoryNext")?.addEventListener(
    "click", () => moveCategories(1)
  );

  // Offer carousel
  const offerTrack = document.getElementById("offerTrack");
  const offerDots = document.getElementById("offerDots");
  const offerPrev = document.getElementById("offerPrev");
  const offerNext = document.getElementById("offerNext");

  const offerCards = offerTrack
    ? Array.from(offerTrack.querySelectorAll(".offer-card"))
    : [];

  let currentOffer = 0;
  let offerTimer;
  let touchStartX = 0;

  function renderDots() {
    if (!offerDots) return;

    offerDots.replaceChildren();

    offerCards.forEach((_, index) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "carousel-dot" +
        (index === currentOffer ? " active" : "");
      dot.setAttribute("aria-label", `Show offer ${index + 1}`);
      dot.setAttribute("aria-current", String(index === currentOffer));

      dot.addEventListener("click", () => {
        showOffer(index);
        restartOfferTimer();
      });

      offerDots.appendChild(dot);
    });
  }

  function showOffer(index) {
    if (!offerCards.length || !offerTrack) return;

    currentOffer = (index + offerCards.length) % offerCards.length;

    const cardWidth = offerCards[0].getBoundingClientRect().width;
    const gap = parseFloat(getComputedStyle(offerTrack).gap) || 0;

    offerTrack.style.transform =
      `translateX(-${currentOffer * (cardWidth + gap)}px)`;

    renderDots();
  }

  function restartOfferTimer() {
    clearInterval(offerTimer);

    if (!reduceMotion && offerCards.length > 1) {
      offerTimer = setInterval(() => {
        showOffer(currentOffer + 1);
      }, 4000);
    }
  }

  offerPrev?.addEventListener("click", () => {
    showOffer(currentOffer - 1);
    restartOfferTimer();
  });

  offerNext?.addEventListener("click", () => {
    showOffer(currentOffer + 1);
    restartOfferTimer();
  });

  offerTrack?.addEventListener("touchstart", event => {
    touchStartX = event.changedTouches[0].clientX;
  }, { passive: true });

  offerTrack?.addEventListener("touchend", event => {
    const difference =
      event.changedTouches[0].clientX - touchStartX;

    if (Math.abs(difference) > 45) {
      showOffer(currentOffer + (difference < 0 ? 1 : -1));
      restartOfferTimer();
    }
  }, { passive: true });

  showOffer(0);
  restartOfferTimer();

  window.addEventListener("resize", () => showOffer(currentOffer));

  // Search restaurants provided by Django.
  const restaurantCards = Array.from(
    document.querySelectorAll(".restaurant-card")
  );

  function searchRestaurants(query) {
    const search = query.trim().toLowerCase();

    if (!search) {
      window.location.href = "/customer-restaurants/";
      return;
    }

    if (!restaurantCards.length) {
      showToast("Please sign in to explore restaurants.");
      return;
    }

    let matches = 0;

    restaurantCards.forEach(card => {
      const searchable = card.dataset.search || "";
      const match = searchable.includes(search);

      card.hidden = !match;
      if (match) matches++;
    });

    let empty = document.getElementById("searchEmpty");

    if (!empty) {
      empty = document.createElement("p");
      empty.id = "searchEmpty";
      empty.className = "empty-state";
      empty.textContent = "No matching restaurants found.";
      document.getElementById("restaurantGrid")?.appendChild(empty);
    }

    empty.hidden = matches > 0;

    document.getElementById("restaurants")?.scrollIntoView({
      behavior: reduceMotion ? "auto" : "smooth"
    });

    if (!matches) showToast("Try another restaurant or cuisine.");
  }

  document.getElementById("heroSearch")?.addEventListener(
    "submit", event => {
      event.preventDefault();
      searchRestaurants(
        document.getElementById("heroSearchInput")?.value || ""
      );
    }
  );

  // Reveal sections when they scroll into view.
  const revealElements = document.querySelectorAll(".reveal");

  if ("IntersectionObserver" in window && !reduceMotion) {
    const observer = new IntersectionObserver((entries, currentObserver) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          currentObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -25px 0px" });

    revealElements.forEach(element => observer.observe(element));
  } else {
    revealElements.forEach(element => element.classList.add("visible"));
  }

  // Button ripple effect
  document.querySelectorAll(".button").forEach(button => {
    button.addEventListener("click", event => {
      if (reduceMotion) return;

      const bounds = button.getBoundingClientRect();
      const size = Math.max(bounds.width, bounds.height);
      const ripple = document.createElement("span");

      ripple.className = "ripple";
      ripple.style.width = `${size}px`;
      ripple.style.height = `${size}px`;
      ripple.style.left =
        `${event.clientX - bounds.left - size / 2}px`;
      ripple.style.top =
        `${event.clientY - bounds.top - size / 2}px`;

      button.appendChild(ripple);
      ripple.addEventListener("animationend", () => ripple.remove(), {
        once: true
      });
    });
  });

  // Newsletter demo. Connect this to a Django view to store subscriptions.
  document.getElementById("newsletterForm")?.addEventListener(
    "submit", event => {
      event.preventDefault();

      const email = document.getElementById("newsletterEmail");
      if (!email || !email.checkValidity()) {
        email?.reportValidity();
        return;
      }

      showToast("Thanks for your interest in MealMate!");
      event.target.reset();
    }
  );

  // Pause automatic offer movement when the tab is hidden.
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      clearInterval(offerTimer);
    } else {
      restartOfferTimer();
    }
  });
});

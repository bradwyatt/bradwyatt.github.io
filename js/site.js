(() => {
  const path = window.location.pathname.replace(/\/+$/, "");
  const links = document.querySelectorAll(".nav-links a[data-path]");
  links.forEach((link) => {
    if (link.dataset.path === path || (link.dataset.path === "/" && path === "")) {
      link.classList.add("active");
    }
  });

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (event) => {
      const target = document.querySelector(anchor.getAttribute("href"));
      if (!target) {
        return;
      }
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  const modal = document.getElementById("video-modal");
  const modalVideo = document.getElementById("modal-video");
  if (modal && modalVideo) {
    const source = modalVideo.querySelector("source");
    const closeModal = () => {
      modal.classList.remove("open");
      modal.setAttribute("aria-hidden", "true");
      modalVideo.pause();
      if (source) {
        source.src = "";
        modalVideo.load();
      }
    };

    document.querySelectorAll("[data-video-src]").forEach((button) => {
      button.addEventListener("click", () => {
        if (!source) {
          return;
        }
        source.src = button.getAttribute("data-video-src");
        modalVideo.load();
        modal.classList.add("open");
        modal.setAttribute("aria-hidden", "false");
      });
    });

    modal.addEventListener("click", (event) => {
      if (event.target === modal) {
        closeModal();
      }
    });

    const closeButton = modal.querySelector(".modal-close");
    if (closeButton) {
      closeButton.addEventListener("click", closeModal);
    }

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && modal.classList.contains("open")) {
        closeModal();
      }
    });
  }

  const lightboxModal = document.getElementById("lightbox-modal");
  const lightboxImage = document.getElementById("lightbox-image");
  if (lightboxModal && lightboxImage) {
    const closeButton = lightboxModal.querySelector(".modal-close");
    const prevButton = lightboxModal.querySelector(".lightbox-prev");
    const nextButton = lightboxModal.querySelector(".lightbox-next");
    const triggers = Array.from(document.querySelectorAll("[data-lightbox-src]"));
    const groups = new Map();
    let currentGroup = [];
    let currentIndex = 0;

    triggers.forEach((trigger) => {
      const groupName = trigger.getAttribute("data-lightbox-group") || "default";
      if (!groups.has(groupName)) {
        groups.set(groupName, []);
      }
      groups.get(groupName).push(trigger);
    });

    const renderImage = () => {
      const activeItem = currentGroup[currentIndex];
      if (!activeItem) {
        return;
      }

      lightboxImage.src = activeItem.getAttribute("data-lightbox-src") || "";
      lightboxImage.alt = activeItem.getAttribute("data-lightbox-alt") || "";

      const showNav = currentGroup.length > 1;
      if (prevButton) {
        prevButton.hidden = !showNav;
      }
      if (nextButton) {
        nextButton.hidden = !showNav;
      }
    };

    const openLightbox = (trigger) => {
      const groupName = trigger.getAttribute("data-lightbox-group") || "default";
      currentGroup = groups.get(groupName) || [trigger];
      currentIndex = Math.max(currentGroup.indexOf(trigger), 0);
      renderImage();
      lightboxModal.classList.add("open");
      lightboxModal.setAttribute("aria-hidden", "false");
    };

    const closeLightbox = () => {
      lightboxModal.classList.remove("open");
      lightboxModal.setAttribute("aria-hidden", "true");
      lightboxImage.src = "";
      lightboxImage.alt = "";
    };

    const stepLightbox = (direction) => {
      if (currentGroup.length < 2) {
        return;
      }
      currentIndex = (currentIndex + direction + currentGroup.length) % currentGroup.length;
      renderImage();
    };

    document.addEventListener("click", (event) => {
      const trigger = event.target.closest("[data-lightbox-src]");
      if (!trigger) {
        return;
      }

      event.preventDefault();
      openLightbox(trigger);
    });

    if (prevButton) {
      prevButton.addEventListener("click", () => stepLightbox(-1));
    }

    if (nextButton) {
      nextButton.addEventListener("click", () => stepLightbox(1));
    }

    if (closeButton) {
      closeButton.addEventListener("click", closeLightbox);
    }

    lightboxModal.addEventListener("click", (event) => {
      if (event.target === lightboxModal) {
        closeLightbox();
      }
    });

    document.addEventListener("keydown", (event) => {
      if (!lightboxModal.classList.contains("open")) {
        return;
      }

      if (event.key === "Escape") {
        closeLightbox();
      } else if (event.key === "ArrowLeft") {
        stepLightbox(-1);
      } else if (event.key === "ArrowRight") {
        stepLightbox(1);
      }
    });
  }
})();

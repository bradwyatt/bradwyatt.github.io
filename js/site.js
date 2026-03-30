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
    const setTrackMode = (mode) => {
      Array.from(modalVideo.textTracks || []).forEach((textTrack) => {
        textTrack.mode = mode;
      });
    };
    const resetTrack = ({ src = "", label = "English", lang = "en", isDefault = false } = {}) => {
      const existingTrack = modalVideo.querySelector("track");
      if (existingTrack) {
        existingTrack.remove();
      }

      const nextTrack = document.createElement("track");
      nextTrack.id = "modal-video-track";
      nextTrack.kind = "subtitles";
      nextTrack.src = src;
      nextTrack.setAttribute("label", label);
      nextTrack.setAttribute("srclang", lang);
      if (isDefault) {
        nextTrack.setAttribute("default", "");
      }
      modalVideo.append(nextTrack);
      return nextTrack;
    };
    const closeModal = () => {
      modal.classList.remove("open");
      modal.setAttribute("aria-hidden", "true");
      modalVideo.pause();
      setTrackMode("disabled");
      if (source) {
        source.src = "";
      }
      resetTrack();
      modalVideo.load();
    };

    document.querySelectorAll("[data-video-src]").forEach((button) => {
      button.addEventListener("click", () => {
        if (!source) {
          return;
        }
        source.src = button.getAttribute("data-video-src");
        const trackSrc = button.getAttribute("data-video-track-src");
        const trackLabel = button.getAttribute("data-video-track-label") || "English";
        const trackLang = button.getAttribute("data-video-track-lang") || "en";
        const activeTrack = resetTrack({
          src: trackSrc || "",
          label: trackLabel,
          lang: trackLang,
          isDefault: Boolean(trackSrc),
        });
        modalVideo.load();
        modalVideo.addEventListener(
          "loadedmetadata",
          () => {
            setTrackMode(activeTrack.src ? "showing" : "disabled");
          },
          { once: true },
        );
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
  const lightboxVideo = document.getElementById("lightbox-video");
  const lightboxVideoSource = document.getElementById("lightbox-video-source");
  if (lightboxModal && lightboxImage && lightboxVideo && lightboxVideoSource) {
    const closeButton = lightboxModal.querySelector(".modal-close");
    const prevButton = lightboxModal.querySelector(".lightbox-prev");
    const nextButton = lightboxModal.querySelector(".lightbox-next");
    const lightboxStage = lightboxModal.querySelector(".lightbox-stage");
    const lightboxFigure = lightboxModal.querySelector(".lightbox-figure");
    const triggers = Array.from(document.querySelectorAll("[data-lightbox-src], [data-lightbox-video-src]"));
    const groups = new Map();
    const groupSources = new Map();
    let currentGroup = [];
    let currentIndex = 0;
    let isZoomed = false;

    triggers.forEach((trigger) => {
      const groupName = trigger.getAttribute("data-lightbox-group") || "default";
      const source =
        trigger.getAttribute("data-lightbox-video-src") || trigger.getAttribute("data-lightbox-src") || "";
      if (!groups.has(groupName)) {
        groups.set(groupName, []);
        groupSources.set(groupName, new Set());
      }
      if (!source || groupSources.get(groupName).has(source)) {
        return;
      }
      groupSources.get(groupName).add(source);
      groups.get(groupName).push(trigger);
    });

    const resetZoom = () => {
      isZoomed = false;
      if (lightboxFigure) {
        lightboxFigure.classList.remove("is-zoomed");
      }
      lightboxImage.classList.remove("is-zoomed");
      lightboxImage.style.width = "";
    };

    const resetVideo = () => {
      lightboxVideo.pause();
      lightboxVideo.hidden = true;
      lightboxVideo.removeAttribute("aria-label");
      lightboxVideoSource.src = "";
      lightboxVideo.load();
    };

    const toggleZoom = () => {
      if (!lightboxImage.src || lightboxImage.hidden) {
        return;
      }

      if (isZoomed) {
        resetZoom();
        return;
      }

      const nextWidth = Math.round(lightboxImage.getBoundingClientRect().width * 1.7);
      if (!nextWidth) {
        return;
      }

      isZoomed = true;
      if (lightboxFigure) {
        lightboxFigure.classList.add("is-zoomed");
        lightboxFigure.scrollTop = 0;
        lightboxFigure.scrollLeft = 0;
      }
      lightboxImage.classList.add("is-zoomed");
      lightboxImage.style.width = `${nextWidth}px`;
    };

    const renderMedia = () => {
      const activeItem = currentGroup[currentIndex];
      if (!activeItem) {
        return;
      }

      resetZoom();
      resetVideo();

      const mediaType = activeItem.getAttribute("data-lightbox-type") || "image";
      const altText = activeItem.getAttribute("data-lightbox-alt") || "";

      if (mediaType === "video") {
        lightboxImage.hidden = true;
        lightboxImage.src = "";
        lightboxImage.alt = "";
        lightboxVideoSource.src = activeItem.getAttribute("data-lightbox-video-src") || "";
        lightboxVideo.hidden = false;
        lightboxVideo.setAttribute("aria-label", altText || "Project video");
        lightboxVideo.load();
      } else {
        lightboxVideo.hidden = true;
        lightboxImage.hidden = false;
        lightboxImage.src = activeItem.getAttribute("data-lightbox-src") || "";
        lightboxImage.alt = altText;
      }

      const showNav = currentGroup.length > 1;
      if (lightboxStage) {
        lightboxStage.classList.toggle("is-single", !showNav);
      }
      if (prevButton) {
        prevButton.hidden = !showNav;
      }
      if (nextButton) {
        nextButton.hidden = !showNav;
      }
    };

    const openLightbox = (trigger) => {
      const groupName = trigger.getAttribute("data-lightbox-group") || "default";
      const triggerSource = trigger.getAttribute("data-lightbox-src") || "";
      currentGroup = groups.get(groupName) || [trigger];
      currentIndex = Math.max(
        currentGroup.findIndex(
          (item) =>
            (item.getAttribute("data-lightbox-video-src") || item.getAttribute("data-lightbox-src") || "") ===
            (trigger.getAttribute("data-lightbox-video-src") || triggerSource)
        ),
        0
      );
      renderMedia();
      lightboxModal.classList.add("open");
      lightboxModal.setAttribute("aria-hidden", "false");
      (closeButton || lightboxModal).focus();
    };

    const closeLightbox = () => {
      resetZoom();
      resetVideo();
      lightboxModal.classList.remove("open");
      lightboxModal.setAttribute("aria-hidden", "true");
      lightboxImage.hidden = false;
      lightboxImage.src = "";
      lightboxImage.alt = "";
    };

    const stepLightbox = (direction) => {
      if (currentGroup.length < 2) {
        return;
      }
      currentIndex = (currentIndex + direction + currentGroup.length) % currentGroup.length;
      renderMedia();
    };

    document.addEventListener("click", (event) => {
      const trigger = event.target.closest("[data-lightbox-src], [data-lightbox-video-src]");
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

    lightboxImage.addEventListener("click", toggleZoom);

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
        event.preventDefault();
        closeLightbox();
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        stepLightbox(-1);
      } else if (event.key === "ArrowRight") {
        event.preventDefault();
        stepLightbox(1);
      }
    });
  }
})();

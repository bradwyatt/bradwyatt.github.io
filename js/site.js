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
  let modalVideo = document.getElementById("modal-video");
  if (modal && modalVideo) {
    let source = modalVideo.querySelector("source");
    const rebuildModalVideo = () => {
      const nextVideo = modalVideo.cloneNode(true);
      nextVideo.querySelectorAll("track").forEach((track) => track.remove());
      nextVideo.removeAttribute("src");

      const nextSource = nextVideo.querySelector("source");
      if (nextSource) {
        nextSource.removeAttribute("src");
      }

      modalVideo.replaceWith(nextVideo);
      modalVideo = nextVideo;
      source = nextSource;
    };
    const resetTrack = ({ src = "", label = "English", lang = "en", isDefault = false } = {}) => {
      Array.from(modalVideo.textTracks || []).forEach((textTrack) => {
        textTrack.mode = "disabled";
      });
      modalVideo.querySelectorAll("track").forEach((track) => track.remove());
      if (!src) {
        return false;
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
      return true;
    };
    const closeModal = () => {
      modal.classList.remove("open");
      modal.setAttribute("aria-hidden", "true");
      modalVideo.pause();
      Array.from(modalVideo.textTracks || []).forEach((textTrack) => {
        textTrack.mode = "disabled";
      });
      rebuildModalVideo();
    };

    document.querySelectorAll("[data-video-src]").forEach((button) => {
      button.addEventListener("click", () => {
        modalVideo.pause();
        rebuildModalVideo();
        if (!source) {
          return;
        }

        source.src = button.getAttribute("data-video-src");
        const trackSrc = button.getAttribute("data-video-track-src");
        const trackLabel = button.getAttribute("data-video-track-label") || "English";
        const trackLang = button.getAttribute("data-video-track-lang") || "en";
        const hasTrack = resetTrack({
          src: trackSrc || "",
          label: trackLabel,
          lang: trackLang,
          isDefault: Boolean(trackSrc),
        });
        modalVideo.load();
        modalVideo.addEventListener(
          "loadedmetadata",
          () => {
            const textTracks = Array.from(modalVideo.textTracks || []);
            textTracks.forEach((textTrack) => {
              textTrack.mode = "disabled";
            });
            if (hasTrack) {
              const activeTrack = textTracks.find((textTrack) => textTrack.language === trackLang) || textTracks[0];
              if (activeTrack) {
                activeTrack.mode = "showing";
              }
            }
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
    const getFullscreenElement = () =>
      document.fullscreenElement || document.webkitFullscreenElement || document.msFullscreenElement || null;
    const closeButton = lightboxModal.querySelector(".modal-close");
    const prevButton = lightboxModal.querySelector(".lightbox-prev");
    const nextButton = lightboxModal.querySelector(".lightbox-next");
    const lightboxStage = lightboxModal.querySelector(".lightbox-stage");
    const lightboxFigure = lightboxModal.querySelector(".lightbox-figure");
    const lightboxPanel = lightboxModal.querySelector(".lightbox-panel");
    const lightboxScrollHint = document.getElementById("lightbox-scroll-hint");
    const lightboxTallHeader = document.getElementById("lightbox-tall-header");
    const lightboxTallLabel = document.getElementById("lightbox-tall-label");
    const lightboxTallClose = lightboxModal.querySelector(".lightbox-tall-close");
    let scrollHintTimeout = null;
    let isPositioningTallMedia = false;
    const dismissScrollHint = () => {
      if (!lightboxScrollHint) {
        return;
      }

      clearScrollHintTimeout();
      lightboxScrollHint.classList.add("is-dismissed");
    };
    const clearScrollHintTimeout = () => {
      if (scrollHintTimeout) {
        window.clearTimeout(scrollHintTimeout);
        scrollHintTimeout = null;
      }
    };
    const scheduleScrollHint = () => {
      if (!lightboxScrollHint) {
        return;
      }

      clearScrollHintTimeout();
      const activeItem = currentGroup[currentIndex];
      const shouldShowHint =
        currentMode === "tall" &&
        currentMediaType === "image" &&
        activeItem &&
        activeItem.getAttribute("data-lightbox-scroll-hint") === "concert-curator-first";
      lightboxScrollHint.hidden = !shouldShowHint;
      if (shouldShowHint) {
        lightboxScrollHint.classList.remove("is-dismissed");
      }
    };
    const dismissScrollHintOnInteraction = () => {
      if (!lightboxFigure || currentMode !== "tall" || isPositioningTallMedia) {
        return;
      }

      const isAtBottom =
        lightboxFigure.scrollTop + lightboxFigure.clientHeight >= lightboxFigure.scrollHeight - 2;

      if (lightboxFigure.scrollTop > 0 || isAtBottom) {
        dismissScrollHint();
      }
    };

    const syncVVTop = () => {
      const offset = window.visualViewport ? Math.round(window.visualViewport.offsetTop) : 0;
      lightboxModal.style.setProperty("--lightbox-vv-top", `${offset}px`);
    };
    const onVVChange = () => syncVVTop();
    const triggers = Array.from(document.querySelectorAll("[data-lightbox-src], [data-lightbox-video-src]"));
    const groups = new Map();
    const groupSources = new Map();
    let currentGroup = [];
    let currentIndex = 0;
    let isZoomed = false;
    let currentMode = "standard";
    let currentMediaType = "image";

    const isMobileMediaViewport = () => {
      if (window.matchMedia("(max-width: 900px)").matches) {
        return true;
      }

      return window.matchMedia("(hover: none), (pointer: coarse)").matches;
    };

    const requestElementFullscreen = (element) => {
      if (!element) {
        return Promise.resolve(false);
      }

      const requestFullscreen =
        element.requestFullscreen ||
        element.webkitRequestFullscreen ||
        element.msRequestFullscreen ||
        null;

      if (!requestFullscreen) {
        return Promise.resolve(false);
      }

      try {
        const result = requestFullscreen.call(element);
        if (result && typeof result.then === "function") {
          return result.then(() => true).catch(() => false);
        }
        return Promise.resolve(true);
      } catch {
        return Promise.resolve(false);
      }
    };

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
        lightboxFigure.scrollTop = 0;
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

    const positionTallMedia = () => {
      if (!lightboxFigure || currentMode !== "tall") {
        return;
      }

      isPositioningTallMedia = true;
      lightboxFigure.scrollTop = 0;

      if (currentMediaType === "image") {
        const maxScrollLeft = Math.max(lightboxFigure.scrollWidth - lightboxFigure.clientWidth, 0);
        lightboxFigure.scrollLeft = maxScrollLeft > 0 ? Math.round(maxScrollLeft / 2) : 0;
        if (lightboxScrollHint && lightboxFigure.scrollHeight <= lightboxFigure.clientHeight) {
          dismissScrollHint();
        }
        requestAnimationFrame(() => {
          isPositioningTallMedia = false;
        });
        return;
      }

      lightboxFigure.scrollLeft = 0;
      requestAnimationFrame(() => {
        isPositioningTallMedia = false;
      });
    };

    const toggleZoom = () => {
      if (!lightboxImage.src || lightboxImage.hidden || currentMode === "tall") {
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

      currentMode = activeItem.getAttribute("data-lightbox-mode") === "tall" ? "tall" : "standard";
      currentMediaType = activeItem.getAttribute("data-lightbox-type") || "image";
      lightboxModal.classList.toggle("mode-tall", currentMode === "tall");
      lightboxModal.classList.toggle("mode-standard", currentMode !== "tall");
      lightboxModal.classList.toggle("has-tall-image", currentMode === "tall" && currentMediaType === "image");
      lightboxModal.classList.toggle("has-tall-video", currentMode === "tall" && currentMediaType === "video");
      if (lightboxPanel) {
        lightboxPanel.classList.toggle("mode-tall", currentMode === "tall");
        lightboxPanel.classList.toggle("mode-standard", currentMode !== "tall");
        lightboxPanel.classList.toggle("has-tall-image", currentMode === "tall" && currentMediaType === "image");
        lightboxPanel.classList.toggle("has-tall-video", currentMode === "tall" && currentMediaType === "video");
      }
      if (lightboxFigure) {
        lightboxFigure.classList.toggle("mode-tall", currentMode === "tall");
        lightboxFigure.classList.toggle("has-tall-image", currentMode === "tall" && currentMediaType === "image");
        lightboxFigure.classList.toggle("has-tall-video", currentMode === "tall" && currentMediaType === "video");
      }
      if (lightboxScrollHint) {
        scheduleScrollHint();
        const isEligible =
          currentMode === "tall" &&
          currentMediaType === "image" &&
          activeItem &&
          activeItem.getAttribute("data-lightbox-scroll-hint") === "concert-curator-first";
        lightboxScrollHint.hidden = !isEligible;
        if (isEligible) {
          lightboxScrollHint.classList.remove("is-dismissed");
        }
      }
      if (lightboxTallHeader) {
        lightboxTallHeader.hidden = currentMode !== "tall";
      }
      if (lightboxTallLabel) {
        lightboxTallLabel.textContent = activeItem.getAttribute("data-lightbox-label") || "";
      }

      const mediaType = currentMediaType;
      const altText = activeItem.getAttribute("data-lightbox-alt") || "";

      if (mediaType === "video") {
        lightboxImage.hidden = true;
        lightboxImage.src = "";
        lightboxImage.alt = "";
        lightboxVideoSource.src = activeItem.getAttribute("data-lightbox-video-src") || "";
        lightboxVideo.hidden = false;
        lightboxVideo.setAttribute("aria-label", altText || "Project video");
        lightboxVideo.load();
        requestAnimationFrame(positionTallMedia);
        lightboxVideo.play().catch(() => {});
      } else {
        lightboxVideo.hidden = true;
        lightboxImage.hidden = false;
        lightboxImage.src = activeItem.getAttribute("data-lightbox-src") || "";
        lightboxImage.alt = altText;
        if (lightboxImage.complete) {
          requestAnimationFrame(positionTallMedia);
        } else {
          lightboxImage.addEventListener("load", positionTallMedia, { once: true });
        }
      }

      const showNav = currentGroup.length > 1 && currentMode !== "tall";
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
      if (currentMode === "tall" && window.visualViewport) {
        syncVVTop();
        window.visualViewport.addEventListener("resize", onVVChange);
        window.visualViewport.addEventListener("scroll", onVVChange);
      }
      const focusTarget = currentMode === "tall" ? (lightboxTallClose || lightboxModal) : (closeButton || lightboxModal);
      focusTarget.focus();
    };

    const closeLightbox = () => {
      resetZoom();
      resetVideo();
      lightboxModal.classList.remove("open");
      lightboxModal.classList.remove("mode-tall", "mode-standard", "has-tall-image", "has-tall-video");
      lightboxModal.setAttribute("aria-hidden", "true");
      lightboxImage.hidden = false;
      lightboxImage.src = "";
      lightboxImage.alt = "";
      currentMode = "standard";
      currentMediaType = "image";
      if (lightboxPanel) {
        lightboxPanel.classList.remove("mode-tall", "mode-standard", "has-tall-image", "has-tall-video");
      }
      if (lightboxFigure) {
        lightboxFigure.classList.remove("mode-tall", "has-tall-image", "has-tall-video");
      }
      if (lightboxScrollHint) {
        clearScrollHintTimeout();
        lightboxScrollHint.hidden = true;
        lightboxScrollHint.classList.remove("is-dismissed");
      }
      if (lightboxTallHeader) {
        lightboxTallHeader.hidden = true;
      }
      lightboxModal.style.removeProperty("--lightbox-vv-top");
      if (window.visualViewport) {
        window.visualViewport.removeEventListener("resize", onVVChange);
        window.visualViewport.removeEventListener("scroll", onVVChange);
      }
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

    lightboxImage.addEventListener("click", () => {
      if (!lightboxImage.src || lightboxImage.hidden) {
        return;
      }

      if (isMobileMediaViewport() && !getFullscreenElement()) {
        requestElementFullscreen(lightboxImage).then((didEnterFullscreen) => {
          if (!didEnterFullscreen && currentMode !== "tall") {
            toggleZoom();
          }
        });
        return;
      }

      toggleZoom();
    });

    if (closeButton) {
      closeButton.addEventListener("click", closeLightbox);
    }

    if (lightboxTallClose) {
      lightboxTallClose.addEventListener("click", closeLightbox);
    }

    lightboxModal.addEventListener("click", (event) => {
      if (event.target === lightboxModal) {
        closeLightbox();
      }
    });

    if (lightboxFigure) {
      lightboxFigure.addEventListener("scroll", dismissScrollHintOnInteraction, { passive: true });
      lightboxFigure.addEventListener("touchmove", dismissScrollHintOnInteraction, { passive: true });
      lightboxFigure.addEventListener("wheel", dismissScrollHintOnInteraction, { passive: true });
    }

    document.addEventListener("keydown", (event) => {
      if (!lightboxModal.classList.contains("open")) {
        return;
      }

      if (event.key === "Escape") {
        event.preventDefault();
        closeLightbox();
      } else if (event.key === "ArrowLeft") {
        if (currentMode !== "tall") {
          event.preventDefault();
          stepLightbox(-1);
        }
      } else if (event.key === "ArrowRight") {
        if (currentMode !== "tall") {
          event.preventDefault();
          stepLightbox(1);
        }
      }
    });
  }
})();

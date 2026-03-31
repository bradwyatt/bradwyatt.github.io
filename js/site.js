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
  const lightboxImageZoomContainer = document.getElementById("lightbox-image-zoom-container");
  const lightboxVideo = document.getElementById("lightbox-video");
  const lightboxVideoSource = document.getElementById("lightbox-video-source");
  if (lightboxModal && lightboxImage && lightboxImageZoomContainer && lightboxVideo && lightboxVideoSource) {
    const closeButton = lightboxModal.querySelector(".modal-close");
    const prevButton = lightboxModal.querySelector(".lightbox-prev");
    const nextButton = lightboxModal.querySelector(".lightbox-next");
    const lightboxStage = lightboxModal.querySelector(".lightbox-stage");
    const lightboxFigure = lightboxModal.querySelector(".lightbox-figure");
    const lightboxPanel = lightboxModal.querySelector(".lightbox-panel");
    const lightboxScrollHint = document.getElementById("lightbox-scroll-hint");
    const lightboxTallHeader = document.getElementById("lightbox-tall-header");
    const lightboxTallLabel = document.getElementById("lightbox-tall-label");
    const lightboxTallCounter = document.getElementById("lightbox-tall-counter");
    const lightboxTallClose = lightboxModal.querySelector(".lightbox-tall-close");
    const lightboxTallNav = document.getElementById("lightbox-tall-nav");
    let isPositioningTallMedia = false;
    let scrollHintTimeoutId = 0;

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
    let mobileZoomScale = 1;
    let mobileZoomTranslateX = 0;
    let mobileZoomTranslateY = 0;
    let pinchStartDistance = 0;
    let pinchStartScale = 1;
    let pinchContentX = 0;
    let pinchContentY = 0;
    let panStartX = 0;
    let panStartY = 0;
    let panStartTranslateX = 0;
    let panStartTranslateY = 0;

    const isMobileMediaViewport = () => {
      if (window.matchMedia("(max-width: 900px)").matches) {
        return true;
      }

      return window.matchMedia("(hover: none), (pointer: coarse)").matches;
    };

    const isDesktopTallViewport = () => !isMobileMediaViewport();

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
        lightboxFigure.scrollLeft = 0;
      }
      lightboxImage.classList.remove("is-zoomed");
      lightboxImage.style.width = "";
      mobileZoomScale = 1;
      mobileZoomTranslateX = 0;
      mobileZoomTranslateY = 0;
      pinchStartDistance = 0;
      pinchStartScale = 1;
      pinchContentX = 0;
      pinchContentY = 0;
      panStartX = 0;
      panStartY = 0;
      panStartTranslateX = 0;
      panStartTranslateY = 0;
      lightboxImage.style.transform = "";
      lightboxImage.style.transformOrigin = "";
      lightboxImage.style.willChange = "";
      lightboxImage.classList.remove("is-mobile-zoomed");
      lightboxImageZoomContainer.classList.remove("is-mobile-zoom-active");
      lightboxImageZoomContainer.classList.remove("is-mobile-pinching");
    };

    const resetVideo = () => {
      lightboxVideo.pause();
      lightboxVideo.hidden = true;
      lightboxVideo.removeAttribute("aria-label");
      lightboxVideoSource.src = "";
      lightboxVideo.load();
    };

    const clearScrollHintTimeout = () => {
      if (!scrollHintTimeoutId) {
        return;
      }

      window.clearTimeout(scrollHintTimeoutId);
      scrollHintTimeoutId = 0;
    };

    const dismissScrollHint = () => {
      if (!lightboxScrollHint || lightboxScrollHint.hidden || lightboxScrollHint.classList.contains("is-dismissed")) {
        return;
      }

      clearScrollHintTimeout();
      lightboxScrollHint.classList.add("is-dismissed");
      scrollHintTimeoutId = window.setTimeout(() => {
        lightboxScrollHint.hidden = true;
        lightboxScrollHint.classList.remove("is-dismissed");
        scrollHintTimeoutId = 0;
      }, 180);
    };

    const shouldShowScrollHint = () => {
      const activeItem = currentGroup[currentIndex];
      if (!activeItem || !lightboxFigure) {
        return false;
      }

      const groupName = activeItem.getAttribute("data-lightbox-group") || "";
      const itemLabel = activeItem.getAttribute("data-lightbox-label") || "";
      const shouldHintItem = itemLabel === "Workflow" || itemLabel === "Behavior Spec";
      return (
        groupName === "concert-curator" &&
        shouldHintItem &&
        currentMode === "tall" &&
        currentMediaType === "image" &&
        lightboxFigure.scrollHeight - lightboxFigure.clientHeight > 24
      );
    };

    const syncScrollHint = () => {
      if (!lightboxScrollHint) {
        return;
      }

      clearScrollHintTimeout();
      lightboxScrollHint.classList.remove("is-dismissed");
      lightboxScrollHint.hidden = !shouldShowScrollHint();
    };

    const isNearFigureBottom = () => {
      if (!lightboxFigure) {
        return false;
      }

      return lightboxFigure.scrollTop + lightboxFigure.clientHeight >= lightboxFigure.scrollHeight - 96;
    };

    const positionTallMedia = () => {
      if (!lightboxFigure || currentMode !== "tall") {
        return;
      }

      isPositioningTallMedia = true;

      if (currentMediaType === "image") {
        const maxScrollTop = Math.max(lightboxFigure.scrollHeight - lightboxFigure.clientHeight, 0);
        const maxScrollLeft = Math.max(lightboxFigure.scrollWidth - lightboxFigure.clientWidth, 0);
        const shouldCenterTallMobileImage = lightboxFigure.classList.contains("mode-tall-mobile-centered");
        lightboxFigure.scrollTop = shouldCenterTallMobileImage ? Math.round(maxScrollTop / 2) : 0;
        lightboxFigure.scrollLeft = maxScrollLeft > 0 ? Math.round(maxScrollLeft / 2) : 0;
        requestAnimationFrame(() => {
          isPositioningTallMedia = false;
          syncScrollHint();
        });
        return;
      }

      lightboxFigure.scrollTop = 0;
      lightboxFigure.scrollLeft = 0;
      requestAnimationFrame(() => {
        isPositioningTallMedia = false;
        syncScrollHint();
      });
    };

    const toggleZoom = (event) => {
      if (!lightboxImage.src || lightboxImage.hidden) {
        return;
      }

      if (isZoomed) {
        resetZoom();
        return;
      }

      const imageRect = lightboxImage.getBoundingClientRect();
      const renderedWidth = imageRect.width;
      const naturalWidth = lightboxImage.naturalWidth || renderedWidth;
      const nextWidth = Math.round(
        Math.min(Math.max(naturalWidth, renderedWidth * 1.75), Math.max(renderedWidth * 2.4, 1800))
      );
      if (!nextWidth) {
        return;
      }

      isZoomed = true;
      if (lightboxFigure) {
        lightboxFigure.classList.add("is-zoomed");
      }
      lightboxImage.classList.add("is-zoomed");
      lightboxImage.style.width = `${nextWidth}px`;
      requestAnimationFrame(() => {
        if (!lightboxFigure || !event) {
          return;
        }

        const zoomedRect = lightboxImage.getBoundingClientRect();
        const pointerX = event.clientX - imageRect.left;
        const pointerY = event.clientY - imageRect.top;
        const xRatio = imageRect.width ? pointerX / imageRect.width : 0.5;
        const yRatio = imageRect.height ? pointerY / imageRect.height : 0.5;
        const targetLeft = Math.max(zoomedRect.width * xRatio - lightboxFigure.clientWidth / 2, 0);
        const targetTop = Math.max(zoomedRect.height * yRatio - lightboxFigure.clientHeight / 2, 0);

        lightboxFigure.scrollLeft = targetLeft;
        lightboxFigure.scrollTop = targetTop;
      });
    };

    const isMobileGestureZoomEnabled = (item = currentGroup[currentIndex]) =>
      currentMediaType === "image" && isZoomEnabledForItem(item) && isMobileMediaViewport();

    const getTouchDistance = (touchA, touchB) => Math.hypot(touchB.clientX - touchA.clientX, touchB.clientY - touchA.clientY);

    const getTouchMidpoint = (touchA, touchB) => ({
      x: (touchA.clientX + touchB.clientX) / 2,
      y: (touchA.clientY + touchB.clientY) / 2,
    });

    const getPointWithinZoomContainer = (clientX, clientY) => {
      const rect = lightboxImageZoomContainer.getBoundingClientRect();
      return {
        x: clientX - rect.left,
        y: clientY - rect.top,
      };
    };

    const clampMobileTranslation = (nextScale = mobileZoomScale, nextX = mobileZoomTranslateX, nextY = mobileZoomTranslateY) => {
      const containerWidth = lightboxImageZoomContainer.clientWidth;
      const containerHeight = lightboxImageZoomContainer.clientHeight;
      const imageWidth = lightboxImage.offsetWidth;
      const imageHeight = lightboxImage.offsetHeight;
      const maxX = Math.max((imageWidth * nextScale - containerWidth) / 2, 0);
      const maxY = Math.max((imageHeight * nextScale - containerHeight) / 2, 0);

      return {
        x: Math.min(Math.max(nextX, -maxX), maxX),
        y: Math.min(Math.max(nextY, -maxY), maxY),
      };
    };

    const applyMobileImageTransform = () => {
      const clamped = clampMobileTranslation();
      mobileZoomTranslateX = clamped.x;
      mobileZoomTranslateY = clamped.y;

      if (mobileZoomScale <= 1.001) {
        mobileZoomScale = 1;
        mobileZoomTranslateX = 0;
        mobileZoomTranslateY = 0;
        lightboxImage.style.transform = "";
        lightboxImage.style.transformOrigin = "";
        lightboxImage.style.willChange = "";
        lightboxImage.classList.remove("is-mobile-zoomed");
        lightboxImageZoomContainer.classList.remove("is-mobile-zoom-active");
        return;
      }

      lightboxImage.style.transformOrigin = "center center";
      lightboxImage.style.willChange = "transform";
      lightboxImage.style.transform = `translate3d(${mobileZoomTranslateX}px, ${mobileZoomTranslateY}px, 0) scale(${mobileZoomScale})`;
      lightboxImage.classList.add("is-mobile-zoomed");
      lightboxImageZoomContainer.classList.add("is-mobile-zoom-active");
    };

    window.addEventListener("resize", () => {
      if (!lightboxModal.classList.contains("open") || mobileZoomScale <= 1.001) {
        return;
      }

      applyMobileImageTransform();
    });

    const renderTallNav = () => {
      if (!lightboxTallNav) {
        return;
      }

      const shouldShowTallNav = currentGroup.length > 1;
      lightboxTallNav.hidden = !shouldShowTallNav;
      lightboxTallNav.replaceChildren();

      if (!shouldShowTallNav) {
        return;
      }

      currentGroup.forEach((item, index) => {
        const navButton = document.createElement("button");
        navButton.type = "button";
        navButton.className = "lightbox-tall-nav-button";
        navButton.textContent = item.getAttribute("data-lightbox-label") || `Item ${index + 1}`;
        navButton.setAttribute("aria-label", `Show ${navButton.textContent}`);
        navButton.setAttribute("aria-pressed", index === currentIndex ? "true" : "false");

        if (index === currentIndex) {
          navButton.classList.add("is-active");
        }

        navButton.addEventListener("click", () => {
          if (currentIndex === index) {
            return;
          }

          currentIndex = index;
          renderMedia();
        });

        lightboxTallNav.append(navButton);
      });

      const activeNavButton = lightboxTallNav.querySelector(".lightbox-tall-nav-button.is-active");
      if (activeNavButton) {
        activeNavButton.scrollIntoView({
          behavior: "smooth",
          block: "nearest",
          inline: "nearest",
        });
      }
    };

    const getLightboxLabel = (item) => {
      const explicitLabel = item.getAttribute("data-lightbox-label");
      if (explicitLabel) {
        return explicitLabel;
      }

      const projectHeading = item.closest("article")?.querySelector("h3")?.textContent?.trim();
      if (projectHeading) {
        return projectHeading;
      }

      return item.getAttribute("data-lightbox-alt") || "";
    };

    const isZoomEnabledForItem = (item) => {
      if (!item) {
        return false;
      }

      return item.getAttribute("data-lightbox-zoom") !== "false";
    };

    const renderMedia = () => {
      const activeItem = currentGroup[currentIndex];
      if (!activeItem) {
        return;
      }

      resetZoom();
      resetVideo();

      currentMediaType = activeItem.getAttribute("data-lightbox-type") || "image";
      const prefersTallMode = activeItem.getAttribute("data-lightbox-mode") === "tall";
      const useImmersiveMobileImageLayout = currentMediaType === "image" && isMobileMediaViewport();
      currentMode = prefersTallMode || useImmersiveMobileImageLayout ? "tall" : "standard";
      const activeLabel = getLightboxLabel(activeItem);
      const useDesktopTallLayout = prefersTallMode && currentMode === "tall" && isDesktopTallViewport();
      const useCenteredMobileImmersiveLayout = currentMode === "tall" && useImmersiveMobileImageLayout && !prefersTallMode;
      const useContainedTallImage =
        currentMode === "tall" && currentMediaType === "image" && activeLabel === "Playlist Sample";
      const isZoomEnabled = currentMediaType === "image" && isZoomEnabledForItem(activeItem);
      const isMobileGestureZoomActive = isZoomEnabled && isMobileMediaViewport();
      lightboxModal.classList.toggle("mode-tall", currentMode === "tall");
      lightboxModal.classList.toggle("mode-standard", currentMode !== "tall");
      lightboxModal.classList.toggle("mode-tall-desktop", useDesktopTallLayout);
      lightboxModal.classList.toggle("mode-tall-mobile-centered", useCenteredMobileImmersiveLayout);
      lightboxModal.classList.toggle("has-contained-tall-image", useContainedTallImage);
      lightboxModal.classList.toggle("has-tall-image", currentMode === "tall" && currentMediaType === "image");
      lightboxModal.classList.toggle("has-tall-video", currentMode === "tall" && currentMediaType === "video");
      lightboxModal.classList.toggle("zoom-disabled", !isZoomEnabled);
      lightboxModal.classList.toggle("mobile-gesture-zoom", isMobileGestureZoomActive);
      if (lightboxPanel) {
        lightboxPanel.classList.toggle("mode-tall", currentMode === "tall");
        lightboxPanel.classList.toggle("mode-standard", currentMode !== "tall");
        lightboxPanel.classList.toggle("mode-tall-desktop", useDesktopTallLayout);
        lightboxPanel.classList.toggle("mode-tall-mobile-centered", useCenteredMobileImmersiveLayout);
        lightboxPanel.classList.toggle("has-contained-tall-image", useContainedTallImage);
        lightboxPanel.classList.toggle("has-tall-image", currentMode === "tall" && currentMediaType === "image");
        lightboxPanel.classList.toggle("has-tall-video", currentMode === "tall" && currentMediaType === "video");
        lightboxPanel.classList.toggle("zoom-disabled", !isZoomEnabled);
        lightboxPanel.classList.toggle("mobile-gesture-zoom", isMobileGestureZoomActive);
      }
      if (lightboxFigure) {
        lightboxFigure.classList.toggle("mode-tall", currentMode === "tall");
        lightboxFigure.classList.toggle("mode-tall-desktop", useDesktopTallLayout);
        lightboxFigure.classList.toggle("mode-tall-mobile-centered", useCenteredMobileImmersiveLayout);
        lightboxFigure.classList.toggle("is-contained-tall-image", useContainedTallImage);
        lightboxFigure.classList.toggle("has-tall-image", currentMode === "tall" && currentMediaType === "image");
        lightboxFigure.classList.toggle("has-tall-video", currentMode === "tall" && currentMediaType === "video");
        lightboxFigure.classList.toggle("zoom-disabled", !isZoomEnabled);
        lightboxFigure.classList.toggle("mobile-gesture-zoom", isMobileGestureZoomActive);
      }
      lightboxImageZoomContainer.classList.toggle("mobile-gesture-zoom", isMobileGestureZoomActive);
      const shouldShowTallHeader = currentMode === "tall" && (Boolean(activeLabel) || currentGroup.length > 1);
      if (lightboxTallHeader) {
        lightboxTallHeader.hidden = !shouldShowTallHeader;
      }
      if (lightboxTallLabel) {
        lightboxTallLabel.textContent = activeLabel;
        lightboxTallLabel.hidden = !activeLabel;
      }
      if (lightboxTallCounter) {
        const showCounter = currentMode === "tall" && currentGroup.length > 1;
        lightboxTallCounter.hidden = !showCounter;
        lightboxTallCounter.textContent = showCounter ? `${currentIndex + 1} / ${currentGroup.length}` : "";
      }

      const mediaType = currentMediaType;
      const altText = activeItem.getAttribute("data-lightbox-alt") || "";

      if (mediaType === "video") {
        lightboxImageZoomContainer.hidden = true;
        lightboxImage.hidden = true;
        lightboxImage.src = "";
        lightboxImage.alt = "";
        lightboxVideoSource.src = activeItem.getAttribute("data-lightbox-video-src") || "";
        lightboxVideo.hidden = false;
        lightboxVideo.setAttribute("aria-label", altText || "Project video");
        lightboxVideo.load();
        syncScrollHint();
        requestAnimationFrame(positionTallMedia);
        lightboxVideo.play().catch(() => {});
      } else {
        lightboxImageZoomContainer.hidden = false;
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

      renderTallNav();

      const showNav = currentGroup.length > 1 && (currentMode !== "tall" || useDesktopTallLayout);
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
      lightboxModal.classList.remove(
        "mode-tall",
        "mode-standard",
        "mode-tall-desktop",
        "mode-tall-mobile-centered",
        "zoom-disabled",
        "mobile-gesture-zoom",
        "has-contained-tall-image",
        "has-tall-image",
        "has-tall-video"
      );
      lightboxModal.setAttribute("aria-hidden", "true");
      lightboxImage.hidden = false;
      lightboxImageZoomContainer.hidden = false;
      lightboxImage.src = "";
      lightboxImage.alt = "";
      currentMode = "standard";
      currentMediaType = "image";
      if (lightboxPanel) {
        lightboxPanel.classList.remove(
          "mode-tall",
          "mode-standard",
          "mode-tall-desktop",
          "mode-tall-mobile-centered",
          "zoom-disabled",
          "mobile-gesture-zoom",
          "has-contained-tall-image",
          "has-tall-image",
          "has-tall-video"
        );
      }
      if (lightboxFigure) {
        lightboxFigure.classList.remove(
          "mode-tall",
          "mode-tall-desktop",
          "mode-tall-mobile-centered",
          "zoom-disabled",
          "mobile-gesture-zoom",
          "is-contained-tall-image",
          "has-tall-image",
          "has-tall-video"
        );
      }
      lightboxImageZoomContainer.classList.remove("mobile-gesture-zoom");
      if (lightboxScrollHint) {
        clearScrollHintTimeout();
        lightboxScrollHint.hidden = true;
        lightboxScrollHint.classList.remove("is-dismissed");
      }
      if (lightboxTallHeader) {
        lightboxTallHeader.hidden = true;
      }
      if (lightboxTallCounter) {
        lightboxTallCounter.hidden = true;
        lightboxTallCounter.textContent = "";
      }
      if (lightboxTallNav) {
        lightboxTallNav.hidden = true;
        lightboxTallNav.replaceChildren();
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

    lightboxImage.addEventListener("click", (event) => {
      if (!lightboxImage.src || lightboxImage.hidden) {
        return;
      }

      if (!isZoomEnabledForItem(currentGroup[currentIndex]) || isMobileMediaViewport()) {
        return;
      }

      toggleZoom(event);
    });

    lightboxImageZoomContainer.addEventListener(
      "touchstart",
      (event) => {
        if (!isMobileGestureZoomEnabled() || lightboxImage.hidden) {
          return;
        }

        if (event.touches.length === 2) {
          event.preventDefault();
          const midpoint = getTouchMidpoint(event.touches[0], event.touches[1]);
          const point = getPointWithinZoomContainer(midpoint.x, midpoint.y);
          pinchStartDistance = getTouchDistance(event.touches[0], event.touches[1]);
          pinchStartScale = mobileZoomScale;
          pinchContentX = (point.x - lightboxImageZoomContainer.clientWidth / 2 - mobileZoomTranslateX) / mobileZoomScale;
          pinchContentY = (point.y - lightboxImageZoomContainer.clientHeight / 2 - mobileZoomTranslateY) / mobileZoomScale;
          lightboxImageZoomContainer.classList.add("is-mobile-pinching");
          return;
        }

        if (event.touches.length === 1 && mobileZoomScale > 1.001) {
          event.preventDefault();
          panStartX = event.touches[0].clientX;
          panStartY = event.touches[0].clientY;
          panStartTranslateX = mobileZoomTranslateX;
          panStartTranslateY = mobileZoomTranslateY;
        }
      },
      { passive: false },
    );

    lightboxImageZoomContainer.addEventListener(
      "touchmove",
      (event) => {
        if (!isMobileGestureZoomEnabled() || lightboxImage.hidden) {
          return;
        }

        if (event.touches.length === 2 && pinchStartDistance > 0) {
          event.preventDefault();
          const midpoint = getTouchMidpoint(event.touches[0], event.touches[1]);
          const point = getPointWithinZoomContainer(midpoint.x, midpoint.y);
          const nextDistance = getTouchDistance(event.touches[0], event.touches[1]);
          const nextScale = Math.min(Math.max((pinchStartScale * nextDistance) / pinchStartDistance, 1), 4);
          mobileZoomScale = nextScale;
          mobileZoomTranslateX = point.x - lightboxImageZoomContainer.clientWidth / 2 - pinchContentX * nextScale;
          mobileZoomTranslateY = point.y - lightboxImageZoomContainer.clientHeight / 2 - pinchContentY * nextScale;
          applyMobileImageTransform();
          return;
        }

        if (event.touches.length === 1 && mobileZoomScale > 1.001) {
          event.preventDefault();
          mobileZoomTranslateX = panStartTranslateX + (event.touches[0].clientX - panStartX);
          mobileZoomTranslateY = panStartTranslateY + (event.touches[0].clientY - panStartY);
          applyMobileImageTransform();
        }
      },
      { passive: false },
    );

    lightboxImageZoomContainer.addEventListener(
      "touchend",
      (event) => {
        if (!isMobileGestureZoomEnabled()) {
          return;
        }

        if (event.touches.length < 2) {
          pinchStartDistance = 0;
          lightboxImageZoomContainer.classList.remove("is-mobile-pinching");
        }

        if (event.touches.length === 1 && mobileZoomScale > 1.001) {
          panStartX = event.touches[0].clientX;
          panStartY = event.touches[0].clientY;
          panStartTranslateX = mobileZoomTranslateX;
          panStartTranslateY = mobileZoomTranslateY;
          return;
        }

        if (event.touches.length === 0) {
          applyMobileImageTransform();
        }
      },
      { passive: true },
    );

    if (lightboxFigure) {
      lightboxFigure.addEventListener("scroll", () => {
        if (isPositioningTallMedia || !shouldShowScrollHint()) {
          return;
        }

        if (isNearFigureBottom()) {
          dismissScrollHint();
        } else if (lightboxScrollHint.hidden) {
          syncScrollHint();
        }
      });

      lightboxFigure.addEventListener(
        "wheel",
        () => {
          if (shouldShowScrollHint() && isNearFigureBottom()) {
            dismissScrollHint();
          } else if (shouldShowScrollHint() && lightboxScrollHint && lightboxScrollHint.hidden) {
            syncScrollHint();
          }
        },
        { passive: true }
      );

      lightboxFigure.addEventListener(
        "touchmove",
        () => {
          if (shouldShowScrollHint() && isNearFigureBottom()) {
            dismissScrollHint();
          } else if (shouldShowScrollHint() && lightboxScrollHint && lightboxScrollHint.hidden) {
            syncScrollHint();
          }
        },
        { passive: true }
      );
    }

    document.addEventListener("keydown", (event) => {
      if (!lightboxModal.classList.contains("open") || currentMode !== "tall") {
        return;
      }

      if (["ArrowDown", "ArrowUp", "PageDown", "PageUp", "Home", "End", " "].includes(event.key) && isNearFigureBottom()) {
        dismissScrollHint();
      }
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

    document.addEventListener("keydown", (event) => {
      if (!lightboxModal.classList.contains("open")) {
        return;
      }

      if (event.key === "Escape") {
        event.preventDefault();
        closeLightbox();
      } else if (event.key === "ArrowLeft") {
        if (currentMode !== "tall" || lightboxModal.classList.contains("mode-tall-desktop")) {
          event.preventDefault();
          stepLightbox(-1);
        }
      } else if (event.key === "ArrowRight") {
        if (currentMode !== "tall" || lightboxModal.classList.contains("mode-tall-desktop")) {
          event.preventDefault();
          stepLightbox(1);
        }
      }
    });
  }
})();

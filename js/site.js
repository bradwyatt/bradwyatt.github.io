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

  const concertCuratorPreviewVideo = document.querySelector(
    ".concert-curator-card .project-gallery-preview video",
  );
  if (concertCuratorPreviewVideo) {
    const mobilePreviewQuery = window.matchMedia("(max-width: 720px)");
    const syncConcertCuratorPreviewVideo = () => {
      if (!mobilePreviewQuery.matches) {
        return;
      }

      concertCuratorPreviewVideo.muted = true;
      concertCuratorPreviewVideo.defaultMuted = true;
      concertCuratorPreviewVideo.playsInline = true;

      if (concertCuratorPreviewVideo.paused) {
        concertCuratorPreviewVideo.play().catch(() => {});
      }
    };

    syncConcertCuratorPreviewVideo();
    concertCuratorPreviewVideo.addEventListener("loadedmetadata", syncConcertCuratorPreviewVideo);
    concertCuratorPreviewVideo.addEventListener("canplay", syncConcertCuratorPreviewVideo);
    document.addEventListener("visibilitychange", () => {
      if (!document.hidden) {
        syncConcertCuratorPreviewVideo();
      }
    });
    window.addEventListener("pageshow", syncConcertCuratorPreviewVideo);
    window.addEventListener("orientationchange", syncConcertCuratorPreviewVideo);
    mobilePreviewQuery.addEventListener("change", syncConcertCuratorPreviewVideo);
  }

  let activeModalHistory = null;
  let ignoreNextModalPopstate = false;

  const registerModalHistory = (key, closeHandler) => {
    activeModalHistory = { key, closeHandler };
    history.pushState({ ...(history.state || {}), __siteModal: key }, "", window.location.href);
  };

  const releaseModalHistory = ({ fromHistory = false } = {}) => {
    if (!activeModalHistory) {
      return;
    }

    activeModalHistory = null;
    if (!fromHistory && history.state && history.state.__siteModal) {
      ignoreNextModalPopstate = true;
      history.back();
    }
  };

  window.addEventListener("popstate", () => {
    if (ignoreNextModalPopstate) {
      ignoreNextModalPopstate = false;
      return;
    }

    if (!activeModalHistory) {
      return;
    }

    const { closeHandler } = activeModalHistory;
    activeModalHistory = null;
    closeHandler({ fromHistory: true });
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
    const closeModal = ({ fromHistory = false } = {}) => {
      modal.classList.remove("open");
      modal.setAttribute("aria-hidden", "true");
      modalVideo.pause();
      Array.from(modalVideo.textTracks || []).forEach((textTrack) => {
        textTrack.mode = "disabled";
      });
      rebuildModalVideo();
      releaseModalHistory({ fromHistory });
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
        registerModalHistory("video-modal", closeModal);
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
    const lightboxScrollbarIndicator = document.getElementById("lightbox-scrollbar-indicator");
    const lightboxScrollbarThumb = document.getElementById("lightbox-scrollbar-thumb");
    const lightboxTallHeader = document.getElementById("lightbox-tall-header");
    const lightboxTallLabel = document.getElementById("lightbox-tall-label");
    const lightboxTallCounter = document.getElementById("lightbox-tall-counter");
    const lightboxTallClose = lightboxModal.querySelector(".lightbox-tall-close");
    const lightboxTallNav = document.getElementById("lightbox-tall-nav");
    let isPositioningTallMedia = false;
    let scrollHintTimeoutId = 0;
    let hasDismissedScrollHint = false;

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
    let swipeStartX = 0;
    let swipeStartY = 0;
    let swipeDeltaX = 0;
    let swipeDeltaY = 0;
    let isSwipeTracking = false;
    let swipeAxis = "";
    let lastTapTime = 0;
    let lastTapX = 0;
    let lastTapY = 0;
    let mobileTransformFrameId = 0;

    const isMobileMediaViewport = () => {
      if (window.matchMedia("(max-width: 900px)").matches) {
        return true;
      }

      return window.matchMedia("(hover: none), (pointer: coarse)").matches;
    };

    const isDesktopTallViewport = () => !isMobileMediaViewport();
    const isMobileLandscapeViewport = () =>
      isMobileMediaViewport() && window.matchMedia("(orientation: landscape)").matches;
    const isPortraitOrientation = () => window.matchMedia("(orientation: portrait)").matches;

    const syncMobileZoomLockState = () => {
      const shouldLock = isMobileMediaViewport() && mobileZoomScale > 1.001;
      lightboxModal.classList.toggle("is-mobile-zoom-locked", shouldLock);
      if (lightboxPanel) {
        lightboxPanel.classList.toggle("is-mobile-zoom-locked", shouldLock);
      }
      if (lightboxFigure) {
        lightboxFigure.classList.toggle("is-mobile-zoom-locked", shouldLock);
      }
    };

    const clearMobileZoomPresentation = () => {
      if (mobileTransformFrameId) {
        window.cancelAnimationFrame(mobileTransformFrameId);
        mobileTransformFrameId = 0;
      }
      lightboxImage.style.transform = "";
      lightboxImage.style.transformOrigin = "";
      lightboxImage.style.willChange = "";
      lightboxImage.classList.remove("is-mobile-zoomed");
      lightboxImageZoomContainer.classList.remove("is-mobile-zoom-active");
      lightboxImageZoomContainer.classList.remove("is-mobile-pinching");
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
      syncMobileZoomLockState();
      syncScrollIndicator();
    };

    const lockMobileZoomBaseSize = () => {
      if (!isMobileGestureZoomEnabled() || lightboxImage.hidden) {
        return;
      }

      const imageRect = lightboxImage.getBoundingClientRect();
      if (!imageRect.width || !imageRect.height) {
        return;
      }

      lightboxImage.style.width = `${imageRect.width}px`;
      lightboxImage.style.height = `${imageRect.height}px`;
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

    const resetZoom = ({ preserveScrollPosition = false } = {}) => {
      let preservedScrollRatioX = 0;
      let preservedScrollRatioY = 0;

      if (preserveScrollPosition && lightboxFigure && isZoomed) {
        const maxScrollLeft = Math.max(lightboxFigure.scrollWidth - lightboxFigure.clientWidth, 0);
        const maxScrollTop = Math.max(lightboxFigure.scrollHeight - lightboxFigure.clientHeight, 0);
        preservedScrollRatioX = maxScrollLeft > 0 ? lightboxFigure.scrollLeft / maxScrollLeft : 0;
        preservedScrollRatioY = maxScrollTop > 0 ? lightboxFigure.scrollTop / maxScrollTop : 0;
      }

      isZoomed = false;
      if (lightboxFigure) {
        lightboxFigure.classList.remove("is-zoomed");
        if (!preserveScrollPosition) {
          lightboxFigure.scrollTop = 0;
          lightboxFigure.scrollLeft = 0;
        }
      }
      lightboxImage.classList.remove("is-zoomed");
      lightboxImage.style.width = "";
      lightboxImage.style.height = "";
      swipeStartX = 0;
      swipeStartY = 0;
      swipeDeltaX = 0;
      swipeDeltaY = 0;
      isSwipeTracking = false;
      swipeAxis = "";
      clearMobileZoomPresentation();

      if (preserveScrollPosition && lightboxFigure) {
        requestAnimationFrame(() => {
          const nextMaxScrollLeft = Math.max(lightboxFigure.scrollWidth - lightboxFigure.clientWidth, 0);
          const nextMaxScrollTop = Math.max(lightboxFigure.scrollHeight - lightboxFigure.clientHeight, 0);
          lightboxFigure.scrollLeft = nextMaxScrollLeft * preservedScrollRatioX;
          lightboxFigure.scrollTop = nextMaxScrollTop * preservedScrollRatioY;
        });
      }
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

      hasDismissedScrollHint = true;
      clearScrollHintTimeout();
      lightboxScrollHint.classList.add("is-dismissed");
      scrollHintTimeoutId = window.setTimeout(() => {
        lightboxScrollHint.hidden = true;
        lightboxScrollHint.classList.remove("is-dismissed");
        scrollHintTimeoutId = 0;
      }, 180);
    };

    const shouldShowScrollHint = () => {
      return false;
    };

    const syncScrollHint = () => {
      if (!lightboxScrollHint) {
        return;
      }

      clearScrollHintTimeout();
      lightboxScrollHint.classList.remove("is-dismissed");
      if (!shouldShowScrollHint() || hasDismissedScrollHint) {
        lightboxScrollHint.hidden = true;
        return;
      }

      lightboxScrollHint.hidden = false;
    };

    function syncScrollIndicator() {
      if (!lightboxScrollbarIndicator || !lightboxScrollbarThumb || !lightboxFigure) {
        return;
      }

      const isMobileZoomSuppressingIndicator =
        isMobileMediaViewport() &&
        currentMediaType === "image" &&
        mobileZoomScale > 1.001;
      const canShowIndicator =
        currentMode === "tall" &&
        currentMediaType === "image" &&
        lightboxFigure.scrollHeight - lightboxFigure.clientHeight > 24 &&
        !isMobileZoomSuppressingIndicator;

      lightboxScrollbarIndicator.hidden = !canShowIndicator;
      if (!canShowIndicator) {
        lightboxScrollbarThumb.style.removeProperty("height");
        lightboxScrollbarThumb.style.removeProperty("transform");
        return;
      }

      const trackHeight = lightboxScrollbarIndicator.clientHeight;
      const scrollRange = Math.max(lightboxFigure.scrollHeight - lightboxFigure.clientHeight, 0);
      const visibleRatio = lightboxFigure.clientHeight / lightboxFigure.scrollHeight;
      const thumbHeight = Math.max(Math.round(trackHeight * visibleRatio), 44);
      const maxThumbOffset = Math.max(trackHeight - thumbHeight, 0);
      const scrollProgress = scrollRange > 0 ? lightboxFigure.scrollTop / scrollRange : 0;
      const thumbOffset = maxThumbOffset * scrollProgress;

      lightboxScrollbarThumb.style.height = `${thumbHeight}px`;
      lightboxScrollbarThumb.style.transform = `translateY(${thumbOffset}px)`;
    }

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
        const shouldCenterTallMobileImage = lightboxFigure.classList.contains("mode-tall-mobile-centered");
        lightboxFigure.scrollTop = shouldCenterTallMobileImage ? 0 : 0;
        lightboxFigure.scrollLeft = 0;
        requestAnimationFrame(() => {
          isPositioningTallMedia = false;
          syncScrollHint();
          syncScrollIndicator();
        });
        return;
      }

      const shouldCenterTallMobileMedia = lightboxFigure.classList.contains("mode-tall-mobile-centered");
      lightboxFigure.scrollTop = 0;
      lightboxFigure.scrollLeft = shouldCenterTallMobileMedia ? 0 : 0;
      requestAnimationFrame(() => {
        isPositioningTallMedia = false;
        syncScrollHint();
        syncScrollIndicator();
      });
    };

    const toggleZoom = (event) => {
      if (!lightboxImage.src || lightboxImage.hidden) {
        return;
      }

      if (isZoomed) {
        resetZoom({ preserveScrollPosition: true });
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

        const figureRect = lightboxFigure.getBoundingClientRect();
        const zoomedRect = lightboxImage.getBoundingClientRect();
        const pointerX = event.clientX - imageRect.left;
        const pointerY = event.clientY - imageRect.top;
        const xRatio = imageRect.width ? pointerX / imageRect.width : 0.5;
        const yRatio = imageRect.height ? pointerY / imageRect.height : 0.5;
        const targetPointX = zoomedRect.width * xRatio;
        const targetPointY = zoomedRect.height * yRatio;
        const viewportPointX = event.clientX - figureRect.left;
        const viewportPointY = event.clientY - figureRect.top;
        const targetLeft = Math.max(targetPointX - viewportPointX, 0);
        const targetTop = Math.max(targetPointY - viewportPointY, 0);

        lightboxFigure.scrollLeft = targetLeft;
        lightboxFigure.scrollTop = targetTop;
        syncScrollIndicator();
      });
    };

    const isMobileGestureZoomEnabled = (item = currentGroup[currentIndex]) =>
      currentMediaType === "image" && isZoomEnabledForItem(item) && isMobileMediaViewport();

    const canSwipeLightboxMedia = () =>
      lightboxModal.classList.contains("open") &&
      isMobileMediaViewport() &&
      currentGroup.length > 1 &&
      mobileZoomScale <= 1.001 &&
      pinchStartDistance === 0;

    const getTouchDistance = (touchA, touchB) => Math.hypot(touchB.clientX - touchA.clientX, touchB.clientY - touchA.clientY);

    const getTouchMidpoint = (touchA, touchB) => ({
      x: (touchA.clientX + touchB.clientX) / 2,
      y: (touchA.clientY + touchB.clientY) / 2,
    });

    const getMobilePinchScale = (nextDistance) => {
      const distanceRatio = pinchStartDistance > 0 ? nextDistance / pinchStartDistance : 1;
      if (!Number.isFinite(distanceRatio)) {
        return pinchStartScale;
      }

      if (!isMobileLandscapeViewport()) {
        return Math.min(Math.max(pinchStartScale * distanceRatio, 1), 4);
      }

      const landscapePinchSensitivity = 0.42;
      const scaleDelta = (distanceRatio - 1) * landscapePinchSensitivity;
      return Math.min(Math.max(pinchStartScale + scaleDelta, 1), 4);
    };

    const isNaturalSizeMobileImage = (item = currentGroup[currentIndex]) => {
      if (!item || currentMode !== "tall" || currentMediaType !== "image" || !isMobileMediaViewport()) {
        return false;
      }

      return item.getAttribute("data-lightbox-natural-size-mobile") === "true";
    };

    const isMetadataExportImage = (item = currentGroup[currentIndex]) => {
      if (!item || currentMode !== "tall" || currentMediaType !== "image") {
        return false;
      }

      return getLightboxLabel(item) === "Metadata Export";
    };

    const isContainedTallImage = (item = currentGroup[currentIndex]) => {
      if (!item || currentMode !== "tall" || currentMediaType !== "image" || !isMobileMediaViewport()) {
        return false;
      }

      const activeLabel = getLightboxLabel(item);
      return activeLabel === "Playlist Sample" || item.getAttribute("data-lightbox-contained") === "true";
    };

    const isDesktopContainedTallImage = (item = currentGroup[currentIndex]) => {
      if (!item || currentMode !== "tall" || currentMediaType !== "image" || !isDesktopTallViewport()) {
        return false;
      }

      return item.getAttribute("data-lightbox-desktop-contained") === "true";
    };

    const getZoomViewportMetrics = () => {
      const activeItem = currentGroup[currentIndex];
      const useCenteredMobileViewport =
        currentMode === "tall" &&
        currentMediaType === "image" &&
        isMobileMediaViewport() &&
        lightboxFigure &&
        lightboxFigure.classList.contains("mode-tall-mobile-centered");
      const useContainedImageViewport = isContainedTallImage(activeItem);
      const useNaturalSizeImageViewport = isNaturalSizeMobileImage(activeItem);
      const useFigureViewport =
        currentMode === "tall" &&
        currentMediaType === "image" &&
        Boolean(lightboxFigure) &&
        !useCenteredMobileViewport &&
        !useContainedImageViewport &&
        !useNaturalSizeImageViewport;
      const viewport = useFigureViewport ? lightboxFigure : lightboxImageZoomContainer;
      const rect = viewport.getBoundingClientRect();

      return {
        rect,
        width: viewport.clientWidth,
        height: viewport.clientHeight,
        scrollLeft: useFigureViewport ? lightboxFigure.scrollLeft : 0,
        scrollTop: useFigureViewport ? lightboxFigure.scrollTop : 0,
      };
    };

    const getPointWithinZoomContainer = (clientX, clientY) => {
      const metrics = getZoomViewportMetrics();
      return {
        x: clientX - metrics.rect.left,
        y: clientY - metrics.rect.top,
      };
    };

    const isCenteredMobileZoomViewport = () =>
      currentMode === "tall" &&
      currentMediaType === "image" &&
      isMobileMediaViewport() &&
      Boolean(lightboxFigure) &&
      lightboxFigure.classList.contains("mode-tall-mobile-centered");

    const centerZoomedImageInViewport = (nextScale) => {
      const imageWidth = lightboxImage.offsetWidth;
      const imageHeight = lightboxImage.offsetHeight;

      mobileZoomScale = nextScale;
      mobileZoomTranslateX = imageWidth * (1 - nextScale) / 2;
      mobileZoomTranslateY = imageHeight * (1 - nextScale) / 2;
    };

    const clampMobileTranslation = (nextScale = mobileZoomScale, nextX = mobileZoomTranslateX, nextY = mobileZoomTranslateY) => {
      const metrics = getZoomViewportMetrics();
      const containerWidth = metrics.width;
      const containerHeight = metrics.height;
      const imageWidth = lightboxImage.offsetWidth;
      const imageHeight = lightboxImage.offsetHeight;
      const scaledWidth = imageWidth * nextScale;
      const scaledHeight = imageHeight * nextScale;
      const naturalOffsetX = Math.max((containerWidth - imageWidth) / 2, 0);
      const naturalOffsetY = Math.max((containerHeight - imageHeight) / 2, 0);
      const minX =
        scaledWidth <= containerWidth
          ? metrics.scrollLeft + (imageWidth - scaledWidth) / 2
          : metrics.scrollLeft + containerWidth - scaledWidth - naturalOffsetX;
      const maxX = scaledWidth <= containerWidth ? minX : metrics.scrollLeft - naturalOffsetX;
      const minY =
        scaledHeight <= containerHeight
          ? metrics.scrollTop + (imageHeight - scaledHeight) / 2
          : metrics.scrollTop + containerHeight - scaledHeight - naturalOffsetY;
      const maxY = scaledHeight <= containerHeight ? minY : metrics.scrollTop - naturalOffsetY;

      return {
        x: Math.min(Math.max(nextX, minX), maxX),
        y: Math.min(Math.max(nextY, minY), maxY),
      };
    };

    const applyMobileImageTransform = () => {
      mobileTransformFrameId = 0;
      const clamped = clampMobileTranslation();
      mobileZoomTranslateX = clamped.x;
      mobileZoomTranslateY = clamped.y;

      if (mobileZoomScale <= 1.001) {
        clearMobileZoomPresentation();
        return;
      }

      lightboxImage.style.transformOrigin = "0 0";
      lightboxImage.style.willChange = "transform";
      lightboxImage.style.transform = `translate3d(${mobileZoomTranslateX}px, ${mobileZoomTranslateY}px, 0) scale(${mobileZoomScale})`;
      lightboxImage.classList.add("is-mobile-zoomed");
      lightboxImageZoomContainer.classList.add("is-mobile-zoom-active");
      syncMobileZoomLockState();
      syncScrollIndicator();
    };

    const scheduleMobileImageTransform = () => {
      if (mobileTransformFrameId) {
        return;
      }

      mobileTransformFrameId = window.requestAnimationFrame(() => {
        applyMobileImageTransform();
      });
    };

    const zoomMobileImageToPoint = (clientX, clientY, nextScale) => {
      const clampedScale = Math.min(Math.max(nextScale, 1), 4);
      if (clampedScale <= 1.001) {
        resetZoom();
        return;
      }

      if (isCenteredMobileZoomViewport()) {
        centerZoomedImageInViewport(clampedScale);
        applyMobileImageTransform();
        return;
      }

      const metrics = getZoomViewportMetrics();
      const point = getPointWithinZoomContainer(clientX, clientY);
      const localX = (metrics.scrollLeft + point.x - mobileZoomTranslateX) / mobileZoomScale;
      const localY = (metrics.scrollTop + point.y - mobileZoomTranslateY) / mobileZoomScale;
      mobileZoomScale = clampedScale;
      mobileZoomTranslateX = metrics.scrollLeft + point.x - localX * clampedScale;
      mobileZoomTranslateY = metrics.scrollTop + point.y - localY * clampedScale;
      applyMobileImageTransform();
    };

    window.addEventListener("resize", () => {
      if (!lightboxModal.classList.contains("open") || mobileZoomScale <= 1.001) {
        return;
      }

      scheduleMobileImageTransform();
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

    const getActiveLightboxImageSource = (item) => {
      if (!item) {
        return "";
      }

      if (isMobileMediaViewport() && isPortraitOrientation()) {
        const portraitSource = item.getAttribute("data-lightbox-src-portrait");
        if (portraitSource) {
          return portraitSource;
        }
      }

      const landscapeSource = item.getAttribute("data-lightbox-src-landscape");
      if (landscapeSource && isMobileMediaViewport() && isMobileLandscapeViewport()) {
        return landscapeSource;
      }

      return item.getAttribute("data-lightbox-src") || "";
    };

    const hasResponsiveLightboxImageSource = (item) =>
      Boolean(item?.getAttribute("data-lightbox-src-portrait") || item?.getAttribute("data-lightbox-src-landscape"));

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

      hasDismissedScrollHint = false;
      resetZoom();
      resetVideo();

      currentMediaType = activeItem.getAttribute("data-lightbox-type") || "image";
      const prefersTallMode = activeItem.getAttribute("data-lightbox-mode") === "tall";
      const activeGroupName = activeItem.getAttribute("data-lightbox-group") || "";
      const isConcertCuratorLightbox = activeGroupName === "concert-curator";
      const useImmersiveMobileImageLayout = currentMediaType === "image" && isMobileMediaViewport();
      currentMode = prefersTallMode || useImmersiveMobileImageLayout ? "tall" : "standard";
      const activeLabel = getLightboxLabel(activeItem);
      const useDesktopTallLayout = prefersTallMode && currentMode === "tall" && isDesktopTallViewport();
      const useCompactConcertCuratorLandscape =
        isConcertCuratorLightbox &&
        currentMode === "tall" &&
        currentMediaType === "image" &&
        isMobileLandscapeViewport();
      const useCenteredTallMedia =
        currentMode === "tall" &&
        isMobileMediaViewport() &&
        (
          (useImmersiveMobileImageLayout && !prefersTallMode && isPortraitOrientation()) ||
          activeItem.getAttribute("data-lightbox-centered") === "true"
        );
      const useContainedTallImage =
        currentMode === "tall" &&
        currentMediaType === "image" &&
        (
          isContainedTallImage(activeItem) ||
          isDesktopContainedTallImage(activeItem)
        );
      const useNaturalSizeImage =
        currentMode === "tall" &&
        currentMediaType === "image" &&
        isNaturalSizeMobileImage(activeItem);
      const useMetadataExportLayout = isMetadataExportImage(activeItem);
      const isZoomEnabled = currentMediaType === "image" && isZoomEnabledForItem(activeItem);
      const isMobileGestureZoomActive = isZoomEnabled && isMobileMediaViewport();
      const isZipTextLightboxVideo =
        currentMediaType === "video" &&
        activeItem.getAttribute("data-lightbox-group") === "zip-text-droid";
      lightboxModal.classList.toggle("mode-tall", currentMode === "tall");
      lightboxModal.classList.toggle("mode-standard", currentMode !== "tall");
      lightboxModal.classList.toggle("mode-tall-desktop", useDesktopTallLayout);
      lightboxModal.classList.toggle("mode-tall-mobile-centered", useCenteredTallMedia);
      lightboxModal.classList.toggle("concert-curator-lightbox", isConcertCuratorLightbox);
      lightboxModal.classList.toggle("concert-curator-landscape-compact", useCompactConcertCuratorLandscape);
      lightboxModal.classList.toggle("has-contained-tall-image", useContainedTallImage);
      lightboxModal.classList.toggle("has-tall-image", currentMode === "tall" && currentMediaType === "image");
      lightboxModal.classList.toggle("has-tall-video", currentMode === "tall" && currentMediaType === "video");
      lightboxModal.classList.toggle("zip-text-landscape-video", isZipTextLightboxVideo);
      lightboxModal.classList.toggle("zoom-disabled", !isZoomEnabled);
      lightboxModal.classList.toggle("mobile-gesture-zoom", isMobileGestureZoomActive);
      lightboxModal.classList.toggle("has-natural-size-image", useNaturalSizeImage);
      lightboxModal.classList.toggle("is-metadata-export", useMetadataExportLayout);
      if (lightboxPanel) {
        lightboxPanel.classList.toggle("mode-tall", currentMode === "tall");
        lightboxPanel.classList.toggle("mode-standard", currentMode !== "tall");
        lightboxPanel.classList.toggle("mode-tall-desktop", useDesktopTallLayout);
        lightboxPanel.classList.toggle("mode-tall-mobile-centered", useCenteredTallMedia);
        lightboxPanel.classList.toggle("concert-curator-lightbox", isConcertCuratorLightbox);
        lightboxPanel.classList.toggle("concert-curator-landscape-compact", useCompactConcertCuratorLandscape);
        lightboxPanel.classList.toggle("has-contained-tall-image", useContainedTallImage);
        lightboxPanel.classList.toggle("has-tall-image", currentMode === "tall" && currentMediaType === "image");
        lightboxPanel.classList.toggle("has-tall-video", currentMode === "tall" && currentMediaType === "video");
        lightboxPanel.classList.toggle("zip-text-landscape-video", isZipTextLightboxVideo);
        lightboxPanel.classList.toggle("zoom-disabled", !isZoomEnabled);
        lightboxPanel.classList.toggle("mobile-gesture-zoom", isMobileGestureZoomActive);
        lightboxPanel.classList.toggle("has-natural-size-image", useNaturalSizeImage);
        lightboxPanel.classList.toggle("is-metadata-export", useMetadataExportLayout);
      }
      if (lightboxFigure) {
        lightboxFigure.classList.toggle("mode-tall", currentMode === "tall");
        lightboxFigure.classList.toggle("mode-tall-desktop", useDesktopTallLayout);
        lightboxFigure.classList.toggle("mode-tall-mobile-centered", useCenteredTallMedia);
        lightboxFigure.classList.toggle("concert-curator-lightbox", isConcertCuratorLightbox);
        lightboxFigure.classList.toggle("concert-curator-landscape-compact", useCompactConcertCuratorLandscape);
        lightboxFigure.classList.toggle("is-contained-tall-image", useContainedTallImage);
        lightboxFigure.classList.toggle("has-tall-image", currentMode === "tall" && currentMediaType === "image");
        lightboxFigure.classList.toggle("has-tall-video", currentMode === "tall" && currentMediaType === "video");
        lightboxFigure.classList.toggle("zip-text-landscape-video", isZipTextLightboxVideo);
        lightboxFigure.classList.toggle("zoom-disabled", !isZoomEnabled);
        lightboxFigure.classList.toggle("mobile-gesture-zoom", isMobileGestureZoomActive);
        lightboxFigure.classList.toggle("has-natural-size-image", useNaturalSizeImage);
        lightboxFigure.classList.toggle("is-metadata-export", useMetadataExportLayout);
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
        lightboxVideo.addEventListener("loadedmetadata", positionTallMedia, { once: true });
        lightboxVideo.load();
        syncScrollHint();
        requestAnimationFrame(positionTallMedia);
        lightboxVideo.play().catch(() => {});
      } else {
        lightboxImageZoomContainer.hidden = false;
        lightboxVideo.hidden = true;
        lightboxImage.hidden = false;
        lightboxImage.src = getActiveLightboxImageSource(activeItem);
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
      registerModalHistory("lightbox-modal", closeLightbox);
      const focusTarget = currentMode === "tall" ? (lightboxTallClose || lightboxModal) : (closeButton || lightboxModal);
      focusTarget.focus();
    };

    const closeLightbox = ({ fromHistory = false } = {}) => {
      resetZoom();
      resetVideo();
      lightboxModal.classList.remove("open");
      lightboxModal.classList.remove(
        "mode-tall",
        "mode-standard",
        "mode-tall-desktop",
        "mode-tall-mobile-centered",
        "concert-curator-lightbox",
        "concert-curator-landscape-compact",
        "is-mobile-zoom-locked",
        "zoom-disabled",
        "mobile-gesture-zoom",
        "zip-text-landscape-video",
        "is-metadata-export",
        "has-contained-tall-image",
        "has-natural-size-image",
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
          "concert-curator-lightbox",
          "concert-curator-landscape-compact",
          "is-mobile-zoom-locked",
          "zoom-disabled",
          "mobile-gesture-zoom",
          "zip-text-landscape-video",
          "is-metadata-export",
          "has-contained-tall-image",
          "has-natural-size-image",
          "has-tall-image",
          "has-tall-video"
        );
      }
      if (lightboxFigure) {
        lightboxFigure.classList.remove(
          "mode-tall",
          "mode-tall-desktop",
          "mode-tall-mobile-centered",
          "concert-curator-lightbox",
          "concert-curator-landscape-compact",
          "is-mobile-zoom-locked",
          "zoom-disabled",
          "mobile-gesture-zoom",
          "zip-text-landscape-video",
          "is-metadata-export",
          "is-contained-tall-image",
          "has-natural-size-image",
          "has-tall-image",
          "has-tall-video"
        );
      }
      lightboxImageZoomContainer.classList.remove("mobile-gesture-zoom");
      if (lightboxScrollHint) {
        clearScrollHintTimeout();
        hasDismissedScrollHint = false;
        lightboxScrollHint.hidden = true;
        lightboxScrollHint.classList.remove("is-dismissed");
      }
      if (lightboxScrollbarIndicator) {
        lightboxScrollbarIndicator.hidden = true;
      }
      if (lightboxScrollbarThumb) {
        lightboxScrollbarThumb.style.removeProperty("height");
        lightboxScrollbarThumb.style.removeProperty("transform");
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
      releaseModalHistory({ fromHistory });
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

    const syncResponsiveLightboxSource = () => {
      if (!lightboxModal.classList.contains("open")) {
        return;
      }

      const activeItem = currentGroup[currentIndex];
      if (!activeItem || currentMediaType !== "image" || !hasResponsiveLightboxImageSource(activeItem)) {
        return;
      }

      const nextSource = getActiveLightboxImageSource(activeItem);
      if (!nextSource || lightboxImage.src.endsWith(nextSource)) {
        return;
      }

      renderMedia();
    };

    window.addEventListener("orientationchange", syncResponsiveLightboxSource);
    window.addEventListener("resize", syncResponsiveLightboxSource);

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
          if (mobileZoomScale <= 1.001) {
            lockMobileZoomBaseSize();
          }
          if (isCenteredMobileZoomViewport()) {
            pinchStartDistance = getTouchDistance(event.touches[0], event.touches[1]);
            pinchStartScale = mobileZoomScale;
            lightboxImageZoomContainer.classList.add("is-mobile-pinching");
            return;
          }

          const metrics = getZoomViewportMetrics();
          const midpoint = getTouchMidpoint(event.touches[0], event.touches[1]);
          const point = getPointWithinZoomContainer(midpoint.x, midpoint.y);
          pinchStartDistance = getTouchDistance(event.touches[0], event.touches[1]);
          pinchStartScale = mobileZoomScale;
          pinchContentX = (metrics.scrollLeft + point.x - mobileZoomTranslateX) / mobileZoomScale;
          pinchContentY = (metrics.scrollTop + point.y - mobileZoomTranslateY) / mobileZoomScale;
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
          if (isCenteredMobileZoomViewport()) {
            const nextDistance = getTouchDistance(event.touches[0], event.touches[1]);
            const nextScale = getMobilePinchScale(nextDistance);
            centerZoomedImageInViewport(nextScale);
            scheduleMobileImageTransform();
            return;
          }

          const metrics = getZoomViewportMetrics();
          const midpoint = getTouchMidpoint(event.touches[0], event.touches[1]);
          const point = getPointWithinZoomContainer(midpoint.x, midpoint.y);
          const nextDistance = getTouchDistance(event.touches[0], event.touches[1]);
          const nextScale = getMobilePinchScale(nextDistance);
          mobileZoomScale = nextScale;
          mobileZoomTranslateX = metrics.scrollLeft + point.x - pinchContentX * nextScale;
          mobileZoomTranslateY = metrics.scrollTop + point.y - pinchContentY * nextScale;
          scheduleMobileImageTransform();
          return;
        }

        if (event.touches.length === 1 && mobileZoomScale > 1.001) {
          event.preventDefault();
          mobileZoomTranslateX = panStartTranslateX + (event.touches[0].clientX - panStartX);
          mobileZoomTranslateY = panStartTranslateY + (event.touches[0].clientY - panStartY);
          scheduleMobileImageTransform();
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
          scheduleMobileImageTransform();
        }
      },
      { passive: true },
    );

    lightboxImageZoomContainer.addEventListener(
      "touchend",
      (event) => {
        if (!isMobileGestureZoomEnabled() || lightboxImage.hidden || event.touches.length !== 0) {
          return;
        }

        const touch = event.changedTouches[0];
        if (!touch) {
          return;
        }

        const now = Date.now();
        const isDoubleTap =
          now - lastTapTime < 280 &&
          Math.hypot(touch.clientX - lastTapX, touch.clientY - lastTapY) < 24;

        lastTapTime = now;
        lastTapX = touch.clientX;
        lastTapY = touch.clientY;

        if (!isDoubleTap) {
          return;
        }

        event.preventDefault();
        if (mobileZoomScale > 1.001) {
          resetZoom();
          return;
        }

        zoomMobileImageToPoint(touch.clientX, touch.clientY, 2.2);
      },
      { passive: false },
    );

    if (lightboxFigure) {
      lightboxFigure.addEventListener(
        "touchstart",
        (event) => {
          if (!canSwipeLightboxMedia() || event.touches.length !== 1) {
            isSwipeTracking = false;
            swipeAxis = "";
            return;
          }

          swipeStartX = event.touches[0].clientX;
          swipeStartY = event.touches[0].clientY;
          swipeDeltaX = 0;
          swipeDeltaY = 0;
          isSwipeTracking = true;
          swipeAxis = "";
        },
        { passive: true }
      );

      lightboxFigure.addEventListener(
        "touchmove",
        (event) => {
          if (!isSwipeTracking || event.touches.length !== 1 || !canSwipeLightboxMedia()) {
            return;
          }

          swipeDeltaX = event.touches[0].clientX - swipeStartX;
          swipeDeltaY = event.touches[0].clientY - swipeStartY;

          if (!swipeAxis) {
            if (Math.abs(swipeDeltaX) < 12 && Math.abs(swipeDeltaY) < 12) {
              return;
            }

            swipeAxis = Math.abs(swipeDeltaX) > Math.abs(swipeDeltaY) * 1.15 ? "x" : "y";
          }

          if (swipeAxis === "x") {
            event.preventDefault();
          } else {
            isSwipeTracking = false;
          }
        },
        { passive: false }
      );

      lightboxFigure.addEventListener(
        "touchend",
        () => {
          if (!isSwipeTracking || swipeAxis !== "x") {
            isSwipeTracking = false;
            swipeAxis = "";
            return;
          }

          if (Math.abs(swipeDeltaX) > 72 && Math.abs(swipeDeltaX) > Math.abs(swipeDeltaY) * 1.15) {
            stepLightbox(swipeDeltaX < 0 ? 1 : -1);
          }

          isSwipeTracking = false;
          swipeAxis = "";
          swipeDeltaX = 0;
          swipeDeltaY = 0;
        },
        { passive: true }
      );

      lightboxFigure.addEventListener("scroll", () => {
        if (isPositioningTallMedia || !shouldShowScrollHint()) {
          syncScrollIndicator();
          if (isPositioningTallMedia) {
            return;
          }
        } else if (isNearFigureBottom()) {
          dismissScrollHint();
        } else if (lightboxScrollHint.hidden) {
          syncScrollHint();
        }
        syncScrollIndicator();
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

    window.addEventListener("resize", () => {
      if (!lightboxModal.classList.contains("open")) {
        return;
      }

      syncScrollIndicator();
    });

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

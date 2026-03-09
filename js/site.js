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
})();

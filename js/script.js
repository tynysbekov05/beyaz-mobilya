// Update copyright year
document.getElementById('year').textContent = new Date().getFullYear();

// Wait for DOM to load
document.addEventListener("DOMContentLoaded", (event) => {
    // Register GSAP plugins
    gsap.registerPlugin(ScrollTrigger);

    // Initial Hero Animations
    const tl = gsap.timeline();
    
    tl.fromTo(".gsap-reveal-up", 
        { y: 50, opacity: 0 },
        { y: 0, opacity: 1, duration: 1, stagger: 0.2, ease: "power3.out" }
    );

    // Hero Image/Video 3D Parallax entry
    tl.fromTo(".gsap-scale",
        { scale: 0.9, opacity: 0, y: 30 },
        { scale: 1, opacity: 1, y: 0, duration: 1.2, ease: "power2.out" },
        "-=0.5"
    );

    // Scroll trigger for Trust Bar elements
    gsap.utils.toArray('.gsap-fade').forEach(element => {
        gsap.fromTo(element, 
            { opacity: 0, x: -30 },
            {
                opacity: 1,
                x: 0,
                duration: 0.8,
                ease: "power2.out",
                scrollTrigger: {
                    trigger: element,
                    start: "top 85%",
                    toggleActions: "play none none reverse"
                }
            }
        );
    });

    // Scroll trigger for Collection Items
    gsap.utils.toArray('.gsap-fade-up').forEach((element, i) => {
        gsap.fromTo(element,
            { opacity: 0, y: 50 },
            {
                opacity: 1,
                y: 0,
                duration: 0.8,
                ease: "power3.out",
                scrollTrigger: {
                    trigger: element,
                    start: "top 85%",
                    toggleActions: "play none none reset",
                }
            }
        );
    });

    // Smooth subtle parallax on the placeholder images on scroll
    gsap.utils.toArray('.parallax-container .col-image').forEach((element) => {
        gsap.to(element, {
            yPercent: 10,
            ease: "none",
            scrollTrigger: {
                trigger: element.parentElement,
                start: "top bottom", 
                end: "bottom top",
                scrub: true
            }
        });
    });

    // --- V2 JS MODIFICATIONS ---

    // 1. CAROUSEL LOGIC
    const carousels = document.querySelectorAll('.p-card-carousel');
    carousels.forEach(carousel => {
        const slides = carousel.querySelectorAll('.p-card-slide');
        const prevBtn = carousel.querySelector('.p-card-arrow.prev');
        const nextBtn = carousel.querySelector('.p-card-arrow.next');
        let currentSlide = 0;

        if (slides.length > 0) {
            slides[0].classList.add('active');
        }

        const showSlide = (index) => {
            slides.forEach(s => s.classList.remove('active'));
            slides[index].classList.add('active');
        };

        if (nextBtn && prevBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.stopPropagation(); // prevent lightbox opening
                currentSlide = (currentSlide + 1) % slides.length;
                showSlide(currentSlide);
            });

            prevBtn.addEventListener('click', (e) => {
                e.stopPropagation(); // prevent lightbox opening
                currentSlide = (currentSlide - 1 + slides.length) % slides.length;
                showSlide(currentSlide);
            });
        }
    });

    // 2. LIGHTBOX LOGIC
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <button class="lightbox-close">×</button>
        <button class="lightbox-arrow prev">‹</button>
        <img class="lightbox-content" src="" alt="">
        <button class="lightbox-arrow next">›</button>
    `;
    document.body.appendChild(lightbox);

    const lightboxImg = lightbox.querySelector('.lightbox-content');
    const lightboxClose = lightbox.querySelector('.lightbox-close');
    const lightboxNext = lightbox.querySelector('.lightbox-arrow.next');
    const lightboxPrev = lightbox.querySelector('.lightbox-arrow.prev');
    
    let activeLightboxGroup = [];
    let currentLightboxIdx = 0;

    const openLightbox = (imgSrc, group) => {
        activeLightboxGroup = group;
        currentLightboxIdx = group.indexOf(imgSrc);
        lightboxImg.src = imgSrc;
        lightbox.classList.add('open');
        document.body.style.overflow = 'hidden'; // prevent scrolling
    };

    const closeLightboxFn = () => {
        lightbox.classList.remove('open');
        document.body.style.overflow = '';
    };

    const nextLightboxImg = (e) => {
        e.stopPropagation();
        if(activeLightboxGroup.length > 0) {
            currentLightboxIdx = (currentLightboxIdx + 1) % activeLightboxGroup.length;
            lightboxImg.src = activeLightboxGroup[currentLightboxIdx];
        }
    };

    const prevLightboxImg = (e) => {
        e.stopPropagation();
        if(activeLightboxGroup.length > 0) {
            currentLightboxIdx = (currentLightboxIdx - 1 + activeLightboxGroup.length) % activeLightboxGroup.length;
            lightboxImg.src = activeLightboxGroup[currentLightboxIdx];
        }
    };

    lightboxClose.addEventListener('click', closeLightboxFn);
    lightbox.addEventListener('click', closeLightboxFn);
    lightboxImg.addEventListener('click', (e) => e.stopPropagation());
    lightboxNext.addEventListener('click', nextLightboxImg);
    lightboxPrev.addEventListener('click', prevLightboxImg);

    // Bind images to lightbox
    const slidesInit = document.querySelectorAll('.p-card-slide');
    slidesInit.forEach(slide => {
        slide.addEventListener('click', () => {
            // Find its parent carousel
            const parent = slide.closest('.p-card-carousel');
            if(parent) {
                const groupSlides = parent.querySelectorAll('.p-card-slide');
                const groupUrls = Array.from(groupSlides).map(s => s.src);
                openLightbox(slide.src, groupUrls);
            }
        });
    });
});

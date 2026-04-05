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
});

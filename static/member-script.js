document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('.member-section');
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // アニメーションを開始
                    entry.target.classList.add('section-active');
                    // パララックス効果
                    const bgImg = entry.target.getAttribute('data-bg-image');
                    entry.target.style.backgroundImage = `url(${bgImg})`;
                }
            });
        },
        {
            rootMargin: "0px 0px -50% 0px",
            threshold: 0.1
        }
    );

    sections.forEach(section => {
        observer.observe(section);
    });
});
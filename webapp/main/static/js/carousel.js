document.addEventListener("DOMContentLoaded", function () {
    var swiper = new Swiper(".swiper", {
        loop: false,
        spaceBetween: 10,
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        breakpoints: {
            320: { slidesPerView: 1 }, // Mobile: 1 card per slide
            768: { slidesPerView: 2 }, // Tablets: 2 cards per slide
            1024: { slidesPerView: 3 }, // Desktops: 3 cards per slide
        }
    });
});

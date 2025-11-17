// LOADING SCREEN
window.addEventListener("load", () => {
    setTimeout(() => {
        const loader = document.getElementById("loading-screen");
        if (loader) {
            loader.style.opacity = "0";
            loader.style.transition = "0.6s ease";

            setTimeout(() => {
                loader.style.display = "none";
            }, 600);
        }
    }, 500); 
});

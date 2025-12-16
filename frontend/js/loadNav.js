fetch("../partials/nav.html")
    .then(res => res.text())
    .then(html => {
        document.getElementById("navbar").innerHTML = html;

        // Global lock behavior
        document.querySelectorAll("[data-lock]").forEach(el => {
            el.addEventListener("click", e => {
                e.preventDefault();
                alert("This section of UIL Analyzer is coming soon.");
            });
        });
    })
    .catch(err => {
        console.error("Failed to load navbar:", err);
    });

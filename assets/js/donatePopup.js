document.addEventListener("DOMContentLoaded", function () {
    var lastShown = localStorage.getItem("donatePopup");
    var now = new Date().getTime();
    var duration = 1 * 60 * 1000; // 1 minute in milliseconds

    function showPopup() {
        if (confirm("Donate to support the author?\n捐赠支持作者？")) {
            window.location.href = "/pages/donate-en";
        }
        localStorage.setItem("donatePopup", now);
    }

    var timeout = 1 * 60 * 1000;

    if (document.title !== "Donate") {
        if (!lastShown) {
            setTimeout(function () {
                showPopup();
            }, timeout);
        } else if ((now - lastShown) > duration) {
            setTimeout(function () {
                if (Math.random() <= 0.3) {
                    showPopup();
                }
            }, timeout);
        }
    }
});

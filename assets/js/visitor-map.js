(function () {
  "use strict";

  var map = document.querySelector(".visitor-map");
  if (!map) return;

  var image = map.querySelector(".visitor-map-image");
  var status = map.querySelector(".visitor-map-status");
  var retry = map.querySelector(".visitor-map-retry");
  var source = image.src;
  var timeout;

  function showResult(loaded) {
    clearTimeout(timeout);
    image.hidden = !loaded;
    image.parentElement.hidden = !loaded;
    status.hidden = loaded;
  }

  function watchLoading() {
    clearTimeout(timeout);
    timeout = setTimeout(function () { showResult(false); }, 12000);
  }

  image.addEventListener("load", function () { showResult(image.naturalWidth > 0); });
  image.addEventListener("error", function () { showResult(false); });
  retry.addEventListener("click", function () {
    status.hidden = true;
    image.hidden = false;
    image.parentElement.hidden = false;
    watchLoading();
    image.src = source + "?reload=" + Date.now();
  });

  if (image.complete) {
    showResult(image.naturalWidth > 0);
  } else {
    watchLoading();
  }
}());

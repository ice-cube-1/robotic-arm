var links = document.getElementsByTagName("a");
for (var i = 0; i < links.length; i++) {
    if (!links[i].href.startsWith("https")) {
        links[i].href = links[i].href+"index.html"
    }
}
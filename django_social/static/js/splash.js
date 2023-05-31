window.addEventListener('load', showSplashScreen);

function showSplashScreen() {
    var splashScreen = document.getElementById('splash-screen');
    var content = document.getElementById('content');

    splashScreen.style.display = 'flex';
    content.style.display = 'none';

    setTimeout(function () {
        splashScreen.style.display = 'none';
        content.style.display = 'block';
    }, 400);

    // splashScreen.style.display = 'none';
    // content.style.display = 'block';
}

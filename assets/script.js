
// Print to the console whenever the letter Q is pressed
document.addEventListener('keydown', function(event) {
    if (event.key.toLowerCase() === 'q') {
        pywebview.api.close(event.shiftKey);
    }
    // else {
    //     // I want the FRONTEND to determine what (or if) script should be executed and call a
    //     // `execute_script` method on the backend.
    //     // This is just a placeholder
    //     pywebview.api.parse_key(event.key, event.shiftKey)
    // }
});

// var countdown = 10;
var countdown = 100;
setInterval(function() {
    countdown--;
    document.getElementById('countdown').innerText = countdown;
    if (countdown === 0) {
        pywebview.api.close(false);
    }
}, 2000);

// TODO: figure out why this is still not the right size - a little too big
window.addEventListener('pywebviewready', function() {
    let width = document.body.scrollWidth;
    let height = document.body.scrollHeight;
    console.log(width); console.log(height);
    pywebview.api.fit_window(width, height);
});

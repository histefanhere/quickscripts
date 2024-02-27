
var active_group = null;
var groups = [];
var scripts = [];


function setActiveGroup(group) {
    if (group === active_group) {
        return;
    }
    for (var i = 0; i < groups.length; i++) {
        if (groups[i].key == group) {
            active_group = group;
            scripts = groups[i].scripts;
            // TODO: update the UI to reflect the new active group
            console.log('Active group: ' + active_group);
            return;
        }
    }
}


// Print to the console whenever the letter Q is pressed
document.addEventListener('keydown', function(event) {
    if (event.key.toLowerCase() === 'q') {
        pywebview.api.close();
    }
    else {
        // pywebview.api.parse_key(event.key, event.shiftKey)
        for (var i = 0; i < scripts.length; i++) {
            if (scripts[i].key === event.key) {
                console.log(scripts[i].script);
                pywebview.api.execute(scripts[i].command);
            }
        }
    }
});


// var countdown = 10;
var countdown = 100;
setInterval(function() {
    countdown--;
    document.getElementById('countdown').innerText = countdown;
    if (countdown === 0) {
        pywebview.api.close();
    }
}, 2000);


window.addEventListener('pywebviewready', function() {
    pywebview.api.get_groups().then(function(response) {
        groups = response;
        console.log('Groups: ' + groups);
        setActiveGroup(1);
        
        // TODO: figure out why this is still not the right size - a little too big
        let width = document.body.scrollWidth;
        let height = document.body.scrollHeight;
        console.log(width); console.log(height);
        pywebview.api.fit_window(width, height);
    });
});


var groups = [];
var active_group = null;
var maxRows = null;
var initialCountdown = 10;
var countdown = initialCountdown;

function setActiveGroup(group) {
    if (active_group != null && group === active_group.key) {
        return;
    }

    // Reset the countdown whenever the group is changed
    countdown = initialCountdown;

    for (var i = 0; i < groups.length; i++) {
        if (groups[i].key == group) {
            active_group = groups[i];
            
            // Groups header
            let html = '<tr>';
            for (let gi = 0; gi < groups.length; gi++) {
                let group = groups[gi];
                let className = 'text-secondary';
                if (group === active_group) {
                    className = 'text-primary';
                }
                html += `<td><span class="fs-1 me-2 ${className}">${group.key.toUpperCase()}</span></td>
                <td><span class="fs-3 me-3 ${className}">${group.name}</span></td>`;
            }
            html += '</tr>';
            document.getElementById('table-groups').innerHTML = html;

            // Scripts in the group
            let scripts = active_group.scripts;
            html = '';
            for (let ri = 0; ri < Math.min(maxRows, scripts.length); ri++) {
                let row = `<tr>`;
                for (let ci = 0; ci < Math.floor( (scripts.length - ri - 1) / maxRows) + 1; ci++) {
                    let script = scripts[ri + maxRows * ci];
                    console.log(ri, ci, script);
                    row += `<td><span class="fs-1 me-2">${script.key.toUpperCase()}</span></td><td><span class="fs-3 me-5">${script.name}</span></td>`;
                }
                row += `</tr>`;
                html += row;
            }
            html += `
            <tr>
                <td><span class="fs-1 me-2 text-danger">Q</span></td>
                <td><span class="fs-3 me-5 text-danger">Quit (<span id="countdown">${countdown}</span>)</span></td>
            </tr>`;
            document.getElementById('table-scripts').innerHTML = html;

            setTimeout(() => { pywebview.api.fit_window(document.body.scrollWidth, document.body.scrollHeight); }, 50);
            return;
        }
    }
}


// Print to the console whenever the letter Q is pressed
document.addEventListener('keydown', function(event) {
    if (event.key.toLowerCase() === 'q') {
        pywebview.api.close();
        return;
    }

    // Check if it is a group
    for (let i = 0; i < groups.length; i++) {
        if (groups[i].key === event.key) {
            setActiveGroup(event.key);
            return;
        }
    }

    // Check if it is a script
    let scripts = active_group.scripts;
    for (var i = 0; i < scripts.length; i++) {
        if (scripts[i].key === event.key) {
            pywebview.api.execute(scripts[i].command);
            return;
        }
    }
});


setInterval(function() {
    countdown--;
    document.getElementById('countdown').innerText = countdown;
    if (countdown === 0) {
        pywebview.api.close();
    }
}, 2000);


window.addEventListener('pywebviewready', function() {
    // TODO: Make these promises resolve together instead of one after another
    pywebview.api.get_rows().then(function (response) {
        maxRows = response;

        pywebview.api.get_groups().then(function(response) {
            groups = response;
            setActiveGroup(1);
        });
    });
});

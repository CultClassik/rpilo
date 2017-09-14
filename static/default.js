function setState(device) {
    deviceWaiting(device, true);

    // debug
    //alert('Device: ' + device);

    // placeholder until ajax call is implemented
    setTimeout(6);

    // now make an ajax call to the python power function url
        $.getJSON("/devices/power/" + device, function(result){
            console.log(result);
            location.reload();
        });
}

function deviceWaiting(device, wait){
    // disable the buttons for this device
    var buttons = $('a[data-device="' + device + '"]').each(function() {
        //$(this).disabled = true;
        $(this).prop('disabled', true);
        $(this).attr('disabled', true);
    });

    // hide/show the status text
    var status = document.getElementById(device + "-status");
    // hide/show the spinner
    var spinner = document.getElementById(device + "-spinner");
    switch(wait) {
        case true:
            status.hidden = true;
            spinner.hidden = false;
            break;
        case false:
            status.hidden = false;
            spinner.hidden = true;
    }

    // probably should make another ajax call here or something to find out if power is on or off, or just refresh the page ;)
}



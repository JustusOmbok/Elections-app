/*!
* Start Bootstrap - Modern Business v5.0.7 (https://startbootstrap.com/template-overviews/modern-business)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-modern-business/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
document.getElementById('seat').addEventListener('change', function() {
    var selectedSeat = this.value;
    if (selectedSeat === 'presidential') {
        document.getElementById('presidentialFields').style.display = 'block';
        document.getElementById('governorFields').style.display = 'none';
    } else if (selectedSeat === 'governor') {
        document.getElementById('presidentialFields').style.display = 'none';
        document.getElementById('governorFields').style.display = 'block';
    } else {
        document.getElementById('presidentialFields').style.display = 'none';
        document.getElementById('governorFields').style.display = 'none';
    }
});

document.getElementById('county').addEventListener('change', function() {
    var selectedCounty = this.value;
    if (selectedCounty !== '') {
        document.getElementById('governorFields').style.display = 'block';
        document.getElementById('presidentialFields').style.display = 'block';
    } else {
        document.getElementById('governorFields').style.display = 'none';
        document.getElementById('presidentialFields').style.display = 'none';
    }
});
console.log("Script for manage.html loaded!");


function navigateTo(page) {
    window.location.href = `/manage/${page}`;
}


function goBack() {
    window.history.back();
}

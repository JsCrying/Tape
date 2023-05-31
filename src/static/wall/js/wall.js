function showLoading() {
    let table = document.querySelector(".content");
    let _pagination = document.querySelector(".pagination");
    _pagination.innerHTML = ``;
    table.innerHTML = `
        <div class="loading"></div>
        <br>
    `;
}
function concealLoading() {
    let table = document.querySelector(".content");
    table.innerHTML = ``;
}

function load_page(date) {
    showLoading();
    fetch(date);
}
function dateToday() {
    let dateGenerator = new Date();
    let day = ("0" + dateGenerator.getDate()).slice(-2);
    let month = ("0" + (dateGenerator.getMonth() + 1)).slice(-2);
    let today = dateGenerator.getFullYear() + "-" + (month) + "-" + (day);

    return today;
}
const dateForm = document.getElementById('date');
window.onload = function() {
    dateForm.value = dateToday();
    let date = dateForm.value;
    load_page(date);
};
date.onchange = function() {
//    console.log(typeof(date.value));
//    console.log(date.value);
    let date = this.value;
    if (date == '') date = dateToday();
    load_page(date);
}
// 烟雾文字效果
function smoke() {
    const texts = document.querySelectorAll('.quote');
    for (let i = 0; i < texts.length; ++i) 
        texts[i].innerHTML = texts[i].textContent.replace(/\S/g, "<span>$&</span>");

    const letters = document.querySelectorAll(".quote span");
    for (let i = 0; i < letters.length; ++i) {
        letters[i].addEventListener('mouseover', function() {
            letters[i].classList.toggle('active');

            setTimeout(() => {
                letters[i].classList.toggle('active');
            }, 2500);
        });
    }
}

// 消息通知一会儿后消失
const info = document.querySelector("#info");
setTimeout(()=>{
    info.classList.toggle("disappear");
}, 20000);

// 菜单栏控制
const menu = document.querySelector(".menu");
const menuBtn = document.querySelector(".menu-btn");
const counters = document.querySelectorAll(".counter");

// toggle open / close menu
menuBtn.addEventListener("click", () => {
    menu.classList.toggle("menu-open");
});

// select all counters
counters.forEach(counter => {
    // Set counter values to zero
    counter.innerText = 0;
    // Set count variable to track the count
    let count = 0;

    // update count function
    function updateCount() {
        // Get counter target number to count to
        const target = parseInt(counter.dataset.count);
        // As long as the count is below the target number
        if (count < target) {
            count += 5;
            // Set the counter text to the count
            counter.innerText = count + "+";
            // Reapeat this every 10 ms
            setTimeout(updateCount, 10); // Count Speed
            // And when the target is reached
        } 
        else {
            // Set the counter text to the target number
            counter.innerText = target + "+";
        }
    }
    // Run the function initialy
    updateCount();
});
smoke();
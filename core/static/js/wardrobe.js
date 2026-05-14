const modal = document.getElementById("itemModal");

const openBtn = document.getElementById("openModalBtn");

const closeBtn = document.getElementById("closeModalBtn");


// OPEN MODAL

if(openBtn){

    openBtn.addEventListener("click", () => {

        modal.style.display = "flex";

    });

}


// CLOSE MODAL

if(closeBtn){

    closeBtn.addEventListener("click", () => {

        modal.style.display = "none";

    });

}


// CLOSE OUTSIDE CLICK

window.addEventListener("click", (e) => {

    if(e.target === modal){

        modal.style.display = "none";

    }

});


// DELETE BUTTONS

const deleteButtons = document.querySelectorAll(".delete-btn");

deleteButtons.forEach((button) => {

    button.addEventListener("click", () => {

        const card = button.closest(".card");

        card.style.transform = "scale(0)";

        setTimeout(() => {

            card.remove();

        }, 300);

    });

});
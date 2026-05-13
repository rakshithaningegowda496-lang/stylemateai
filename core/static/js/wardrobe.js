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
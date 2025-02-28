function toggleModal(modalId, action) {
    const modal = document.getElementById(modalId);
    if (action === 'open') {
        modal.style.display = 'block';
        document.body.style.overflow = "hidden";
        modal.dispatchEvent(new Event("show"));
    } else if (action === 'close') {
        modal.style.display = 'none';
        document.body.style.overflow = "auto";
        modal.dispatchEvent(new Event("close"));
    }
}
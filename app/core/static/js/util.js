function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

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

function toTitleCase(str) {
  return str.replace(
    /\w\S*/g,
    text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
  );
}
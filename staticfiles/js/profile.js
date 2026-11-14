// Avatar preview
const avatarInput = document.getElementById("avatarInput");
const avatarPreview = document.getElementById("avatarPreview");

const originalAvatar = avatarPreview.src;

avatarInput.addEventListener("change", function () {
const file = this.files[0];

if (file) {
    if (!file.type.startsWith("image/")) {
    alert("Iltimos, faqat rasm faylini tanlang!");
    this.value = "";
    return;
    }

    const reader = new FileReader();

    reader.onload = function (e) {
        avatarPreview.src = e.target.result;
    };

    reader.readAsDataURL(file);
}
});

function resetAvatar() {
    avatarPreview.src = originalAvatar;
    avatarInput.value = "";
}

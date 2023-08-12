const imageInput = document.querySelector('.image-url');
const previewImage = document.querySelector('.search-img-preview img');

imageInput.addEventListener('input', () => {
  const imageUrl = imageInput.value;

  const img = new Image();
  img.onload = function() {
    previewImage.src = this.src;
  };
  img.onerror = function() {
    previewImage.src = 'https://raw.githubusercontent.com/l4wio/dota2-emoji-nickname/master/img/dc.gif';
  };
  img.src = imageUrl;
});
document.addEventListener('DOMContentLoaded', function () {
  var input = document.querySelector('#id_image');
  if (!input) return;

  var preview = document.createElement('img');
  preview.id = 'live-image-preview';
  preview.style.cssText = 'max-width:220px;border-radius:10px;margin-top:12px;display:none;border:1px solid #E6ECF5;';
  input.parentNode.appendChild(preview);

  var hint = document.createElement('div');
  hint.textContent = 'Предпросмотр выбранного файла:';
  hint.style.cssText = 'font-size:12px;color:#7386A8;margin-top:10px;display:none;';
  input.parentNode.insertBefore(hint, preview);

  input.addEventListener('change', function (e) {
    var file = e.target.files && e.target.files[0];
    if (!file) {
      preview.style.display = 'none';
      hint.style.display = 'none';
      return;
    }
    var reader = new FileReader();
    reader.onload = function (ev) {
      preview.src = ev.target.result;
      preview.style.display = 'block';
      hint.style.display = 'block';
    };
    reader.readAsDataURL(file);
  });
});
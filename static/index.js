 const fileInput = document.querySelector('#file');
 const progress = document.querySelector('#progress');

 fileInput.addEventListener('change', (e) => {
     const file = e.target.files[0];
     const formData = new FormData();
     formData.append('file', file);

     fetch('/upload', {
         method: 'POST',
         body: formData
     }).then(response => {
         // Lógica para manejar la respuesta del servidor
     }).catch(error => {
         // Lógica para manejar errores
     });
 });

 // Simulación de progreso de carga
 let progressValue = 0;
 setInterval(() => {
     if (progressValue < 100) {
         progressValue += 10;
         progress.value = progressValue;
     }
 }, 500);
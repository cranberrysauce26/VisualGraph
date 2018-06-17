// Check for the various File API support.
if (window.File && window.FileReader && window.FileList && window.Blob) {
    // Great success! All the File APIs are supported.
} else {
    alert('The File APIs are not fully supported in this browser.');
}
var form = document.getElementById('file-form');
var fileSelect = document.getElementById('file-select');
var uploadButton = document.getElementById('upload-button');

form.onsubmit = function(event) {
    event.preventDefault();
    uploadButton.innerHTML = 'Uploading...';
    if (fileSelect.files.length == 0){
        uploadButton.innerHTML = 'Upload';
        return;
    }
    var file = fileSelect.files[0];
    if (!file.type.match('text/x-python')){
        alert('Error: You must upload a python file');
        uploadButton.innerHTML = 'Upload';
        return;
    }
    var reader = new FileReader();
    reader.readAsText(file);
    reader.onload = function(e) {
        editor.setValue(reader.result);
        uploadButton.innerHTML = 'Upload';
    };
}

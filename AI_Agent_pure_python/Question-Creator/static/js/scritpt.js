
// Get references to HTML elements
let result = document.getElementById('result');
let loader = document.getElementById('loader'); // loader, section while processing the pdf
let download = document.getElementById('download'); // download section
let viewPdf = document.getElementById('view-pdf'); // to view the uploaded pdf
let downloadBtn = document.getElementById('download-btn'); // download button

// When the document is ready, set up the click event handler for the upload button

$(document).ready(function () {
    $("#upload-btn").click(async function (event) {
        // stops the form from submitting and reloading the page when the "Generate Q&A" button is clicked.
        event.preventDefault(); 
        const formData = new FormData();
        const fileInput = document.getElementById('pdf-file') ;  
        var file = fileInput.files[0];           
        
        formData.append('pdf_file', file);
        formData.append('filename', file.name)
        let response = await fetch('/upload', {
            method: "POST",
            body: formData                
        });                
        processUploadResponse(response);  
    });
});

async function processUploadResponse(response){
    switch (response.status) {
        case 400:  
            Swal.fire({
                icon: 'error',
                title: 'Oops!!!',
                text: "Sorry, Couldn't be able to upload your pdf!!!",
                confirmButtonColor: "#15011d"
            }).then(function() {
                window.location.reload();
            });
            break;
        case 200:                 
            var json = await response.json();
            if (json.msg == "error") {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops!',
                    text: 'Maximum number of pages exceeded.',
                    confirmButtonColor: "#545454"
                }).then(function() {
                    window.location.reload();
                });
            }else {
                result.style.display = "block";
                loader.style.display = "block";
                download.style.display = "none";
                viewPdf.setAttribute('src', "../"+json.pdf_filename)
                viewPdf.setAttribute('preload', 'auto');
                const formData = new FormData();
                formData.append('pdf_filename', json.pdf_filename)
                fetch('/analyze', {
                    method: "POST",
                    body: formData                
                }).then(processAnalyzeResponse)  
            }
            
            break;
        default:
            Swal.fire({
                icon: 'error',
                title: 'Oops!!!',
                text: "There is a "+response.status+" error. Please contact admin for support.",
                confirmButtonColor: "#15011d"
            }).then(function() {
                window.location.reload();
            });
    }
}

async function processAnalyzeResponse(response){            
    switch (response.status) {
        case 400:  
            Swal.fire({
                icon: 'error',
                title: 'Oops!!!',
                text: "Sorry, Couldn't analyze your pdf!!!",
                confirmButtonColor: "#15011d"
            }).then(function() {
                window.location.reload();
            });
            break;
        case 200:                     
            loader.style.display = "none";
            download.style.display = "block";
            var json = await response.json();
            downloadBtn.setAttribute('href', "../"+json.output_file)
            break;
        default:
            Swal.fire({
                icon: 'error',
                title: 'Oops!!!',
                text: "There is a "+response.status+" error. Please contact admin for support.",
                confirmButtonColor: "#15011d"
            }).then(function() {
                window.location.reload();
            });
    }
}

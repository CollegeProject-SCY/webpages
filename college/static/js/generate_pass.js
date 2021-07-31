window.onload = function () {
    document.getElementById("download")
        .addEventListener("click", () => {
            const pass = this.document.getElementById("pass");
            console.log(pass);
            console.log(window);
            var opt = {
                
                margin: 1,
                filename: 'myfile1.pdf',
                image: { type: 'jpeg', quality: 1.5 },
                html2canvas: { scale:2},
                jsPDF: { unit: 'in', format: 'letter', orie1ntation: 'portrait' }
            };
            html2pdf().from(pass).set(opt).save();
        })
}
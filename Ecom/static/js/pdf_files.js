$("#download-list-products").on("click", function (){
    $.ajax({
    url : 'display-product/',
    method : 'GET',
    success: function(data){

            var doc = new jsPDF();
            doc.text('Liste des produits', 10, 10);
            doc.autoTable({html: '#export_to_pdf'});
            doc.save('liste-prosuits.pdf');
            doc.setPageSize('a4');
            doc.output('dataurlnewwindow');

        }
    })
})


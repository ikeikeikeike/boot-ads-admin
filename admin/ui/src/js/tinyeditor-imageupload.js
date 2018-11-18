'use strict';

(() => {

let $modal = null;

tinymce.PluginManager.add("imageupload",
  function(e){
    e.addCommand("imageupload",
      function() {
        $modal.modal({})  //e.execCommand("mceInsertContent",!1,"<hr />")
      }
    ),
    e.addButton("imageupload", {
      icon: "image",
      tooltip: "画像の管理",
      cmd: "imageupload"
    }),
    e.addMenuItem("imageupload", {
      icon: "image",
      text: "画像の管理",
      cmd:  "imageupload",
      context: "insert"
    })
  }
)


$(() => {


const modalfun = (data) => {
  $.noConflict();
  $('body').append(data);

  $modal            = $(".imageupload-modal");
  const $table      = $("#imageupload-library-content table");
  const initEvent   = (opt) => {
    $table.find('tbody').on('click', 'tr', function() {
      const $this = $(this)
      insertContent(
        $this.find('img').attr('src'),
        $this.find('[name=name]').text()
      )

      $modal.modal('toggle');
    })
  }

  const insertContent = (src, filename) => {
    const img = `<img src="${src}" alt="${filename}" />`
    tinymce.activeEditor.insertContent(img)
  }

  // init datatable
  const $dataTable = $table.DataTable({
    bFilter: true, bLengthChange: false,
    fnDrawCallback: opt => initEvent(opt) // initevent
  })

  const myDropzone = new Dropzone("#mydropzone", {
    url: $("#mydropzone").data('url'),
    maxFilesize: 30,
    maxFiles: 50,
    parallelUploads: 50,
    autoProcessQueue: true,
    uploadMultiple: true,
    thumbnailWidth: false,
    thumbnailHeight: false,
    previewsContainer: false,
    previewTemplate: false,
    createImageThumbnails: false,
    acceptedFiles: 'image/jpeg, image/png, image/gif',
    headers: {'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')},
    init: function() {

      const addRow = (src, file) => {
        const row = [
          `<img src="${src}" alt="${file.name}" width="100" height="75" />`,
          file.name, file.type, file.size
        ]

        $dataTable.row.add(row).draw()
        insertContent(src, file.name)
      }

      this.on('dragenter', function(e) {
        this.element.classList.add( "dz-drag-hover" )
      })
      this.on('dragend',   function(e) {
        this.element.classList.remove('dz-drag-hover')
      })
      this.on('dragleave', function(e) {
        this.element.classList.remove('dz-drag-hover')
      })

      this.on("successmultiple", function(files) {
        const names = files.map(f => f.name).join(', ')
        alert(`Successful upload image: ${names}`)

        $modal.modal('toggle')
      })

      // this.on("maxfilesexceeded", function(file) { this.removeFile(file) })

      this.on("error", function (file, msg) {
        if (!file.accepted) this.removeFile(file)
        alert(`Failed to upload image: ${msg}`)
      })

      this.on("success", function(file, res) {
        addRow(res.paths.pop(), file)
      })
    }
  })

}


$.ajax({url: '/post/imageform', type: 'GET'})
  .done(data => {
    modalfun(data)
  })
  .fail(data => {}).always(data => {});
});


})()

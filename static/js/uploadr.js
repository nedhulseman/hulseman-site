
/******************************************************************************
 * HTML5 Multiple File Uploader Demo                                          *
 ******************************************************************************/

// Constants
var MAX_UPLOAD_FILE_SIZE = 1024*1024; // 1 MB
var UPLOAD_URL = "/registerRecipe/";
var NEXT_URL   = "/files/";

// List of pending files to handle when the Upload button is finally clicked.
var PENDING_FILES  = [];


$(document).ready(function() {
    // Set up the drag/drop zone.
    initDropbox();

    // Set up the handler for the file input box.
    $("#file-picker").on("change", function() {
        handleFiles(this.files);
    });
    // Handle the submit button.
    $("#upload-button").on("click", function(e) {
        // If the user has JS disabled, none of this code is running but the
        // file multi-upload input box should still work. In this case they'll
        // just POST to the upload endpoint directly. However, with JS we'll do
        // the POST using ajax and then redirect them ourself when done.
        console.log("subbmit button clicked!");
        e.preventDefault();
        doUpload();
    })
});


function doUpload() {
    $("#progress").show();
    var $progressBar   = $("#progress-bar");

    // Gray out the form.
    $("#upload-form :input").attr("disabled", "disabled");

    // Initialize the progress bar.
    $progressBar.css({"width": "0%"});

    // Collect the form data.
    fd = collectFormData();
    for(var pair of fd.entries()) {
          console.log(pair[0]+ ', '+ pair[1]);
     }


    // Attach the files.
    for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
        // Collect the other form data.
        fd.append("file", PENDING_FILES[i]);
    }

    for(var pair of fd.entries()) {
       console.log(pair[0]+ ', '+ pair[1]);
    }

    // Inform the back-end that we're doing this over ajax.
    fd.append("__ajax", "true");
    
    var xhr = $.ajax({
        xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                xhrobj.upload.addEventListener("progress", function(event) {
                    var percent = 0;
                    var position = event.loaded || event.position;
                    var total    = event.total;
                    if (event.lengthComputable) {
                        percent = Math.ceil(position / total * 100);
                    }

                    // Set the progress bar.
                    $progressBar.css({"width": percent + "%"});
                    $progressBar.text(percent + "%");
                }, false)
            }
            return xhrobj;
        },
        url: UPLOAD_URL,
        method: "POST",
        contentType: false,
        processData: false,
        cache: false,
        data: fd,
        success: function(data) {
            
          console.log('ready to jsonify'); 
	   $progressBar.css({"width": "100%"});
	  /*
            data = JSON.parse(data);
	   

            // How'd it go?
            if (data.status === "error") {
                // Uh-oh.
                window.alert(data.msg);
                $("#upload-form :input").removeAttr("disabled");
                return;
            }
            else {
                // Ok! Get the UUID.
                var uuid = data.msg;
                window.location = NEXT_URL + uuid;
            }*/
            
            console.log("I am guessing it doesnt make it here?");
            window.location ='/search-recipes';
        },
	error: function(requestObject, error, errorThrown, data){
		console.log("ERROR THROWN");
		console.log(errorThrown);
		console.log(error);
	},
    });
}


function collectFormData() {
    // Go through all the form fields and collect their names/values.
    var fd = new FormData();

    $("#upload-form :input").each(function() {
        var $this = $(this);
        var name  = $this.attr("name");
        var type  = $this.attr("type") || "";
        var value = $this.val();
        console.log(name);
        console.log(value);
        // No name = no care.
        if (name === undefined) {
            return;
        }

        // Skip the file upload box for now.
        if (type === "file") {
            return;
        }

        // Checkboxes? Only add their value if they're checked.
        if (type === "checkbox" || type === "radio") {
            if (!$this.is(":checked")) {
                return;
            }
        }

        fd.append(name, value);
        console.log("incremental fd: ", Object.keys(fd));
        console.log('a', fd.get('a'))
    });
    for(var pair of fd.entries()) {
  	 console.log('entry: ', pair[0]+ ', '+ pair[1]);
     }
    console.log('final fd', fd);
    return fd;
}


function handleFiles(files) {
    // Add them to the pending files list.
    for (var i = 0, ie = files.length; i < ie; i++) {
        PENDING_FILES.push(files[i]);
    }
}


function initDropbox() {
    var $dropbox = $("#dropbox");

    // On drag enter...
    $dropbox.on("dragenter", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).addClass("active");
    });

    // On drag over...
    $dropbox.on("dragover", function(e) {
        e.stopPropagation();
        e.preventDefault();
    });

    // On drop...
    $dropbox.on("drop", function(e) {
        e.preventDefault();
        $(this).removeClass("active");

        // Get the files.
        var files = e.originalEvent.dataTransfer.files;
        handleFiles(files);

        // Update the display to acknowledge the number of pending files.
        $dropbox.text(PENDING_FILES.length + " files ready for upload!");
    });

    // If the files are dropped outside of the drop zone, the browser will
    // redirect to show the files in the window. To avoid that we can prevent
    // the 'drop' event on the document.
    function stopDefault(e) {
        e.stopPropagation();
        e.preventDefault();
    }
    $(document).on("dragenter", stopDefault);
    $(document).on("dragover", stopDefault);
    $(document).on("drop", stopDefault);
}

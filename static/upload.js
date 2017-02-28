document.addEventListener("DOMContentLoaded", function (event) {
  // We can attach the `fileselect` event to all file inputs on the page
  $(document).on('change', ':file', function() {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
  });

  // We can watch for our custom `fileselect` event like this --leave this as jquery
      $(':file').on('fileselect', function(event, numFiles, label) {
        // could re-write below without jquery
          var input = $(this).parents('.input-group').find(':text'),
              log = numFiles > 1 ? numFiles + ' files selected' : label;

          if( input.length ) {
              input.val(log);
          } else {
              if( log ) alert(log);
          }
  });
  var button = document.getElementById('upload');
  var terms = document.getElementById('terms');

  // Disable the button on initial page load
  button.disabled = true;

  //add event listener
  terms.addEventListener('change', function(event) {
      button.disabled = !terms.checked;
      document.getElementById('termsConditionsDiv').style.display = "none";
  });
});


function showTermsConditionsDiv(evt) {
    document.getElementById('termsConditionsDiv').style.display = "block";
}
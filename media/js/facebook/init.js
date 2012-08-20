$(document).ready(function(){
  // Set initial preview state if any form options are pre-checked
  var style = $(":radio[name='style']:checked").attr("data-image");
  $("#banner").attr("src", "/media/img/facebook/banners/"+style+".png");
  $(":radio[name='style']:checked").parents("label").addClass("selected");
  
  // Show profile image preview if the option is pre-checked, or else hide
  if ($("#profile-img").is(":checked")) {
    $("#userpic").show();
  }
  else {
    $("#userpic").hide();
  }
  
  // Hide newsletter options
  $("#newsletter .options").hide();
});

  // Swap the preview image as the selection changes
  $(":radio[name='style']").change(function(){
    var style = $(this).attr("data-image");
    $("#banner").attr("src", "/media/img/facebook/banners/"+style+".png");
    $(":radio[name='style']").parents("label").removeClass("selected");
    $(this).parents("label").addClass("selected");
  });

  // Show the note
  $(".note-link").click(function(){
    $("#ad-note").fadeToggle('fast').removeAttr("aria-hidden");
    return false;
  });
  
  // Hide note when anything else is clicked
  $(document).bind('click', function(e) {
    var $clicked = $(e.target);
    if ($("#ad-note:visible") && ! $clicked.hasClass("note-link")) {
      $("#ad-note").fadeOut('fast').attr("aria-hidden", "true");
    }
  });
  
  // or gets focus
  $("a, input, textarea, button, :focus").bind('focus', function(e) {
    var $focused = $(e.target);
    if ($("#ad-note:visible") && ! $focused.hasClass("note-link")) {
      $("#ad-note").fadeOut('fast').attr("aria-hidden", "true");
    }
  });
  
  // Toggle the profile image preview when the option changes
  $("#profile-img").change(function(){
    if ($(this).is(":checked")) {
      $("#userpic").fadeIn(100);
    }
    else {
      $("#userpic").fadeOut(100);
    }
  })
  
  // Show/hide the account linking form
  $(".not-linked a").click(function(){
    $("#link-account").slideToggle('fast');
    $(this).blur();
    return false;
  });
  
  // Show newsletter options
  $("#news-email").focus(function(){
    $("#newsletter .options").slideDown('fast');
  });
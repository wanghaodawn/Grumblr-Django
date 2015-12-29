
function populateList() {
  console.log("Begin populateList")
    $.get("/get_posts")
      .done(function(data) {
          var list = $("#posts-list");
          list.data('max_entry', data['max_entry']);
          list.html('');
          console.log(data.posts.length);
          for (var i = 0; i < data.posts.length; i++) {
              post = data.posts[i];
              var new_post = $(post.html);
              list.append(new_post);
              var comment_list = $("#comment_list_" + post.id);
              console.log(comment_list);
              var comments = post.comments;

              for (var j = 0; j < comments.length; j++) {
                var comment = comments[j];
                var new_comment = $(comment.html);
                comment_list.append(new_comment);
              }
          }
    });
  console.log("End populateList")
}


// function addPost(){
//     var postField = $("#inputPost");
//     $.post("/global_page", {post: postField.val()})
//       .done(function(data) {
//           getUpdates();
//           postField.val("").focus();
//       });
// }


function addComment(){
    console.log("Begin addComment")
    var post_id = parseInt($(this).attr('btn-id'));
    var commentField = $("#comment_field_" + post_id);
    $.post("/add_comment/" + post_id, {comment: commentField.val()})
      .done(function(data) {
        var comment_list = $("#comment_list_" + post_id);
        comment = $(data.comments[0].html);
        comment_list.append(comment);
        commentField.val("").focus();
      });
    console.log("End addComment")
}


function getUpdates() {
    console.log("Begin getUpdates")
    var list = $("#posts-list");
    var max_entry = list.data("max_entry");
    $.get("/get_changes/" + max_entry)
      .done(function(data) {
          list.data('max_entry', data['max_entry']);
          console.log(max_entry);
          //console.log(data.posts.length);
          for (var i = 0; i < data.posts.length; i++) {
            var post = data.posts[i];
            var new_post = $(post.html);
            list.prepend(new_post);
          }
      });
    console.log("End getUpdates")
}


$(document).ready(function () {
  // Add event-handlers
  //$("#add-btn").click(addPost);
  //$("#inputPost").keypress(function (e) { if (e.which == 13) addPost(); } );
  $(document).on("click", "#add_comment_button", addComment);

  // Set up with initial DB posts and DOM data
  populateList();
  //$("#inputPost").focus();

  // Periodically refresh every 5 seconds
  window.setInterval(getUpdates, 5000);

  // CSRF set-up copied from Django docs
  function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});

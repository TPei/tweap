{% load i18n %}
$(document).ready(function(){
    newMembers = new Members();
    $('<p id="project_icon"><i id="projectIcon" name="projectIcon" class="{{ project.icon|default:"fa fa-folder-open-o" }} project_icon" data-toggle="modal" data-target="#projectIconModal"></i> {% trans "Click icon to change it" %}</p>').insertAfter('label[for=id_icon]');
    $('label[for=id_icon]').attr('for', 'projectIcon');

    projectIconClass = '{{ project.icon|default:"fa fa-folder-open-o" }}'
    projectIconClass = "." + projectIconClass.split(" ")[1];
    console.log(projectIconClass);
    active = $('#projectIconModal').find(projectIconClass);
    console.log(active)
    $(active).addClass('project_icon_chosen');
});

//Adds click listener to the icons in modal
$(document).on('click', '.project_icon_choose', function() {
    $('.project_icon_chosen').removeClass('project_icon_chosen');
    $(this).addClass('project_icon_chosen');
    var icon_class = $('.project_icon_chosen').attr('id');
    $('#projectIcon').removeClass().addClass('project_icon ' + icon_class);
    $('input[name=icon]').val(icon_class);
    $('#projectIconModal').modal('hide');
});

//Adds new Inputfields
$(document).on('click', '.addUserButton', function() {

    // if input is empty, prevent user adding
    if(!$(this).prev().val()) {
        // focus on empty field and give error message
        $(this).prev().focus();
        $(this).prev().attr("placeholder", "{% trans 'Username or eMail' %}");
        $(this).parent().parent().addClass('has-error');
    }
    else {
        addMemberInput();
    }
});

// if input is there add new field, make old field uneditable and removable
function addMemberInput(){
    $('.addUserButton').addClass('removeUserButton');
    $('.addUserButton').removeClass('addUserButton');

    $('.removeUserButton').children().first().removeClass('glyphicon-plus-sign');
    $('.removeUserButton').children().first().addClass('glyphicon-minus-sign');

    $('.removeUserButton').prev().attr("disabled", true);

    $('.removeUserButton').parent().parent().removeClass('has-error');

    $('#newInputs').prepend(
        "<div class='form-group'><div class='input-group date'><input id='users' type='text' placeholder='{% trans "Username or eMail" %}' class='form-control member'><span class='input-group-addon addUserButton focus-pointer'><i class='glyphicon glyphicon-plus-sign'></i></span></div></div>"
    );

    $('#suggestions').remove();
    $('#newInputs div:first-child').after("<div id='suggestions'></div>");

    $('.removeUserButton').click(function(){
        $(this).parent().parent().remove();
    })
}

//Ajax-Request for Usersuggestions
$(document).on('keyup', '#users', function(){
    typedText = (this).value
    //AJAX-Request:
    data = {search:typedText};
    $.get("{% url 'user_management:user_suggestion' %}", data, function(output){
        manageUserSuggestionAjaxRequest(output)
    })

});

//Puts the ID of an Suggestionelement into the value of the first inputelement in #newInputs and adds a new inputField
$(document).on('click', '.suggestion', function() {
    suggestionId = $(this).attr('id');
    firstInput = $('#newInputs').find('input[type=text]').filter(':visible:first')
    firstInput.val(suggestionId);
    addMemberInput();
});

/*
is called on an AjaxRequest - deletes all #suggestion-HTMLElements
and calls addSuggestionsToContent. Adding of the HTMLElements is done for each
User inside the data-Array.
 */
function manageUserSuggestionAjaxRequest(data){
    $('#suggestions').empty();
    for(i=0;i<data.length;i++){
        addSuggestionToContent(data[i]);
    }
}

/*
adds #suggestions-HTMLElements over the inputs.
 */
function addSuggestionToContent(id) {
    $('#suggestions').append(
        '<h3 class="suggestion" id="' + id + '"><span class="label label-info focus-pointer">' + id + '</span></h3>'
    );
}

//Adds Userarray-JSONString to Hiddenfield
function insertHiddenValues(){
    inputMemberArr = $("#newInputs .member");

    for(i=0;i<inputMemberArr.length;i++){
        newMembers.addUser(inputMemberArr.eq(i).val());
    }

    $('#hiddenValues').val(newMembers.getUsersString());
}

//Object is initialized on the very Beginning of this document
var Members = function(){
    this.Users = new Array();

    //Adds new Userstring to Users-Array (Attribute)
    this.addUser = function(added_user){
        this.Users.push(added_user)
    }

    //Stringifies the Users-Arrayattribute and returns it
    this.getUsersString = function() {
        return JSON.stringify(this.Users);
    }
}
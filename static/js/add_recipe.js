
  function getRecipeSRC() {
    if (document.getElementById("url-src-recipe").checked == true) {
      document.getElementById("url-recipe-input").style.display ='flex';
      document.getElementById("upload-recipe-input").style.display ='none';
    }
    else {
      document.getElementById("url-recipe-input").style.display ='none';
      document.getElementById("upload-recipe-input").style.display ='flex';
    }
  }
  getRecipeSRC();
  function getImgSRC() {
    if (document.getElementById("url-src-img").checked == true) {
      document.getElementById("url-img-input").style.display ='flex';
      document.getElementById("upload-img-input").style.display ='none';
    }
    else {
      document.getElementById("url-img-input").style.display ='none';
      document.getElementById("upload-img-input").style.display ='flex';
    }
  }
  getImgSRC();


  if (document.readyState == 'complete') {
    console.log('complete?');
    var element = document.getElementById('form-tags-1_tagsinput');
    element.addEventListener('DOMSubtreeModified', addIngredientsTable);
} else {
    document.onreadystatechange = function () {
        console.log('on ready state');
        if (document.readyState === "complete") {
          setTimeout(function() {
            var element = document.getElementById('form-tags-1_tagsinput');
            element.addEventListener('DOMSubtreeModified', addIngredientsTable);
          }, 200);
        }
    }
}


function getDrpdwn(id_name){
  ingred_measure_drpdwn = `<div class="btn-group">
            <button type="button" id=`+id_name+'-drpdwn'+` onClick="addClickAction()" class="drpdwn btn btn-danger dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Action
            </button>
            <div id=`+id_name+'-drpdwn_div'+` class="dropdown-menu">
              <a class="dropdown-item" >Action</a>
              <a class="dropdown-item">Another action</a>
              <a class="dropdown-item" >Something else here</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" >Separated link</a>
            </div>
          </div>`;
  return ingred_measure_drpdwn;
};

function addIngredientsTable() {
    console.log('ran');
    var ingredient_tags = document.getElementsByClassName('tag-text');

    // get ingredients in tag
    ingredients_tagged = [];
    for (var i=0; i<ingredient_tags.length; i++) {
      ingredients_tagged.push(ingredient_tags[i].textContent);
    }

    // get ingredients currently in table
    var ingredient_rows = document.getElementsByClassName('ingredient_tags');
    ingredients_table = [];
    for (var i=0; i<ingredient_rows.length; i++) {
      ingredients_table.push(ingredient_rows[i].getElementsByTagName('td')[0].textContent);
    }
    new_items = [];

    //in tags and not in table (added)
    for (var i=0; i<ingredients_tagged.length; i++) {
      if( ! ingredients_table.includes(ingredients_tagged[i])) {
        new_items.push(ingredients_tagged[i]);
      };
    }
    // in table and not in tags (removed)
    rm_items = [];
    for (var i=0; i<ingredients_table.length; i++) {
      if( ! ingredients_tagged.includes(ingredients_table[i])) {
        rm_items.push(ingredients_table[i]);
      }
    }



    /*
    ingred_measure_drpdwn =`<div class="dropdown">
                              <a aria-expanded="false" aria-haspopup="true" role="button" data-toggle="dropdown" class="dropdown-toggle" href="#">
                                <span id="selected">Chose option</span><span class="caret"></span></a>
                            <ul class="dropdown-menu">
                              <li><a href="#">Option 1</a></li>
                              <li><a href="#">Option 2</a></li>
                              <li><a href="#">Option 3</a></li>
                              <li><a href="#">Option 4</a></li>
                            </ul>
                          </div>`;
    */
    //ingred_measure_drpdwn = '<div class="dropdown-menu"><a class="dropdown-item" href="#">Action</a><a class="dropdown-item" href="#">Another action</a><a class="dropdown-item" href="#">Something else here</a></div>';
    // Add new items to tables
    for (var i=0; i<new_items.length; i++){
      row = "<tr id='"+new_items[i]+"' class='ingredient_tags' ><td>"+new_items[i]+"</td><td></td></tr>";
      var table = document.getElementById("ingredients-table").getElementsByTagName('tbody')[0];
      var row = table.insertRow(0);
      row.setAttribute('id', new_items[i]);
      row.setAttribute('class', 'ingredient_tags');
      var ing = row.insertCell(0);
      var drp = row.insertCell(1);
      ing.innerHTML = new_items[i];
      drp.innerHTML = getDrpdwn(new_items[i]);
    };
    // Remove items from tables
    for (var i=0; i<rm_items.length; i++) {
      console.log(rm_items);
      document.getElementById(rm_items[i]).remove();
    };
  }

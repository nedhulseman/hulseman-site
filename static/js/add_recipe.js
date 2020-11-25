
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




  function addIngredientsTable() {
    console.log('ran');
    var ingredient_tags = document.getElementsByClassName('tag-text');

    // get ingredients in tag table
    ingredients_tagged = [];
    for (var i=0; i<ingredient_tags.length; i++) {
      ingredients_tagged.push(ingredient_tags[i].textContent);
    }

    // get ingredients currently in table
    var ingredient_rows = document.getElementsByClassName('ingredient_tags');
    ingredients_table = [];
    for (var i=0; i<ingredient_rows.length; i++) {
      ingredients_table.push(ingredient_rows[i].textContent);
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
        rm.push(ingredients_table[i]);
      }
    }

    for (var i=0; i<new_items.length; i++){
      row = "<tr id='"+new_items[i]+"' class='ingredient_tags' ><td>"+new_items[i]+"</td><td></td></tr>";
      var table = document.getElementById("ingredients-table").getElementsByTagName('tbody')[0];
      var row = table.insertRow(0);
      row.setAttribute('id', new_items[i]);
      row.setAttribute('class', 'ingredient_tags');
      var ing = row.insertCell(0);
      var drp = row.insertCell(1);
      ing.innerHTML = new_items[i];
      drp.innerHTML = "";
    }

  }

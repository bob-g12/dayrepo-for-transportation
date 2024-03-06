var i = 1 ;
function addForm() {
  var content_area = document.getElementById("form_area");
  var clone_element = content_area.cloneNode(true);
  clone_element.id = i;
  alert("工程を追加しますか？");
  content_area.after(clone_element);
  i++ ;
}
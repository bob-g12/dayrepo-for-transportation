let i = 1 ;
const addForm = () => {
  let content_area = document.getElementById("form_area");
  let content_clone = document.getElementById("add_space");
  let clone_element = content_area.cloneNode(true);
  clone_element.id = i;
  alert("工程を追加しますか？");
  content_area.reset();
  content_clone.before(clone_element);
  i++ ;
}
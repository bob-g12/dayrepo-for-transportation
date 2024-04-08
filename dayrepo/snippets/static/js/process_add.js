const addForm = () => {
  let count = Number(document.getElementById("count").innerHTML);
  const limit = 6;
  if (count == limit){
    alert("これ以上増やせません")
    return
  }
  alert("工程を追加します");
  count += 1;
  const content_area = document.getElementById("form_area");
  let clone_element = content_area.cloneNode(true);
  let content_clone = document.getElementById("add_space");
  const content_count = content_area.childElementCount;
  const bool_select = 8;
  const not_select = 10;
  for (let i=0; i<content_count; i++){
    if (i != bool_select && i <= not_select){
      clone_element.children[i].children[1].value="";
    }
    else if (i == bool_select){
      clone_element.children[i].children[1].checked="";
    }
  }
  content_clone.before(clone_element)
  document.getElementById("count").innerHTML = count;
  clone_element.id = now_count;
}
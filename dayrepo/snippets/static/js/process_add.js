const limit = 6;
let bool_select = 8;
let not_select = 10;
const addForm = () => {
  const count = Number(document.getElementById("count").innerHTML);
  let now_count = count + 1;
  if (now_count <= limit){
    alert("工程を追加します");
    const content_area = document.getElementById("form_area");
    let clone_element = content_area.cloneNode(true);
    let content_clone = document.getElementById("add_space");
    const content_count = content_area.childElementCount;
    for (let i=0; i<content_count; i++){
      if (i != bool_select && i <= not_select){
        clone_element.children[i].children[1].value="";
      }
      else if (i == bool_select){
        clone_element.children[i].children[1].checked="";
      }
    }
    content_clone.before(clone_element)
    document.getElementById("count").innerHTML = now_count;
    clone_element.id = now_count;
  }
  else {
    alert("これ以上増やせません");
  }
}
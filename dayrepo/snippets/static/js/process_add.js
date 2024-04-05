let i = 1 ;
const addForm = () => {
  let count = Number(document.getElementById("count").innerHTML);
  let now_count = count + i;
  if (now_count <= 6){
    alert("工程を追加しますか？",);
    let content_area = document.getElementById("form_area");
    let clone_element = content_area.cloneNode(true);
    let content_clone = document.getElementById("add_space");
    let content_count = content_area.childElementCount;
    for (let i=0; i<content_count; i++){
      if (i != 8 && i <= 10){
        clone_element.children[i].children[1].value="";
      }
      else if (i == 8){
        clone_element.children[i].children[1].checked="";
      }
    }
    content_clone.before(clone_element)
    document.getElementById("count").innerHTML = now_count;
    clone_element.id = now_count;
    i++ ;
  }
  else {
    alert("これ以上増やせません",);
  }
}
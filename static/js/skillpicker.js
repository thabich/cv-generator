// Vanilla JS MultiSelect Skillpicker enhancements
document.addEventListener("DOMContentLoaded", function(){
  document.querySelectorAll("select[multiple]").forEach(sel=>{
    sel.addEventListener("change", function(){
      // Optional: Validation
      if(sel.selectedOptions.length>10){
        alert("Max 10 Skills pro Task erlaubt");
        sel.selectedOptions[sel.selectedOptions.length-1].selected=false;
      }
    });
  });
});

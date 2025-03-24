document.addEventListener("DOMContentLoaded", function(event) { 
    let inputs = document.getElementsByName("sentiment_filter");
    for(let input of inputs) {
        input.addEventListener("input", (ev) => {
            let fieldset_div = document.getElementById("id_sentiments");
            for(let child_div of fieldset_div.getElementsByTagName("div")) {
                let label = child_div.getElementsByTagName("label")[0];
                let label_text = label.textContent;
                let input_text = input.value.trim().toUpperCase();
                if(input_text.length === 0) {
                    child_div.style.display = "";
                } else if(label_text.trim().toUpperCase().indexOf(input_text) >= 0) {
                    child_div.style.display = "";
                } else {
                    child_div.style.display = "none";
                }
            }
        });
    }
  });

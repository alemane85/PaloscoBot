function toggle(source) {
  checkboxes = document.getElementsByName('mycheck');
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}

function valcheckboxes()
{
    var checkboxs=document.getElementsByName("mycheck");
    var okay=false;
    for(var i=0,l=checkboxs.length;i<l;i++)
    {
        if(checkboxs[i].checked)
        {
            okay=true;
            break;
        }
    }
    return okay
}

function formValidation()
    {
        var enable_submit=true;
        var msg=" ";
        if(!(valcheckboxes()))
            {enable_submit=false;}
        if(isNaN(document.getElementById("input_bolla").value) || document.getElementById("input_bolla").value.length<1)
            {enable_submit=false;}
        if(isNaN(Date.parse(document.getElementById("input_data").value)) || document.getElementById("input_data").value.length<1)
            {enable_submit=false;}
        if(enable_submit)
            {
                document.getElementById("btn_submit").disabled = false;
                document.getElementById("btn_submit").className = "btn btn-success";
            }
        else
            {
                document.getElementById("btn_submit").disabled = true;
                document.getElementById("btn_submit").className = "btn btn-secondary";
            }
    }

window.onload = function ()
                    {
                        var enable_submit=false;
                        var btn_submit = document.getElementById("btn_submit");
                        var bolla = document.getElementById("input_bolla");
                        var checkboxs = document.getElementsByName("mycheck");
                        var data = document.getElementById("input_data")
                        btn_submit.disabled = true
                        btn_submit.className = "btn btn-secondary"
                        bolla.onkeyup = formValidation;
                        data.onkeyup = formValidation;
                        for(var i=0,l=checkboxs.length;i<l;i++)
                            {
                                checkboxs[i].onclick = formValidation;
                            }
                    }

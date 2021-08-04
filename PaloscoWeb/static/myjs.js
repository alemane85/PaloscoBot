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
        var t1ck=true;
        var msg=" ";
        if(!(valcheckboxes()))
            {
                t1ck=false;
                msg = msg + "non hai checkbox attive<br>";
            }
        if(isNaN(document.getElementById("input_bolla").value) || document.getElementById("input_bolla").value.length<1)
            {
                t1ck=false;
                msg = msg + "non è un numero<br>";
            }
        if(document.getElementById("t1").value.length < 3 )
            {
                t1ck=false;
                msg = msg + "Your name should be minimun 3 char length<br>";
            }
        if(!document.getElementById("r1").checked && !document.getElementById("r2").checked)
            {
                t1ck=false;
                msg = msg + " Select your Gender<br>";
            }
        if(document.getElementById("s1").value.length < 3 )
            {
                t1ck=false;
                msg = msg + " Select one of the games <br>";
            }
        if(!document.getElementById("c1").checked )
            {
                t1ck=false;
                msg = msg + " You must agree to terms & conditions<br> ";
            }
        //alert(msg + t1ck);
        if(t1ck)
            {
                document.getElementById("btn_submit").disabled = false;
                msg=msg+ " <b> Submit Button is enabled </b>";
            }
        else
            {
                document.getElementById("btn_submit").disabled = true;
                msg=msg+ " <b> Submit Button is disabled </b>";
            }
            // end of if checking status of t1ck variable
            document.getElementById('my_msg').innerHTML=msg;
}

function resetForm(){
document.getElementById("btn_submit").disabled = true;
var frmMain = document.forms[0];
frmMain.reset();
}

window.onload = function ()
                    {
                        var btn_submit = document.getElementById("btn_submit");
                        var btnReset = document.getElementById("btnReset");
                        var t1 = document.getElementById("t1");
                        var r1 = document.getElementById("r1");
                        var r2 = document.getElementById("r2");
                        var s1=document.getElementById("s1");
                        var c1=document.getElementById("c1");
                        var t1ck=false;
                        document.getElementById("btn_submit").disabled = true;
                        t1.onkeyup = formValidation;
                        r1.onclick = formValidation;
                        r2.onclick = formValidation;
                        s1.onclick = formValidation;
                        c1.onclick = formValidation;
                        btnReset.onclick = resetForm;
                    }

class P {
    constructor(text) {
        this.text = text;
    }
}

function callPythonOnChange(element) {
    p = new P($('#report').val());
    var r = "True";
    var oldValue = element.defaultValue;
    var newValue = element.value;
    $.ajax({
        type: 'post',
        url: "/change/",
        dataType: 'json',
        contentType: 'application/json',
        error: function (sd) {
            r = sd['responseText'];
            if (r === "False") {
                element.value = oldValue;
            } else {
                element.defaultValue = newValue;
            }
        },
        data: JSON.stringify(p)
    });
}

function callPythonOnClick(clickid) {
    p = new P(clickid);
    $.ajax({
        type: 'post',
        url: "/communication/",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(p),
        error: function (sd) {
            s = sd['responseText'];
            if (s.includes('Redirect')) {
                if (s.includes('main')) {
                    document.location = "/"
                } else if (s.includes('profile')) {
                    document.location = "/reports/profile"
                } else if (s.includes('custom')) {
                    document.location = "/reports/customization"
                }
            } else {
                alert(s);
                document.location.reload()
            }
        }
    })
}

function callPythonReport() {
    p = new P($('#report').val());
    $.ajax({
        type: 'post',
        url: "/sendreport",
        dataType: "json",
        contentType: 'application/json',
        data: JSON.stringify(p),
        error: function f(sd) {
            s = sd['responseText'];
            if (s === "Save") {
                alert("Your report is saved into the database");
                document.location.reload();
            } else {
                alert("We have an error, please re-log");
                document.location = "/logout";
            }
        }
    });

}

function tellDjango(t) {

    if (t === 0) {
        //TODO : Template
        p = new P($('#template').val());
        $.ajax({
            type: 'post',
            url: "/reports/sendtemplate",
            dataType: "json",
            contentType: 'application/json',
            data: JSON.stringify(p),
            error: function f() {
                alert("Your template has been updated in the database");
                document.location = "/reports/customization";
            }
        });
    } else if (t === 1) {
        //TODO : Default
        p = new P($('#default').val());
        $.ajax({
            type: 'post',
            url: "/reports/sendd",
            dataType: "json",
            contentType: 'application/json',
            data: JSON.stringify(p),
            error: function f() {
                alert("Your default report has been updated in the database");
                document.location = "/reports/customization";
            }
        });
    } else if (t === 2) {
        tellDjango(0);
        tellDjango(1);
    }

}

function toggleDestroy(b) {
    document.getElementById("destroy_account").disabled = b;
}

function del() {
    document.getElementById("destroy_account").disabled = true;
}

function unlock() {
    s = confirm("Are you sure you want to unlock the destroy account button ? ( 7s )");
    console.log(s);
    if (s) {
        console.log("enable");
        toggleDestroy(false);
        setInterval(del, 7000)
    }
}

function destroy() {
    s = confirm("Are you sure you want to destroy your account ?");
    if (s) {
        callPythonOnClick('destroy');
    }
}
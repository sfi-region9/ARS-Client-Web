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
        url: "/reports/change/",
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
        url: "/reports/communication/",
        dataType: 'json',
        contentType: 'application/json',
        error: function (sd) {
            s = sd['responseText'];
            alert(s);
        }
    })
}

function callPythonReport() {
    p = new P($('#report').val());
    $.ajax({
        type: 'post',
        url: "/reports/sendreport",
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
                document.location = "/reports/logout";
            }
        }
    });

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
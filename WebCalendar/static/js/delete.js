function Delete(url) {
    fetch(url, {
    method: "DELETE",
})
.then(res => {
    if (res.ok) { window.location.href = "/event" }
    else { console.log("HTTP request unsuccessful") }
    return res
})
.then(res => res.json())
.then(data => console.log(data))
.catch(error => console.log(error))
}

function Add(url) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url);

    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    let data = `{
    "event": "smth",
    "date": "2022-12-12",
    }`;

    xhr.send(data);
}
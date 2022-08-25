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
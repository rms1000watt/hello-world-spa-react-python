var authenticated = false;

export const PORT = 8111;

export function setAuthenticated(_authenticated) {
    authenticated = _authenticated;
}

export function getAuthenticated() {
    let web_user = getCookie("web_user");
    return Boolean(web_user)
}

export function ajax(payload, url, successCB, errorCB) {
    var request = new Request(url, {
        method: 'POST', 
        mode: 'cors', 
        redirect: 'follow',
        credentials: 'include', 
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
        body: JSON.stringify(payload)
    });

    fetch(request)
    .then((response)=>{return response.json()})
    .then(successCB)
    .catch(errorCB)
}

export function getCookie(name)  {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
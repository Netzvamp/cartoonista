var api_base_url = "/";
var api_endpoints = {
    cartoonists: "cartoonists",
    cartoon: "cartoon"
};

var cartoon = {
    credits: "",
    img: "",
    language: "",
    name: "",
    title: "",
    txt: "",
    website: ""
};
config = {  // The default config
    excluded_cartoonists: [],  // exclude filter
}

var vm = new Vue({
    el: '#cartoonista',
    data: { cartoon: cartoon }
});

async function get_new_cartoon() {
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(config)
    }
    const response = await fetch(api_base_url + api_endpoints.cartoon, requestOptions);
    const data = await response.json();
    cartoon.img = data.img;
}

get_new_cartoon();

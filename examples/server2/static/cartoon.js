// localStorage.setItem('Name', 'somevalue');
// localStorage.getItem('Name');
// localStorage.removeItem('Name');
// localStorage.clear();
// localStorage.length;


let cartoonista = {
    cartoonists: {},
    config: {},
    get_cartoonists: async function () {
        // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
        let cartoonists = await fetch("/rest/cartoons/cartoonists");
        return cartoonists.json();
    },
    init: async function () {
        await cartoonista.get_cartoonists().then(data => {
            cartoonista.cartoonists = data;
        });
        if (typeof(Storage) !== "undefined") {
            if (localStorage.getItem("cartoonista.config")) {
                cartoonista.config = JSON.parse(localStorage.getItem("cartoonista.config"));
            } else {
                // set the default config
                cartoonista.config["cartoonists"] = "all";
                localStorage.setItem('person', JSON.stringify(cartoonista.config));
            }
        } else {
            console.warn("Sorry your browser is to old and has no web storage api. So we can't save your settings :P");
        }
        // building form
        cartoonista.cartoonists.forEach(function (c) {
            let input = document.createElement('input');
            input.type = 'checkbox';
            input.name = c.name;
            input.value = c.name;
            input.id = c.name;
            if (cartoonista.config["cartoonists"] === "all") {
                input.checked = true;
            }
            let label = document.createElement('label')
            label.for = c.name;
            label.innerText = c.name;
            document.getElementById("cartoonista_cartoonists").append(input);
            document.getElementById("cartoonista_cartoonists").append(label);
            document.getElementById("cartoonista_cartoonists").append(document.createElement('br'));
        });
        console.log(cartoonista);
    },
    open_config: function () {
        document.getElementById('cartoonista_config_window').style.display = "block";
    },
    close_config: function () {
        document.getElementById('cartoonista_config_window').style.display = "none";
    },
    resize: function () {
        document.getElementById('image').style.maxHeight = 'none';
        document.getElementById('cartoon').style.transform = 'translate(-50%,0)'
        document.getElementById('cartoon').style.top = 0;
    },
};
cartoonista.init();

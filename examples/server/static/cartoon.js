let cartoonista = {
    api_base_url: "/",
    api_endpoints: {
        cartoonists: "cartoonists",
        cartoon: "cartoon"
    },
    cartoonists: {},
    config: {  // The default config
        excluded_cartoonists: [],  // exclude filter
    },
    get_cartoonists: async function () {
        let cartoonists = await fetch(this.api_base_url + this.api_endpoints.cartoonists);
        return cartoonists.json();
    },
    get_cartoon: async function () {
        let cartoon = await fetch(
            this.api_base_url + this.api_endpoints.cartoon,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify(this.config)
            });
        return cartoon.json();
    },
    init: async function () {
        await this.get_cartoonists().then(data => {
            this.cartoonists = data;
            if (typeof (Storage) !== "undefined") {
                if (localStorage.getItem("cartoonista.config")) {
                    this.config = JSON.parse(localStorage.getItem("cartoonista.config"));
                }
            } else {
                console.warn("Sorry your browser is to old and has no web storage api. So we can't save your settings :P");
            }
            this.render_form();
        });
        await this.new_cartoon();
    },
    new_cartoon: async function () {
        await this.get_cartoon().then(data => {
            let img = document.createElement('img');
            img.src = data.img;
            img.id = "cartoonista_image";
            if (typeof data.txt !== "undefined") {
                img.title = data.txt;
            }
            img.addEventListener("click", this.resize);
            let c = document.getElementById("cartoonista_cartoon");
            if (c.firstChild) {
                c.removeChild(c.firstChild);
            }
            c.append(img);

            if ('txt' in data) {
                document.getElementById("cartoonista_txt").innerHTML =
                    `${data.txt} <a href="${data.website}" target="_blank">&copy; ${data.credits}</a>`;
            } else {
                document.getElementById("cartoonista_txt").innerHTML =
                    `<a href="${data.website}" target="_blank">&copy; ${data.credits}</a>`;
            }
            if ('title' in data) {
                document.getElementById("cartoonista_title").innerHTML = data.title;
            } else { document.getElementById("cartoonista_title").innerHTML = ""; }
            cartoonista.resize_reset();
        })
    },
    render_form: function () {
        this.cartoonists.forEach(function (c) {
            let input = document.createElement('input');
            input.type = 'checkbox';
            input.name = c.name;
            input.value = c.name;
            input.id = c.name;
            if (!cartoonista.config.excluded_cartoonists.includes(c.name)) {
                input.checked = true;
            }
            input.addEventListener('change', cartoonista.config_event, false);
            let label = document.createElement('label')
            label.for = c.name;
            label.innerText = c.credits;
            document.getElementById("cartoonista_cartoonists").append(input);
            document.getElementById("cartoonista_cartoonists").append(label);
            document.getElementById("cartoonista_cartoonists").append(document.createElement('br'));
        });
    },
    config_event: function (event) {
        let t = event.target;

        // prevent no selected cartoonists
        if (!t.checked && cartoonista.config.excluded_cartoonists.length === cartoonista.cartoonists.length - 1) {
            t.checked = true; return;
        }

        if (!t.checked && !cartoonista.config.excluded_cartoonists.includes(t.value)) {
            cartoonista.config.excluded_cartoonists.push(t.value);
        }
        if (t.checked && cartoonista.config.excluded_cartoonists.includes(t.value)) {
            cartoonista.config.excluded_cartoonists.splice(cartoonista.config.excluded_cartoonists.indexOf(t.value), 1);
        }
        localStorage.setItem("cartoonista.config", JSON.stringify(cartoonista.config))
    },
    open_config_modal: function () {
        document.getElementById('cartoonista_config_window').style.display = "flex";
    },
    close_config_modal: function () {
        document.getElementById('cartoonista_config_window').style.display = "none";
    },
    resize: function () {
        let i = document.getElementById('cartoonista_cartoon');
        let img = document.getElementById('cartoonista_image');
        if (img.style.maxHeight !== 'none') {
            i.style.top = "6em";
            i.style.transform = 'translate(-50%,0)';
            img.style.maxHeight = 'none';
            img.style.cursor = 'zoom-out';
        } else {
            cartoonista.resize_reset();
        }
    },
    resize_reset: function () {
        let i = document.getElementById('cartoonista_cartoon');
        let img = document.getElementById('cartoonista_image');
        i.style.top = "50%";
        i.style.transform = 'translate(-50%,-50%)';
        img.style.maxHeight = '78vh';
        img.style.cursor = 'zoom-in';
    }
};
cartoonista.init();

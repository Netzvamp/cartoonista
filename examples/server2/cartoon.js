let cartoonista = {
    cartoonists: {},
    get_cartoonists: async function(){
        // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
        let cartoonists = await fetch("/rest/cartoons/cartoonists");
        return cartoonists.json();
    },
    init: async function () {
        await cartoonista.get_cartoonists().then(data => {
            cartoonista.cartoonists = data;
        });
        console.log(cartoonista.cartoonists);
    },
    open_config: function() {
        document.getElementById('cartoonista_config_window').style.display = "block";
    },
    close_config: function() {
        document.getElementById('cartoonista_config_window').style.display = "none";
    },
    resize: function () {
        document.getElementById('image').style.maxHeight='none';
        document.getElementById('cartoon').style.transform = 'translate(-50%,0)'
        document.getElementById('cartoon').style.top = 0;
    }
};
cartoonista.init();

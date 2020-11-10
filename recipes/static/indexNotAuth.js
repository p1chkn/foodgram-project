const container = document.querySelector('.card-list');
const counterId = document.querySelector('#counter');
const api = new Api(apiUrl);
const header = new Header(counterId);
const configButton = {
    purchases: {
        attr: 'data-out',
        default: {
            class: 'button_style_light-blue',
            text: '<span class="icon-plus button__icon"></span>Добавить в покупки'
        },
        active: {
            class: 'button_style_light-blue-outline',
            text: `<span class="icon-check button__icon"></span> Рецепт добавлен`
        }
    }
}
function addOrUpdateUrlParam(name, value)
                    {
                        var href = window.location.href;
                        var regex = new RegExp("[&\\?]" + name + "=");
                        if(regex.test(href))
                        {
                        regex = new RegExp("([&\\?])" + name + "=\\w+");
                        window.location.href = href.replace(regex, "$1" + name + "=" + value);
                        }
                        else
                        {
                        if(href.indexOf("?") > -1)
                        window.location.href = href + "&" + name + "=" + value;
                        else
                        window.location.href = href + "?" + name + "=" + value;
                        }
                    }
const purchases = new Purchases(configButton.purchases, api);

const cardList = new CardList(container, '.card', header, api, false, {
    purchases
});

cardList.addEvent();



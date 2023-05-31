// 双语
const language_selection = document.getElementById("language_selection");
function language_translate() {
    let translate_obj = {
        check: language_selection.checked,
        dict: function(word) {
            if (this.check) {
                word = dict_cn2en[word];
            }
            return word;
        },
        translate_value: function(e) {
            let word = this.dict(e.getAttribute('la'));
            e.value = word;
        },
        translate_innerHTML: function(e) {
            let word = this.dict(e.getAttribute('la'));
            e.innerHTML = word;
        },
        translate_placeholder: function(e) {
            let word = this.dict(e.getAttribute('la'));
            e.placeholder = word;
        },
    };
    let translate_value_list = document.getElementsByClassName("translate-value");
    for (let i = 0; i < translate_value_list.length; ++i) {
        translate_obj.translate_value(translate_value_list[i]);
    }
    let translate_innerhtml_list = document.getElementsByClassName("translate-innerhtml");
    for (let i = 0; i < translate_innerhtml_list.length; ++i) {
        translate_obj.translate_innerHTML(translate_innerhtml_list[i]);
    }
    let translate_placeholder_list = document.getElementsByClassName("translate-placeholder");
    for (let i = 0; i < translate_placeholder_list.length; ++i) {
        translate_obj.translate_placeholder(translate_placeholder_list[i]);
    }
};
language_selection.onchange = () => {
    language_translate();
};
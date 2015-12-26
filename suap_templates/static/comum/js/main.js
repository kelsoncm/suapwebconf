// Variáveis
window.__admin_media_prefix__ = "/static/admin/";

function open_menu_item(menu_item_id) {
    elem = jQuery("#menu-item-" + menu_item_id);
    elem.addClass("active");
    elem.parents("li").addClass("active").toggleClass("opened");
    elem.parents("ul,li").show();
}

function mode_responsive() {
    if ($(window).width() < 940) {
        $("body").addClass("hideSidebar");
    }
}

// Módulo de Abas da página inicial
function moduloAbas(aba) {
    if (!jQuery(aba).hasClass("active")) {
        jQuery(aba).parent().find("h4").removeClass("active");
        jQuery(aba).addClass("active");   
    }
}

function initMenu() {
    /* Menu principal: Toggle Sidebar */
    menu_hide_sidebar = function(){
        jQuery("nav > ul > li").removeClass("hint--right");
        jQuery("nav > ul > li").removeAttr("data-hint");
    };
    
    /* Menu principal */
    jQuery("nav li.has-child > a").click(function(e){
        e.preventDefault();
        if (jQuery("body").hasClass("hideSidebar")) {
            menu_hide_sidebar();
            jQuery("body").removeClass("hideSidebar");
        }
        $(this).parent("li").toggleClass("opened");
        $(this).next("ul").toggle(); 
    });
    
    /* Menu principal: Toggle Sidebar */
    jQuery("#acoes.toggleSidebar").click(function(e){
        e.preventDefault();
        if (jQuery("body").hasClass("hideSidebar")) {
            jQuery("html, body").animate({scrollTop: "0px"}, 'slow');
            menu_hide_sidebar();
            jQuery("nav li.opened > ul").show("slow");
            $.get( "/comum/expandir_menu/" );
        } else {
            jQuery("nav > ul > li").addClass("hint--right");
            jQuery("nav > ul > li").each(function(){
                var texto = jQuery(this).find("> a").text();
                jQuery(this).attr("data-hint", texto);
                $(this).find("ul").hide();
            });
            $.get( "/comum/retrair_menu/" );
        }
        jQuery("body").toggleClass("hideSidebar");
    });
}

var popupUserTriggerAtual;
var popupUserTrigger;
function hide_user_popup(popupUser){
    setTimeout(function() { popupUser.removeClass("active"); }, 3000);
}
    
function show_user_popup(profileId){
    var popupUser = jQuery('.popup-user-container');
    if(popupUser.length == 0 || !popupUser.hasClass('active')){
        jQuery.ajax({
             url: "/djtools/user_info/"+profileId+"/",
             async: false,
             method: "GET",
        }).done(function(data) {
            var popupUser = jQuery('.popup-user-container');
            popupUser.remove();
            jQuery('body').append(data);
            popupUser = jQuery('.popup-user-container');
            var position = popupUserTrigger.offset();
            position['top'] = position['top']+23;
            popupUser.css(position);
            
            popupUser.toggleClass("active");
            if(popupUser.hasClass('active')){
                setTimeout(function() {
                    var isHovered = jQuery('.popup-user-container:hover').length > 0;
                    if (!isHovered) {
                        hide_user_popup(popupUser);
                    }
                }, 1000);
            }
            popupUser.hover(function() {}, 
                function(){
                    hide_user_popup(popupUser);
                });
        });
    }
}

/* Buscar itens de menu */
String.prototype.removeAccents = function(){
 return this
         .replace(/[áàãâä]/gi,"a")
         .replace(/[éè¨ê]/gi,"e")
         .replace(/[íìïî]/gi,"i")
         .replace(/[óòöôõ]/gi,"o")
         .replace(/[úùüû]/gi, "u")
         .replace(/[ç]/gi, "c")
         .replace(/[ñ]/gi, "n")
         .replace(/[^a-zA-Z0-9]/g," ");
}

function __treeListFilter(input_text, list_name, timeout) {
    var list = jQuery(list_name);
    var new_list = list.clone().appendTo(list.parent());
    new_list.children().find('*').show();
    new_list.find('li.has-child').addClass("opened");
    new_list.hide();
    var input = jQuery(input_text);
    var keyTimeout;
    var lastFilter = '';

    // Default timeout
    if (timeout === undefined) {
        timeout = 200;
    }

    function filterList(ulObject, filterValue) {
        if (!ulObject.is('ul') && !ulObject.is('ol')) {
            return false;
        }
        var children = ulObject.children();
        var result = false;
        for (var i = 0; i < children.length; i++) {
            var liObject = jQuery(children[i]);
            if (liObject.is('li')) {
                var display = false;
                if (liObject.children().length > 0) {
                    for (var j = 0; j < liObject.children().length; j++) {
                        var subDisplay = filterList(jQuery(liObject.children()[j]), filterValue);
                        display = display || subDisplay;
                    }
                }
                if (!display) {
                    var text = liObject.text().removeAccents();
                    display = text.toLowerCase().indexOf(filterValue.removeAccents()) >= 0;
                    if (display) {
                        liObject.addClass('__show-children__');
                    }
                }
                liObject.css('display', display ? 'block' : 'none');
                result = result || display;
            }
        }
        ulObject.find('.__show-children__').find('*').show();
        return result;
    }

    input.change(function () {
        var filter = input.val().toLowerCase();
        if (filter != '') {
            list.hide();
            new_list.show();
            new_list.find('*').removeClass('__show-children__');
        } else {
            list.show();
            new_list.hide();
        }
        filterList(new_list, filter);
        return false;
    }).keydown(function () {
        clearTimeout(keyTimeout);
        keyTimeout = setTimeout(function () {
            if (input.val() === lastFilter) return;
            lastFilter = input.val();
            input.change();
        }, timeout);
    });
    return this;
}

function initAll(context) {
    if (!context) var context = "body";
    
    // Buscar Itens de Menu
    __treeListFilter('#__filterinput__', '#lista-menu-lateral', 200);

    // Responsive mode
    mode_responsive();

	/* Action Bar */
    jQuery(context).find(".action-bar .has-child > a").click(function() {
        jQuery(this).next("ul").toggle();
        return false;
    });
    jQuery(context).find(".action-bar .has-child ul").hover(function() {
	}, function () {
		jQuery(this).hide("fast");
	});
	
	// Label Required
	jQuery(context).find("label.required, .required label").attr("title", "Preenchimento obrigatório");

	/* Box */
    jQuery(context).find(".box h3").click(function() {
        jQuery(this).parent().find("> div").animate({
            height: 'toggle'
        });   
        jQuery(this).parent().toggleClass("hideInfo");
        var atributo = jQuery(this).attr("title");
        if (atributo == "Mostrar informações") {
            jQuery(this).attr("title", "Esconder informações");
        } else {
            jQuery(this).attr("title", "Mostrar informações");
        }
        return false;
    });
    
    /* Action Links */
    jQuery(context).find(".action-print a").click(function() {
	    print();
        return false;
    });
    jQuery(context).find("#topodapagina").click(function(){
		jQuery('html, body').animate({scrollTop:0}, 'slow');
	});

	/* Âncoras */
	jQuery(context).find(".ancoras").click(function() {
		jQuery(this).toggleClass("hideInfo");
		jQuery(context).find(".com_ancora").toggleClass("hideInfo");
	});
	jQuery(context).find(".ancoras a").click(function() {
		var link = jQuery(this).attr("href");
		var destino = jQuery(link).offset().top;
		jQuery("html, body").animate({scrollTop: destino}, 'slow');
        return false;
	});
	jQuery(context).find(".ancoras-telefones a").click(function() {
		var link = jQuery(this).attr("href");
		jQuery(context).find(".ancoras-telefones li").removeClass("selected");
		jQuery(this).parent("li").addClass("selected");
		jQuery(context).find("div.container").hide();
		jQuery(link).parent("div.container").show();
		var destino = jQuery(link).offset().top;
		jQuery("html, body").animate({scrollTop: destino}, 'slow');
        return false;
	});

    /* Barra de progresso */
    jQuery(context).find(".progress p").each(function() {
        var texto = jQuery(this).text();
        var porcentagem = texto.indexOf("%");
        if (porcentagem==-1) {
            var split = texto.split('/');
            texto = split[0]*100/split[1] + "%";
        }
        jQuery(this).css("width", texto);
        jQuery(this).parent().attr("title", texto);
    });
    
    jQuery(context).find(".confirm, .danger, .icon-trash").not(".no-confirm, .ajax").click(function(e) {
        var result = confirm(jQuery(this).attr("data-confirm") || "Tem certeza que deseja continuar?");

        if(result != true) {
            e.preventDefault();
        }
    });
    
    jQuery(context).find(".voltar").click(function() {
        window.history.back();
    });

	jQuery(context).find("#menu-device a").click(function() {
        jQuery(context).find('nav > ul').toggle();
    });
    
    // Popup User
    jQuery(context).find(".popup-user-trigger").click(function(e) {
        popupUserTrigger = jQuery(this);
        var profileId = popupUserTrigger.data("profile-id");
        var popupUser = jQuery('.popup-user-container');
        //Se já existir um popup ativo remova
        var estahAtivo = popupUser.length > 0 && popupUser.hasClass('active');
        if(estahAtivo){
            popupUser.remove();
            //Se o que foi clicado não foi o mesmo além de fechar a cima deve-se abrir o novo
            if(JSON.stringify(popupUserTriggerAtual) != JSON.stringify(popupUserTrigger)){
                //abrir poppup
                show_user_popup(profileId);
            }
        } else {
            //abrir poppup
            show_user_popup(profileId);
        }
        popupUserTriggerAtual = popupUserTrigger;
        e.preventDefault();
    });
    
    // Mapeamento de classes e title's
    mapeamento_class_title = {
        csv: "Exportar para CSV",
        pdf: "Exportar para PDF",
        editar16: "Editar",
        remover16: "Remover",
        detalhar16: "Detalhar",
        upload16: "Enviar Arquivo",
        cracha16: "Gerar crachá",
        carteira16: "Gerar carteira"
    };
    for (key in mapeamento_class_title) {
        jQuery.each(jQuery("a."+key), function(index, value) {
            elem = jQuery(value);
            if (elem.attr("title") == "") {
                elem.attr("title", mapeamento_class_title[key]);
            }
        });
    }
	
	// Expandir
	jQuery(context).find(".action-bar .normalscreen").hide();
	jQuery(context).find(".action-bar .fullscreen").click(function() {
		jQuery(this).hide();
		jQuery(context).find("aside, footer, h2").hide();
		jQuery(context).find(".action-bar .normalscreen").show();
		jQuery(context).find("article").addClass("fullscreen");
	});
	jQuery(context).find(".action-bar .normalscreen").click(function() {
		jQuery(this).hide();
		jQuery(context).find("aside, footer, h2").show();
		jQuery(context).find(".action-bar .fullscreen").show();
		jQuery(context).find("article").removeClass("fullscreen");
	});
    
    // Remove o ícone padrão do Django por um do estilo
    jQuery(context).find(".selector-chosen .selector-filter img").attr("src", "/static/comum/img/selector-choosen.png");
    
    // Módulo de Abas da página inicial
    jQuery(context).find(".modulo-abas h4").click(function() {
        moduloAbas(this);
    });
    
    // esconder Links Sem Filhos
    jQuery(context).find(".action-bar .has-child").find("ul").each(function() {
        if (!jQuery(this).has("li").length) {
            jQuery(this).parent().hide();
        }
    });
    
}
jQuery(document).ready(function() {
    initAll();
    initMenu();
    
    /* Menu principal: Para dispositivos moveis */
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        jQuery("body").addClass("hideSidebar");
    }
});

jQuery.expr[":"].icontains = jQuery.expr.createPseudo(function(arg) {
    return function( elem ) {
        return jQuery(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});


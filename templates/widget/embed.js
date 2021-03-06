{% load escapejs %}
(function() {
    var innerStyle = '{% escapejs %}{% include "widget/widget.css" %}{% endescapejs %}';
    var innerWidgetHTML = '{% escapejs %}{% include "widget/widget.html" %}{% endescapejs %}';

{% if element_id %}
    var containingElement = document.getElementById('{{ element_id }}');
{% else %}
    var containingElement;
    var scripts = document.getElementsByTagName('script');
    for (var i = 0; i < scripts.length; i++) {
        if (scripts[i].src.match(/embed_widget.js/)) {
            containingElement = document.createElement('div');
            scripts[i].parentNode.insertBefore(containingElement, scripts[i]);
            break;
        }
    }
{% endif %}
    containingElement.innerHTML =
        ['<style>', innerStyle, '</style>', innerWidgetHTML].join('');

    var scripts = [
    {% for dep in js_dependencies %}
      '{{dep|safe}}'{% if not forloop.last %},{% endif %}
    {% endfor %}];

    var identifier = {% include "widget/embed_params.js" %};

    var head = document.getElementsByTagName('head')[0];

    if (typeof(mirosubs) != 'undefined' && 
        typeof(mirosubs.EmbeddableWidget) != 'undefined')
        mirosubs.EmbeddableWidget.wrap(identifier);
    else {
        if (!window.MiroSubsLoading) {
            window.MiroSubsLoading = true;
            for (var i = 0; i < scripts.length; i++) {
                var script = document.createElement('script');
                script.type = 'text/javascript';
                script.src = scripts[i];
                script.charset = 'UTF-8';
                head.appendChild(script);
            }
        }
        if (typeof(MiroSubsToEmbed) == 'undefined')
            window.MiroSubsToEmbed = [];
        window.MiroSubsToEmbed.push(identifier);
    }

    if (!window.MiroCSSLoading) {
        window.MiroCSSLoading = true;
        var css = document.createElement("link");
        css.type = "text/css";
        css.rel = 'stylesheet';
        css.href = 'http://{{site.domain}}/site_media/css/mirosubs-widget.css';
        css.media = 'screen';
        head.appendChild(css);
    }
})();
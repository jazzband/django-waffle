(function(){
    var FLAGS = {
        {% for flag, value in flags %}'{{ flag }}': {% if value %}true{% else %}false{% endif %}{% if not forloop.last %},{% endif %}{% endfor %}
    };
    window.waffle = function waffle(flag) {
        return !!FLAGS[flag];
    };
})();

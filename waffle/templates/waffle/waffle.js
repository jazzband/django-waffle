(function(){
    var FLAGS = {
        {% for flag, value in flags %}'{{ flag }}': {% if value %}true{% else %}false{% endif %}{% if not forloop.last %},{% endif %}{% endfor %}
    };
    window.waffle = function waffle(flag) {
        if (typeof FLAGS[flag] == 'undefined') {
            return false;
        }
        return FLAGS[flag];
    };
})();

(function(){
    var FLAGS = {
        {% for flag, value in flags %}'{{ flag }}': {% if value %}true{% else %}false{% endif %}{% if not forloop.last %},{% endif %}{% endfor %}
        },
        SWITCHES = {
        {% for switch, value in switches %}'{{ switch }}': {% if value %}true{% else %}false{% endif %}{% if not forloop.last %},{% endif %}{% endfor %}
        };
    window.waffle = {
        flag: function waffle_flag(flag_name) {
            return !!FLAGS[flag_name];
        },
        switch: function waffle_switch(switch_name) {
            return !!SWITCHES[switch_name];
        }
    };
})();

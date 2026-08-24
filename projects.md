---
layout: default
title: Projects
---

# Projects

<ul class="index">
{% for project in site.data.projects %}
  <li><a href="{{ project.url }}">{{ project.title }}</a></li>
{% endfor %}
</ul>

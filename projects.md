---
layout: default
title: Projects
---

# Projects

<ul class="project-list">
{% for project in site.data.projects %}
  <li><a href="{{ project.url }}">{{ project.title }}</a></li>
{% endfor %}
</ul>

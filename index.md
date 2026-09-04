---
layout: default
title: Home
---

## Latest Posts

<ul class="index">
  {% for post in site.posts %}
  <li>
    <a href="{{ post.url }}">{{ post.title }}</a><span class="index-date">{{ post.date | date: "%b %-d, %Y" }}</span>
  </li>
  {% endfor %}
</ul>

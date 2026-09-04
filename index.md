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

{% comment %}
  Solutions land weekly and posts land every couple of months, so a home page
  that showed only posts would look dormant during the stretch the site is most
  active. Capped at five and kept in its own list: an essay and "2.6" in one
  stream makes the essay look small and the section look inflated.
{% endcomment %}
{% assign recent = site.analysis | sort: "date" | reverse %}
{% if recent.size > 0 %}
## Working through

<ul class="index">
  {% for s in recent limit: 5 %}
  <li>
    <a href="{{ s.url }}">&sect;{{ s.section }} {{ s.title }}</a><span class="index-date">{{ s.date | date: "%b %-d, %Y" }}</span>
  </li>
  {% endfor %}
</ul>

<p><a href="/math/analysis/">All sections &rsaquo;</a></p>
{% endif %}

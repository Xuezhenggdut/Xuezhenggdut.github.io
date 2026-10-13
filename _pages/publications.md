---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---
{% assign author = site.data.authors[page.author] | default: site.author %}
{% assign pubs = site.data.publications.items %}
{% assign journal_pubs = pubs | where: "type", "journal" | sort: "year" | reverse %}
{% assign conference_pubs = pubs | where: "type", "conference" | sort: "year" | reverse %}
{% assign scholar_profile = site.data.publications.profile %}

{% if author.googlescholar %}
<p class="pub-meta-note">
  Data source: <a href="{{ author.googlescholar }}">Google Scholar</a>.
  {% if scholar_profile %}
  <span class="pub-dot">&middot;</span>Citations {{ scholar_profile.citations }}
  <span class="pub-dot">&middot;</span>h-index {{ scholar_profile.h_index }}
  <span class="pub-dot">&middot;</span>i10-index {{ scholar_profile.i10_index }}
  {% endif %}
</p>
{% endif %}

<div class="pub-filter" role="tablist" aria-label="Publication Type Filter">
  <button class="pub-filter-btn is-active" type="button" data-filter="all">All</button>
  <button class="pub-filter-btn" type="button" data-filter="journal">Journal</button>
  <button class="pub-filter-btn" type="button" data-filter="conference">Conference</button>
</div>

<section class="pub-block" data-block="journal">
  <h2 class="pub-section-title"><i class="fas fa-book-open" aria-hidden="true"></i> Journal Articles</h2>
  <div class="pub-list">
    {% for pub in journal_pubs %}
      <article class="pub-item" data-type="{{ pub.type }}">
        <span class="pub-label">J{% if forloop.index < 10 %}0{% endif %}{{ forloop.index }}</span>
        <div class="pub-content">
          <p class="pub-title"><a class="pub-title-link" href="{{ pub.paper_url | default: pub.scholar_url }}" target="_blank" rel="noopener noreferrer">{{ pub.title }}</a></p>
          <p class="pub-authors">{{ pub.authors }}</p>
          <p class="pub-venue"><em>{{ pub.venue }}</em>, {{ pub.year }}</p>
          <p class="pub-links">
            <a class="pub-cite-link" href="{{ pub.scholar_url }}" target="_blank" rel="noopener noreferrer">
              <span class="pub-cite-box">
                <span class="pub-cite-label">Citation</span>
                <span class="pub-cite-value">{{ pub.cited_by }}</span>
              </span>
            </a>
          </p>
        </div>
      </article>
    {% endfor %}
  </div>
</section>

<section class="pub-block" data-block="conference">
  <h2 class="pub-section-title"><i class="fas fa-microphone-lines" aria-hidden="true"></i> Conference Papers</h2>
  <div class="pub-list">
    {% for pub in conference_pubs %}
      <article class="pub-item" data-type="{{ pub.type }}">
        <span class="pub-label pub-label-conf">C{% if forloop.index < 10 %}0{% endif %}{{ forloop.index }}</span>
        <div class="pub-content">
          <p class="pub-title"><a class="pub-title-link" href="{{ pub.paper_url | default: pub.scholar_url }}" target="_blank" rel="noopener noreferrer">{{ pub.title }}</a></p>
          <p class="pub-authors">{{ pub.authors }}</p>
          <p class="pub-venue"><em>{{ pub.venue }}</em>, {{ pub.year }}</p>
          <p class="pub-links">
            <a class="pub-cite-link" href="{{ pub.scholar_url }}" target="_blank" rel="noopener noreferrer">
              <span class="pub-cite-box">
                <span class="pub-cite-label">Citation</span>
                <span class="pub-cite-value">{{ pub.cited_by }}</span>
              </span>
            </a>
          </p>
        </div>
      </article>
    {% endfor %}
  </div>
</section>

<script>
  (function () {
    var buttons = Array.prototype.slice.call(document.querySelectorAll(".pub-filter-btn"));
    var blocks = Array.prototype.slice.call(document.querySelectorAll(".pub-block"));

    function setFilter(filter) {
      buttons.forEach(function (btn) {
        btn.classList.toggle("is-active", btn.getAttribute("data-filter") === filter);
      });

      blocks.forEach(function (block) {
        var blockType = block.getAttribute("data-block");
        var visible = filter === "all" || filter === blockType;
        block.style.display = visible ? "" : "none";
      });
    }

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        setFilter(btn.getAttribute("data-filter"));
      });
    });
  })();
</script>

---
permalink: /
title: "<i class='fas fa-user' aria-hidden='true'></i> About me"
excerpt: "About me"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---
<div class="home-hero">
  <p class="home-lead">
    Zheng Xue received the Ph.D. degree in Information and Communication Engineering from Guangdong University of Technology (GDUT), Guangzhou, China, in 2024.
    He is currently a Postdoctoral Researcher at GDUT, working with <a href="https://yzw.gdut.edu.cn/info/1088/1333.htm"><span class="name-nowrap">Prof. Yi Fang</span></a> and <a href="https://teacher.gdut.edu.cn/hanguojun"><span class="name-nowrap">Prof. Guojun Han</span></a>.
  </p>
  <p class="home-focus"><strong>Research Interests:</strong> Vehicular Networks, Edge Intelligence, Cooperative Perception, and Agent Networks.</p>
</div>

<i class="fas fa-graduation-cap" aria-hidden="true"></i> Education
======
<div class="edu-grid">
  <article class="edu-card">
    <div class="edu-logo edu-logo--gdut">
      <img src="/images/logos/gdut-logo.svg" alt="Guangdong University of Technology logo">
    </div>
    <div class="edu-body">
      <p class="edu-degree">Ph.D., Information and Communication Engineering</p>
      <p class="edu-school">School of Information Engineering, Guangdong University of Technology</p>
      <p class="edu-meta"><span>2021.09 - 2024.06</span><span>Guangzhou, China</span></p>
    </div>
  </article>
  <article class="edu-card">
    <div class="edu-logo edu-logo--gdut">
      <img src="/images/logos/gdut-logo.svg" alt="Guangdong University of Technology logo">
    </div>
    <div class="edu-body">
      <p class="edu-degree">B.Eng., Electronic and Communication Engineering</p>
      <p class="edu-school">School of Information Engineering, Guangdong University of Technology</p>
      <p class="edu-meta"><span>2018.09 - 2021.06</span><span>Guangzhou, China</span></p>
    </div>
  </article>
  <article class="edu-card">
    <div class="edu-logo edu-logo--cqjtu">
      <img src="/images/logos/cqjtu-logo.svg" alt="Chongqing Jiaotong University logo">
    </div>
    <div class="edu-body">
      <p class="edu-degree">Bachelor, Automotive Service Engineering</p>
      <p class="edu-school">College of Traffic and Transportation, Chongqing Jiaotong University</p>
      <p class="edu-meta"><span>2014.09 - 2018.06</span><span>Chongqing, China</span></p>
    </div>
  </article>
</div>

<i class="fas fa-newspaper" aria-hidden="true"></i> Selected Publications
======
{% assign top_journal_pubs = site.data.publications.items | where: "type", "journal" | sort: "cited_by" | reverse %}
<div class="selected-pub-list">
  {% for pub in top_journal_pubs limit: 4 %}
  <article class="selected-pub-item">
    <p class="selected-pub-title"><a class="pub-title-link" href="{{ pub.paper_url | default: pub.scholar_url }}" target="_blank" rel="noopener noreferrer">{{ pub.title }}</a></p>
    <p class="selected-pub-authors">{{ pub.authors }}</p>
    <p class="selected-pub-venue"><em>{{ pub.venue }}</em>, {{ pub.year }}</p>
    <p class="selected-pub-links">
      <a class="pub-cite-link" href="{{ pub.scholar_url }}" target="_blank" rel="noopener noreferrer">
        <span class="pub-cite-box">
          <span class="pub-cite-label">Citation</span>
          <span class="pub-cite-value">{{ pub.cited_by }}</span>
        </span>
      </a>
    </p>
  </article>
  {% endfor %}
</div>
- More papers: [full publication list](/publications/).

<i class="fas fa-project-diagram" aria-hidden="true"></i> Projects
------
- Performance Fairness and Isolation Algorithms for Multi-Tenant Enterprise SSDs
- Low-Latency Multi-Channel High-Definition Video Transmission System
  <!-- ![System Diagram](/images/FPGA.png "System Diagram") -->
- [V2X Cooperative Perception System](https://github.com/Xuezhenggdut/V2X_cooperative_perception_system)
- [Research on Resource Allocation and Collaborative Perception Technologies in Vehicular Edge Computing](http://xuezhenggdut.github.io/files/doctoral_thesis.pdf)
- [Research on Data Transmission and Caching Strategies in Vehicular Networks](http://xuezhenggdut.github.io/files/master_thesis.pdf)

<i class="fab fa-github" aria-hidden="true"></i> Open Source
------
- [Paper with code for communication and network](https://github.com/Xuezhenggdut/Paper_with_code_for_communication_and_network) ![GitHub Repo stars](https://img.shields.io/github/stars/Xuezhenggdut/Paper_with_code_for_communication_and_network.svg?style=flat-square&cacheSeconds=3600)
- [learn how to research](https://github.com/Xuezhenggdut/learn_how_to_research) ![GitHub Repo stars](https://img.shields.io/github/stars/Xuezhenggdut/learn_how_to_research?style=flat-square)
- [Security in Vehicular Networks and Autonomous Driving](https://github.com/Internet-of-Vehicles-Code/Security_in_Vehicular_Networks_and_Autonomous_Driving) ![GitHub Repo stars](https://img.shields.io/github/stars/Internet-of-Vehicles-Code/Security_in_Vehicular_Networks_and_Autonomous_Driving?style=flat-square)

<i class="fas fa-globe-asia" aria-hidden="true"></i> Visitor Map
------
<div class="visitor-map">
  <script type='text/javascript' id='clustrmaps' src='//cdn.clustrmaps.com/map_v2.js?cl=ffffff&w=600&t=n&d=N0b8H83Io6TZu6SShY5_UIAVuBntR3kpP45Pa18rhcc'></script>
</div>

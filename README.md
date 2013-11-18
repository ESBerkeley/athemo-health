athemo-health
=============

sudo pip install django-static-precompiler
sudo pip install django

{% load scss %}

<link rel="stylesheet" href="{{ STATIC_URL}}{% scss "path/to/styles.scss" %}" />

sudo gem install sass

---
name: review.md
description: Handwritten instructions/notes intendend for the AI - Date - summary - detail. Goal is to carefully review and correct the AI with the focus on the review
---
## 10-05-26 - Initial review notes, rebuilt from clean pelican, added my theme
 - need to clean up theme, AI put in too much actual content from the previous site, there should not be any more content in the site then is in the \content directory, right now i just have content\pages\about.md, but i see broken links for photos and others in the generated site. no categories, tags, links, archives, nothing should exist in the lakefront template or site. Should be Home About on menu. Home page should have short description/text/summary and then a list of all/any posts, of which there are currently none.
 - style is a little off, attach a screen shot of previous site. fix up the lakeshore theme, fix styling and remove any and all content that isn't in the about page or home page now (you can fix up home.md now with summary and single list for small screen and double list for big screen)
 - give me simple templates to start with - too many in there now to start with, will circle back later for the complex ones like apps and gallery. For now lets start with page, post, idea, link, photo, chat.
 - base.html shouldn't have all those page links in the footer, just about (and home). its a list generated from the pages. If needed the template should code for the empty edge cases.
 - status should default to draft, not published
 - pelican field use:
  - template of articles will be post, project, til, idea, read, view, photo (to display a single photo), gallery and more. each template has a short code like TIL or READ, and longer like Book Review or Thing I Learned, an icon and then the particular view of the content - ideas will be different than a book review or photo.  any pages will be able to create views of specificy types (templates) or list all together, flexible sorting.
  - category will be used as my 'lanes' a key orientation of the site (and me), some starter ones would be 'ai', 'taichi', 'music', 'science', 'photography', 'art', 'crafts', 'diy', so pelican will create separate category pages with views of all posts (articles). In fact, lets use 'lanes' instead of categories throughout the display, still call it category for the metadata, but lane/lanes on the site.
  - ai can be an author, or other people, articles/pages that are all/partially ai will have ai as an author
  - like the provenance concept - me, mine, ai, ours, theirs, lets simply make it a tag (with tag page override/enhance)
  - need a way to author prose and other content for specific tags/categories, otherwise those pages will just have the default list of matching articles, and placeholder/dummy text/summary (don't generate AI content for missing things, in fact add agent rules to always use obviously placeholder text instead of generating content, unless asked). This new content will come from the /content/categories directory. so if there is a file /content/categories/taichi.md, the data in that file would be merged with the taichi category document generated, and the provided prose used in both the categories detail list view and in the category document (say for taichi). tags would work the same way. taichi is a category, but '/content/tags/taichi-108/grasp-birds-tail' or 'taichi-108/single-whip' would be tags. 
  - add custom 404 page - match theme, maybe add a nice photo
  - menu, menu_order, menu_title, featured, original_author,isbn, external_url
For all these items perform the analysis, maximize native pelican use, check for non-generic content in the lakefront theme, verify responsive web support for phone landscape/portrait, tablet landscape/portrait, desktop small display and TV/big display.
update Readme with key content metadata use, site rules/design, approach, devops, links to repo, tools, site

  
 ## need to add tests to get ui cleaned up, can fix what the ai can't see. need to add some skills and direction

 ## future - look at pelican internals, devise way to do datafile support like some other static site generators - tie back to pipeline-tools using pixeltable. A template should be able to look up tags in a data file maybe, definitely photos metadata.

**Name : ** Nick Chen
**Date : ** 20260909
**Forked repo : ** https://github.com/Avulpix0412/theailab-net

---

## (a) What improvements did you make? & (b) What resources did you use, and why did you choose them?

### Phase 1 - Engineering Hygiene

* This phase are some essential changes for the website to fulfill the requirements that a website that have

* Added favicons and `<meta name="description">` to all 22 pages to aviod affecting SEO and link-preview cards
* Added a link of "skip to content" for accessibility
* Added a .table-wrap (overflow-x: auto) to all `<table>` to aviod wide tables break the layout on mobile phone
* Removed approximately 150 lines of dead code from the original WordPress theme port such as blog-post cards or social-share buttons
* Built a pytest test suite that checksthe consistency and structural integrity of all pages that re-run after every changes to prevent from conflicts between changes and previous contents

### Phase 2 - Interactive Features & Visual Redesign

* This phase does not change the overall layout of the website, and the goal is to make it looks better and more interesting for students to explore

## Typography & color system
* Replaced the site's fonts with Fraunces for headings, Newsreader for body text, and Quicksand (bold) for UI
* Replaced the blue with a warm palette -- according to claude, a terracotta accent color, plus a muted five-color "kusumi-ro" (dusty Japanse pastel) palette. For the color system, I found it hard to describe in English what color I really want or to describe it in terms of RGB. I can only come up with unprofessional words like "milky", so I found some colors that I like on some color website and sent it to claude and let it conclude what's the similarity between these colors and then I can decide which color to use for the Website.

## Homepage Links Redesign
* Added a clickable SVG "15 weeks journey map" on the homepage, which is a curved path that connecting the 15 nodes that represents each week. I have different color represent weeks for different Mini-Project, and have diamond markers represent the three discussion weeks for "ethics thread"
* Implemented a "you are here" indicator written in JavaScript that reads the current date and highlights the week with a pulsing ring; It can also shows "on break, next: Week N" if students visit the website during October break or Thanks Giving break. 
* Removed the "Quick Links" on the homepage because there are not much thing on the homepage and you can visit all the links from the top already; I also removed the links of weekly schedule on the top and moved it to the map session with a link "Full schedule with dates →" because they are kind of repeat. I also added a section on the right that shows which week we are at, the topic of the week, a line to show how much percent we have completed, and a link "Go to this week →" to accomplish part of the function of the "Schedule" part and to make the right part of the website not too empty.

## Dark mode
* Built a dark mode that has a button of sun/moon icon and a lock button at the top-right corner of every page. They will follow the system time and light mode are from 7am to 7pm whereas dark mode are from 7pm to 7am. Users can hit the lock button to stay in one mode. If they switch by hand during the right session, for example, if one user switch from light mode to dark mode at 8am, the system will stay in dark mode until 7am the next day. I also separately designed the color palette for the dark mode to make it more visible against the dark background including the main color and the five colors for the mini project.

## Today in AI
* This is the section that I am most satisfied with adding. My initial thought was that the right part of the webpage is kind of empty, so I wished to add some feature to it, which led me to the thoughts of Today in AI. The implementation of it is pretty simple -- Javascript will call the Hacker News Algolia Search API which is a fully public endpoint that do not requires registration or API key. Then on page load, it will fetch today's posts through a date filter, and filters for AI relevance using a keyword list. Claude also added a feature that let it match with word-boundary regex (so that you do not get "air-conditioning" as results for ai). It will sort the results by upvotes and keep the top 8.
* Display: Once an hour, the 8 stories will be cached in the brower's localStorage and each time an user visit the website or refresh, it will pick a random title to display, so that you will not always getting one same news if you need to navigate the website through different pages within the hour. Also there is an AI generated sentence in the section which I do not intentionally ask for -- "The field does not pause for a syllabus - here's today's version of it, next to where you are in the course." I think it is really cool and let you know where you are in the field and what others are doing to make you feel connected and motivate your study, so I choose to keep it. 

## Interaction details
* Through CSS transform, the links on the top have a subtle "scale up on hover" effect as the cursor moves across them, just like the Dock bar in Macos system
* Also through CSS, added the View Transitions API for smooth crossfade transitions between page navigations that are native in the browser.

## Homepage background animation
* Added a `<canvas>`-based particle/line animation background on the homepage by HTML, which is basically a sunburst of rays radiating from on point and eases toward the cursor on mouse movement, rotates as users scroll, and reshuffles into a new pattern on click. Each ray will have its color independently that cycling from the site's existing palette. I get the inspiration from "Stripe.com", they have some really beautiful animation design on their webpage. I only added this animation on the home page, because I wish other sections to be material-focused.
* The cards ("map", "Today in AI", and "Go to this week")on the homepage use a "frosted glass" effect (CSS backdrop-filter: blur()), which makes the cards more integrated to the background especially when users scrolling through them over the animation background. 






## (c) what future feature improvements would you add?
* I have updated the weekly schedule of Week 3 based on the content of email Professor Chun sent. I have saved the pattern of this work, so that Claude will work fast when updating schedules for following weeks, which is highly likely because the the industry is changing rapidly. I initially wish to add a feature of "To-Do List" either at the homepage or the page of each week. Users can check each boxes when they finish corresponding work, but as the plans for each week are keep updating and hard to predict, I left this feature undone, but it is defintely worth adding when all the schedules are fixed.






## Generative AI Use Statement

* This project was built in collaboration with Claude Code, used as the primary implementation tool throughout.

* What Claude Code did:
* Wrote all actual code changes including HTML structure, CSS, and Javascript
* Ran the test suite after each change and fixed regressions it introduced
* Made all git commits and pushed them to Github when I approved
* Provide guidance if I don't understand some part of the task, including writing this markdown file

* What I did:
* Directed the overall design goals and aesthetic preferences
* Reviewed the result at each step and have feedback (the "Today in AI" section and the background animation each takes more than 10 rounds of revision to become what they are now)
* Made decisions on design tradeoffs
* Verified the finished site after each step
* Typed each single word in this markdown file
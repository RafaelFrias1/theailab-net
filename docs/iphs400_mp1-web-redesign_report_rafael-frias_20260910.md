Rafael Frias  
IPHS 400: Frontiers in Generative AI  
10 September 2026

**Mini-Project 1: Website Redesign**  
**Repository**: https://github.com/RafaelFrias1/theailab-net

**Step 1: Cleanup and fixes**  
Following the manual, I stripped the hosting and deployment files so the site would run locally on its own. Then I had Claude Code audit the repository and report what it found using this prompt:  
"Analyze the course website code in this repo and critique it for errors, omissions, missing best practices, etc. Save your results in a complete, clear, and well-structured report."  
Then, I had it turn that list into a ranked plan with step-by-step instructions, allowing me to read through and approve the plan before it made changes I wouldn’t understand.

The fixes that came out of this were mostly invisible from the outside:

* Accessibility. Added a "skip to content" link for keyboard users, labels that tell screen readers which page you're on, and proper headers on every table.  
* Search engine basics. Every page got a description tag and a favicon.  
* An actual content bug. One of the week’s source files contained the wrong week's material, and five weeks had links whose text didn't match the page they pointed to.  
* Repo cleanup. Removed about 240 lines of stylesheet code that no page was using and some junk files that had been committed by accident.

**Step 2: Visual redesign**  
From this point on, the changes were made beyond the manual. For each of the following additions and features, I had Claude assist me in drafting clear, detailed prompts, fed it to Claude code in plan mode, reviewed the plan, implemented the change, and then reviewed said changes before proceeding to the next feature.

For the look, I used al-folio (alshedivat.github.io/al-folio) as a reference. I had Claude Code pull its stylesheet directly and pick out values while being careful about blatantly copying. I told it:  
"Do not copy al-folio's CSS/JS wholesale; propose original values adapted to this site."

The site now sits in a centered column, uses fonts already installed on your computer, and sets the colors, spacing, and text sizes in one place at the top of the stylesheet.

**Step 3: Features added**

1. A dark/light toggle that remembers your choice between visits.  
2. An "up next" banner on the homepage showing the next assignment due, based on today's date.  
3. A highlight of the current week on the Schedule page, which figures out which week we are in and marks it.

I had Claude code test it against a handful of different dates to ensure the right week came up each time.

**What I'd add next**

* A search feature.  
* One source for dates. When I was making edits, the Schedule and Assignments pages drifted apart since they each have their own copy of dates.  
* A homepage diagram showing how the four mini-projects build on each other, and what we are working towards over the course of the semester.
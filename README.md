# valeem-site

Standalone pages for valeem.com that live alongside the Moodle site.

| Folder | Live address | Status |
| --- | --- | --- |
| `homeschool-pathways/` | https://www.valeem.com/homeschool-pathways/ | Live, under internal review |
| `new-home/` | https://www.valeem.com/new-home/ | Draft of the new homepage, for internal review |
| `online-tuition-saudi-arabia/` | https://www.valeem.com/online-tuition-saudi-arabia/ | Saudi Arabia page; price guidance pending |
| `online-tuition-uae/` | https://www.valeem.com/online-tuition-uae/ | UAE page; price guidance pending |
| `online-tuition/` | https://www.valeem.com/online-tuition/ | Online Tuition category page |
| `skills-courses/` | https://www.valeem.com/skills-courses/ | Skills & Courses category page |
| `teach-at-valeem/` | https://www.valeem.com/teach-at-valeem/ | Teacher page and application form (leads tagged TEACHER APPLICATION) |
| `root-files/llms.txt` | https://www.valeem.com/llms.txt | Plain-language facts for AI assistants |
| `root-files/robots.txt`, `root-files/sitemap.xml` | Site root | Crawler rules and the page list for search engines. Add each new page to the sitemap |
| `tools/lead-capture.gs` | Google Apps Script (not deployed from here) | Reference copy of the form script |

## How changes reach the site

1. Changes are committed to the `main` branch of this repository.
2. In cPanel, open **Git Version Control**, click **Manage** on this repository, open **Pull or Deploy**, then click **Update from Remote** followed by **Deploy HEAD Commit**.
3. `.cpanel.yml` copies only the folders and files it lists into `public_html`. It never deletes files and never touches Moodle.

`new-home/` carries a `noindex` tag while it is a draft. Remove that line when it becomes the real homepage.

## Forms

Both pages post to the same Apps Script web app, which writes to the "Enquiries" tab of the
"Homeschool Pathways Enquiries" Google Sheet and emails contact@valeem.com.
Homepage enquiries are tagged `HOMEPAGE:` in the `interests` column.

WhatsApp number used on both pages: +92 332 2636574.

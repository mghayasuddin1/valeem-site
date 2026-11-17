# valeem-site

Standalone pages for valeem.com that live alongside the Moodle site.

| Folder | Live address | Status |
| --- | --- | --- |
| `homeschool-pathways/` | https://www.valeem.com/homeschool-pathways/ | Live, under internal review |
| `new-home/` | https://www.valeem.com/new-home/ | Draft of the new homepage, for internal review |
| `tools/lead-capture.gs` | Google Apps Script (not deployed from here) | Reference copy of the form script |

## How changes reach the site

1. Changes are committed to the `main` branch of this repository.
2. In cPanel, open **Git Version Control**, click **Manage** on this repository, open **Pull or Deploy**, then click **Update from Remote** followed by **Deploy HEAD Commit**.
3. `.cpanel.yml` copies only the folders it lists into `public_html`. It never deletes files and never touches Moodle.

## Forms

Both pages post to the same Apps Script web app, which writes to the "Enquiries" tab of the
"Homeschool Pathways Enquiries" Google Sheet and emails contact@valeem.com.
Homepage enquiries are tagged `HOMEPAGE:` in the `interests` column.

WhatsApp number used on both pages: +92 332 2636574.

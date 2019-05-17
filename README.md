# PublicPages: FB OpenGraph API data collection
## A simple API downloader for FB's public pages data 

This script calls the FB API (v3.3) on a public page.
Under main you can define a page_id, that you find in the URL of the public page that you are interested.
For example, for the Italian newspaper Repubblica (https://www.facebook.com/repubblica -> page_id = 'repubblica')
The resulting dataset contains these fields:

| title | description | message | status_type | url | date | post_id | comments | shares | likes | love | wow | haha | sad | angry |
|-------|-------------|---------|-------------|-----|------|---------|----------|--------|-------|------|-----|------|-----|-------|

You can find an example dataset in 'repubblica_example.tsv'
The idea is based on [minimaxir](https://github.com/minimaxir)'s [facebook scraper](https://github.com/minimaxir/facebook-page-post-scraper), which was built before FB closed the access to public pages.

Now you __need__ to submit your app for App Review process in order have the [Page Public Content Access](https://developers.facebook.com/docs/apps/review/feature#reference-PAGES_ACCESS).

After the approval you will be able to retrieve data from the endpoint ```/{page-id}/feed```. 
The app, after approval, will still be subject to [Rate Limiting](https://developers.facebook.com/docs/graph-api/overview/rate-limiting#application-level-rate-limiting). I have not implemented any fancy throttling method on this, but suggestions are more than welcome. Same goes for the exception-handling during the parsing of json response.

For the time being, the script is far from perfect but could be helpful to retrieve quickly similar datasets once the App Review process is complete.

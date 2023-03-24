# Solution for fishy-motd

## Introduction
This challenge is based off of [CWE-1022](https://cwe.mitre.org/data/definitions/1022.html). In essence, when clicking on an `<a>` tag that has the rel="opener" attribute, the newly opened page can change the original window's url. This allows bad actors to phish users. In reality, this requires control of the website, but one important thing to learn from this is to never use `rel="opener"`, and rather use `rel="noopener noreferrer"`. Although `noopener` is now the [implicit default](https://mathiasbynens.github.io/rel-noopener/), having both is the best practice.

## Solution
1. Set the MOTD to a link to a page you control, with the attributes `target="_blank" rel="opener"`. This allows you to open a new window, while maintaining control of the window.location of the original window. 
2. This new page can be modelled after [redirect.html](./redirect.html). In the bot function, there's a 1 second waiting period that prevents trivial solutions that open a simple phishing page—this also simulates real users that would likely realize that the url just changed to a malicious domain. To bypass this, make a `setTimeout` that waits for a bit more than 1 second, the sets the `window.opener.location` to your phishing page.
3. Model the final fake login page after [fakelogin.html](./fakelogin.html). It's enough to simply copy the original page's HTML/CSS and add a webhook on form submission.
4. Use the scraped credentials to get the flag
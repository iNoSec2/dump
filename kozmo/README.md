<p align="middle">
  <img src="https://image.ibb.co/jV0cyK/kozmo_1.png">
  <h1 align="middle">Kozmo</h1>
</p>

Kozmo is a manual web application testing framework designed to be minimal, modular, efficient & powerful.

## What's Kozmo?
Kozmo has a lot of amazing features but to understand it's core functionality, let's try to test a webpage for LFI vulnerabiliy.

![demo](https://image.ibb.co/nwKwSe/Screenshot_2018_08_22_10_57_51.png)

So basically this is Kozmo's core funtionality i.e. it let's you make & compare HTTP requests.
The status bar on the top of every response let's you monitor all the properties you need to analyse. The properties which differ from the original response are highlighted in red.\
It displays only the changed content of response body instead of printing the whole thing and the input is highlighted in green.

### What makes Kozmo awesome?

Kozmo supports GET & POST methods and let's you easily alter values of different parameters.\
Need to run a system command? No program, you can just do `os <command>`.\
Believe me your experience with Kozmo is going to be smooth!

![ux](https://github.com/user-attachments/assets/bfe3f6ff-9224-4926-81db-56dd8f71be08)

Supplying headers to comamnd line programs is a pain in the ass but kozmo makes it painless by using nano as an input handler.

![headers](https://image.ibb.co/mh01ce/Screenshot_2018_08_22_12_40_12.png)

These are the default headers where the `$` sign tells Kozmo to handle the header value itself.\
You can modify them as you want or just paste the headers intercepted by Burp Suite or similar browser proxy tool.

#### Plugins
Kozmo's capabilities can be increased to greater extents with plugins. Following plugins are available at the moment:

- CMS Detector: Detects 389 content management systems
- WAF Detector: Detects 12 web application firewalls
- Web Technology Detector: Detects 1157 web technologies
- Subdomain Finder: Lightening fast subdomain finder
- Censys: Dumps data from censys.io
- Decodify: Detects & decodes encoded strings, recursively
- Encodify: Encodes strings
- XSStrike: Suggests XSS payloads by analysing reflection context

Kozmo has a lot more to offer. The detailed documentation can be found at [Kozmo's Wiki].

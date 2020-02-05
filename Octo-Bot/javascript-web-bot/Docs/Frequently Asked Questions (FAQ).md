# Frequently Asked Questions (FAQ)
Question: How do I determine the CSS selector of elements

Answer: Most modern browsers support this feature. Open "inspect element" and hover over the intended element, right click and there should be a option to copy the css selector. Below shows some examples on some browsers.

**Firefox**
![Copying css selector in firefox](resources/gif/CSS_Selector_Firefox.gif)

**Chrome**
![Copying css selector in chrome](resources/gif/CSS_Selector_Chrome.gif)

##
Q: Why does my browser crash in docker container?

A: Try adding the ```--shm-size 2g``` or ```-v /dev/shm:/dev/shm``` to the ```docker run``` command ([More information here](https://github.com/SeleniumHQ/docker-selenium/pull/485)).